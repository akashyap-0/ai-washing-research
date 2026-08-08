"""Train and apply the versioned multi-label FinBERT passage classifier.

Training refuses unadjudicated labels and splits by company to reduce leakage
from repeated corporate boilerplate. The original FinBERT sentiment head is
replaced with independent sigmoid labels; this is topic classification, not
ordinary positive/negative sentiment scoring.
"""

import argparse
import csv
import json
import os
import random

import label_schema

DEFAULT_MODEL = "ProsusAI/finbert"
MAX_LENGTH = 384


def load_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def validate_training_rows(rows):
    errors = []
    seen = set()
    for number, row in enumerate(rows, start=2):
        if row.get("passage_id") in seen:
            errors.append(f"row {number}: duplicate passage_id")
        seen.add(row.get("passage_id"))
        for error in label_schema.validate_annotation(row, require_adjudicated=True):
            errors.append(f"row {number}: {error}")
    companies = {row.get("ticker") for row in rows if row.get("ticker")}
    if len(companies) < 5:
        errors.append("at least five labeled companies are required for grouped splits")
    return errors


def seed_everything(seed):
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def grouped_splits(rows, seed):
    from sklearn.model_selection import GroupShuffleSplit

    indices = list(range(len(rows)))
    groups = [row["ticker"] for row in rows]
    outer = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=seed)
    train_val_idx, test_idx = next(outer.split(indices, groups=groups))
    train_val_idx = list(train_val_idx)
    inner_groups = [groups[index] for index in train_val_idx]
    inner = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=seed + 1)
    train_rel, val_rel = next(inner.split(train_val_idx, groups=inner_groups))
    train_idx = [train_val_idx[index] for index in train_rel]
    val_idx = [train_val_idx[index] for index in val_rel]
    return train_idx, val_idx, list(test_idx)


class PassageDataset:
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.encodings["input_ids"])

    def __getitem__(self, index):
        import torch

        item = {key: value[index] for key, value in self.encodings.items()}
        if self.labels is not None:
            item["labels"] = torch.tensor(self.labels[index], dtype=torch.float32)
        return item


def encode_rows(tokenizer, rows):
    return tokenizer(
        [row["text"] for row in rows], padding=True, truncation=True,
        max_length=MAX_LENGTH, return_tensors="pt",
    )


def predict(model, dataset, batch_size, device):
    import numpy as np
    import torch
    from torch.utils.data import DataLoader

    model.eval()
    probabilities = []
    with torch.no_grad():
        for batch in DataLoader(dataset, batch_size=batch_size, shuffle=False):
            inputs = {key: value.to(device) for key, value in batch.items()
                      if key != "labels"}
            logits = model(**inputs).logits
            probabilities.append(torch.sigmoid(logits).cpu().numpy())
    return np.concatenate(probabilities, axis=0)


def choose_thresholds(labels, probabilities):
    import numpy as np
    from sklearn.metrics import f1_score

    labels = np.asarray(labels)
    thresholds = {}
    for index, label in enumerate(label_schema.MODEL_LABELS):
        if len(set(labels[:, index])) < 2:
            thresholds[label] = 0.5
            continue
        candidates = np.arange(0.20, 0.81, 0.05)
        scored = [(f1_score(labels[:, index], probabilities[:, index] >= value,
                            zero_division=0), value)
                  for value in candidates]
        # On a tie, prefer the higher threshold and therefore higher precision.
        thresholds[label] = float(max(scored)[1])
    return thresholds


def evaluation_metrics(labels, probabilities, thresholds):
    import numpy as np
    from sklearn.metrics import average_precision_score, precision_recall_fscore_support

    labels = np.asarray(labels)
    output = {}
    for index, label in enumerate(label_schema.MODEL_LABELS):
        predicted = probabilities[:, index] >= thresholds[label]
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels[:, index], predicted, average="binary", zero_division=0)
        average_precision = None
        if len(set(labels[:, index])) > 1:
            average_precision = float(average_precision_score(
                labels[:, index], probabilities[:, index]))
        output[label] = {
            "threshold": thresholds[label],
            "prevalence": float(labels[:, index].mean()),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "average_precision": average_precision,
        }
    return output


def train(args):
    rows = load_rows(args.annotations)
    errors = validate_training_rows(rows)
    if errors:
        preview = "\n".join(errors[:25])
        raise ValueError(f"Annotation validation failed ({len(errors)} errors):\n{preview}")

    import numpy as np
    import torch
    from torch.utils.data import DataLoader
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    seed_everything(args.seed)

    train_idx, val_idx, test_idx = grouped_splits(rows, args.seed)
    subsets = {
        "train": [rows[index] for index in train_idx],
        "validation": [rows[index] for index in val_idx],
        "test": [rows[index] for index in test_idx],
    }
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.base_model, num_labels=len(label_schema.MODEL_LABELS),
        id2label={i: label for i, label in enumerate(label_schema.MODEL_LABELS)},
        label2id={label: i for i, label in enumerate(label_schema.MODEL_LABELS)},
        problem_type="multi_label_classification", ignore_mismatched_sizes=True,
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    datasets = {}
    matrices = {}
    for name, subset in subsets.items():
        matrices[name] = np.asarray([
            [int(row[label]) for label in label_schema.MODEL_LABELS]
            for row in subset
        ], dtype=np.float32)
        datasets[name] = PassageDataset(encode_rows(tokenizer, subset), matrices[name])

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    train_loader = DataLoader(datasets["train"], batch_size=args.batch_size,
                              shuffle=True)
    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        losses = []
        for batch in train_loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            optimizer.zero_grad()
            loss = model(**batch).loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            losses.append(loss.item())
        history.append({"epoch": epoch, "mean_train_loss": sum(losses) / len(losses)})
        print(f"epoch={epoch} mean_train_loss={history[-1]['mean_train_loss']:.6f}")

    validation_probabilities = predict(model, datasets["validation"],
                                        args.batch_size, device)
    thresholds = choose_thresholds(matrices["validation"], validation_probabilities)
    test_probabilities = predict(model, datasets["test"], args.batch_size, device)
    metrics = evaluation_metrics(matrices["test"], test_probabilities, thresholds)

    os.makedirs(args.output_dir, exist_ok=True)
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    metadata = {
        "label_schema_version": label_schema.SCHEMA_VERSION,
        "labels": list(label_schema.MODEL_LABELS),
        "base_model": args.base_model,
        "seed": args.seed,
        "thresholds": thresholds,
        "split_companies": {
            name: sorted({row["ticker"] for row in subset})
            for name, subset in subsets.items()
        },
        "split_rows": {name: len(subset) for name, subset in subsets.items()},
        "training_history": history,
        "held_out_test_metrics": metrics,
    }
    with open(os.path.join(args.output_dir, "research_metadata.json"), "w",
              encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
    print(f"Saved model and held-out evaluation to {args.output_dir}")


def score(args):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    rows = load_rows(args.passages)
    with open(os.path.join(args.model_dir, "research_metadata.json"),
              encoding="utf-8") as handle:
        metadata = json.load(handle)
    if metadata["labels"] != list(label_schema.MODEL_LABELS):
        raise ValueError("Model labels do not match the current label schema")

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    probabilities = predict(model, PassageDataset(encode_rows(tokenizer, rows)),
                            args.batch_size, device)

    fields = list(rows[0].keys()) if rows else []
    for label in label_schema.MODEL_LABELS:
        fields.extend([f"p_{label}", f"pred_{label}"])
    fields.extend(["pred_neutral", "model_version"])
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row, values in zip(rows, probabilities):
            output = dict(row)
            any_positive = False
            for index, label in enumerate(label_schema.MODEL_LABELS):
                probability = float(values[index])
                predicted = int(probability >= metadata["thresholds"][label])
                output[f"p_{label}"] = f"{probability:.8f}"
                output[f"pred_{label}"] = predicted
                any_positive |= bool(predicted)
            output["pred_neutral"] = int(not any_positive)
            output["model_version"] = os.path.basename(os.path.abspath(args.model_dir))
            writer.writerow(output)
    print(f"Scored {len(rows):,} passages -> {args.output}")


def validate(args):
    rows = load_rows(args.annotations)
    errors = validate_training_rows(rows)
    if errors:
        preview = "\n".join(errors[:50])
        raise ValueError(f"Annotation validation failed ({len(errors)} errors):\n{preview}")
    print(f"Validated {len(rows):,} adjudicated annotations across "
          f"{len({row['ticker'] for row in rows})} companies")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validation = subparsers.add_parser("validate")
    validation.add_argument("--annotations", default="derived/annotation_template.csv")
    validation.set_defaults(func=validate)

    training = subparsers.add_parser("train")
    training.add_argument("--annotations", default="derived/annotation_template.csv")
    training.add_argument("--output-dir", default="models/finbert-ai-workforce-v1")
    training.add_argument("--base-model", default=DEFAULT_MODEL)
    training.add_argument("--epochs", type=int, default=4)
    training.add_argument("--batch-size", type=int, default=8)
    training.add_argument("--learning-rate", type=float, default=2e-5)
    training.add_argument("--seed", type=int, default=20260808)
    training.set_defaults(func=train)

    scoring = subparsers.add_parser("score")
    scoring.add_argument("--passages", default="derived/clean_passages.csv")
    scoring.add_argument("--model-dir", default="models/finbert-ai-workforce-v1")
    scoring.add_argument("--output", default="derived/passage_predictions.csv")
    scoring.add_argument("--batch-size", type=int, default=16)
    scoring.set_defaults(func=score)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

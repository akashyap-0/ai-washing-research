"""Aggregate passage predictions into auditable company-period/form scores."""

import argparse
import csv
import os
from collections import defaultdict

import label_schema


def load_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["period_id"], row["form"])].append(row)

    by_period = defaultdict(dict)
    for (period_id, form), members in groups.items():
        prefix = form.lower().replace("-", "")
        base = members[0]
        scores = {
            f"{prefix}_eligible_passages": len(members),
            f"{prefix}_eligible_words": sum(int(row["word_count"]) for row in members),
        }
        for label in label_schema.MODEL_LABELS:
            probabilities = [float(row[f"p_{label}"]) for row in members]
            predictions = [int(row[f"pred_{label}"]) for row in members]
            positive_words = sum(
                int(row["word_count"]) * prediction
                for row, prediction in zip(members, predictions)
            )
            scores[f"{prefix}_{label}_mean_probability"] = sum(probabilities) / len(members)
            scores[f"{prefix}_{label}_passage_share"] = sum(predictions) / len(members)
            scores[f"{prefix}_{label}_positive_passages"] = sum(predictions)
            scores[f"{prefix}_{label}_positive_word_share"] = (
                positive_words / scores[f"{prefix}_eligible_words"]
                if scores[f"{prefix}_eligible_words"] else ""
            )
        neutral = [int(row["pred_neutral"]) for row in members]
        scores[f"{prefix}_neutral_passage_share"] = sum(neutral) / len(members)
        by_period[period_id][form] = (base, scores)

    output = []
    for period_id in sorted(by_period):
        form_groups = by_period[period_id]
        base = next(iter(form_groups.values()))[0]
        row = {
            "period_id": period_id,
            "ticker": base["ticker"],
            "company": base["company"],
            "anchor_10k_filing_date": base["anchor_10k_filing_date"],
            "model_version": base.get("model_version", ""),
            "label_schema_version": label_schema.SCHEMA_VERSION,
        }
        for _form, (_base, scores) in form_groups.items():
            row.update(scores)
        for label in label_schema.PRIMARY_LABELS:
            for metric in ("mean_probability", "passage_share", "positive_word_share"):
                tenk = row.get(f"10k_{label}_{metric}")
                eightk = row.get(f"8k_{label}_{metric}")
                row[f"gap_{label}_{metric}"] = (
                    float(eightk) - float(tenk)
                    if tenk not in (None, "") and eightk not in (None, "") else ""
                )
        output.append(row)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", default="derived/passage_predictions.csv")
    parser.add_argument("--output", default="derived/company_period_text_scores.csv")
    args = parser.parse_args(argv)

    rows = aggregate(load_rows(args.predictions))
    fields = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Aggregated {len(rows):,} company-period rows -> {args.output}")


if __name__ == "__main__":
    main()

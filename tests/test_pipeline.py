import csv
import os
import tempfile
import unittest

import aggregate_company_period as aggregate
import build_passage_dataset as passages
import label_schema
import merge_financial_panel as merger
import run_panel_experiments as experiments
import storage
import finbert_multilabel as classifier


class PassagePipelineTests(unittest.TestCase):
    def test_chunking_is_bounded_and_preserves_text(self):
        sentence = "AI tools improve employee productivity and reduce manual processing time."
        chunks = passages.chunk_text(" ".join([sentence] * 60))
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk.split()) <= passages.MAX_WORDS for chunk in chunks))

    def test_retrieval_is_multi_reason(self):
        reasons = passages.retrieval_reasons(
            "We deployed artificial intelligence to improve employee productivity.")
        self.assertEqual(reasons, ["ai", "workforce", "productivity"])

    def test_8k_anchor_window(self):
        anchors = [{"filing_date": "2023-02-20"}, {"filing_date": "2024-02-20"}]
        anchor, status = passages.match_anchor("2023-07-01", anchors)
        self.assertEqual(status, "matched")
        self.assertEqual(anchor["filing_date"], "2024-02-20")
        anchor, status = passages.match_anchor("2024-04-01", anchors)
        self.assertIsNone(anchor)
        self.assertEqual(status, "after_latest_10k")

    def test_palantir_is_not_approved(self):
        self.assertNotIn("PLTR", passages.APPROVED_TICKERS)

    def test_annotation_neutral_is_derived(self):
        row = {label: "0" for label in label_schema.MODEL_LABELS}
        row.update({"neutral": "1", "risk_type": "not_a_risk",
                    "actuality": "unclear",
                    "specificity": "unclear", "causal_link_strength": "none",
                    "review_status": "adjudicated"})
        self.assertEqual(label_schema.validate_annotation(row), [])
        row["ai_risk"] = "1"
        self.assertIn("neutral must equal 1 only when all substantive labels are 0",
                      label_schema.validate_annotation(row))

    def test_extract_relevant_8k_items(self):
        try:
            import edgar
        except ModuleNotFoundError as error:
            if error.name == "bs4":
                self.skipTest("Beautiful Soup is not installed in this checkout environment")
            raise
        text = ("ITEM 2.05 Costs Associated with Exit Activities\n"
                "The company approved a restructuring plan that will reduce its "
                "workforce and recognize severance expense during the next quarter.\n"
                "ITEM 9.01 Financial Statements and Exhibits\nExhibit 99.1")
        result = edgar.extract_8k_items(text)
        self.assertIn("Item 2.05", result)
        self.assertNotIn("Item 9.01", result)

    def test_aggregate_calculates_directional_gap(self):
        rows = []
        for form, opportunity in (("10-K", 0.2), ("8-K", 0.8)):
            row = {"period_id": "IBM:2024-02-20", "form": form, "ticker": "IBM",
                   "company": "IBM", "anchor_10k_filing_date": "2024-02-20",
                   "word_count": "100", "pred_neutral": "0", "model_version": "v1"}
            for label in label_schema.MODEL_LABELS:
                value = opportunity if label == "ai_opportunity" else 0.1
                row[f"p_{label}"] = str(value)
                row[f"pred_{label}"] = str(int(value >= 0.5))
            rows.append(row)
        result = aggregate.aggregate(rows)[0]
        self.assertAlmostEqual(result["gap_ai_opportunity_mean_probability"], 0.6)

    def test_financial_merge_rejects_duplicate_periods(self):
        with self.assertRaises(ValueError):
            merger.merge([{"period_id": "x"}],
                         [{"period_id": "x"}, {"period_id": "x"}])

    def test_bh_correction_is_monotone_in_rank(self):
        adjusted = experiments.benjamini_hochberg([0.01, 0.04, 0.03])
        self.assertAlmostEqual(adjusted[0], 0.03)
        self.assertAlmostEqual(adjusted[1], 0.04)
        self.assertAlmostEqual(adjusted[2], 0.04)

    def test_dedup_enriches_blank_metadata_without_replacing_text(self):
        with tempfile.TemporaryDirectory() as directory:
            dataset = storage.Dataset(directory)
            original = {"company": "IBM", "ticker": "IBM", "source_type": "10-K",
                        "filing_date": "2024-02-20", "section": "Item 1A Risk Factors",
                        "url": "https://example.test/filing", "text": "original"}
            _, first = dataset.save_document(original)
            enriched = {**original, "cik": "51143", "accession": "abc",
                        "period_end": "2023-12-31", "text": "replacement"}
            _, second = dataset.save_document(enriched)
            saved = dataset.get_all_documents()[0]
            self.assertTrue(first)
            self.assertFalse(second)
            self.assertEqual(saved["cik"], "51143")
            self.assertEqual(saved["text"], "original")

    def test_classifier_rejects_unreviewed_blank_annotations(self):
        errors = classifier.validate_training_rows([
            {"passage_id": "p1", "ticker": "IBM", "review_status": "unreviewed"}
        ])
        self.assertTrue(any("must be 0 or 1" in error for error in errors))
        self.assertTrue(any("adjudicated" in error for error in errors))

    def test_panel_fixed_effect_harness_runs(self):
        try:
            import pandas as pd
            import statsmodels  # noqa: F401
        except ModuleNotFoundError:
            self.skipTest("statsmodels is not installed")
        rows = []
        for firm in range(8):
            for year in range(2019, 2025):
                score = (firm + year - 2019) / 20
                rows.append({
                    "ticker": f"F{firm}", "fiscal_year": year,
                    "industry": "tech" if firm < 4 else "other",
                    "ai_business_role": "infrastructure" if firm < 4 else "adopter",
                    "score": score, "control": firm / 10,
                    "outcome": 0.5 * score + 0.01 * (year - 2019),
                })
        results = experiments.run(pd.DataFrame(rows), ["outcome"], ["score"], ["control"])
        self.assertTrue(any(row["specification"] == "firm_year_fe" for row in results))
        self.assertTrue(all("p_value_bh" in row for row in results))


if __name__ == "__main__":
    unittest.main()

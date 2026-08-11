"""Versioned multi-label schema for the AI/workforce passage classifier.

The field *definitions* live here, not only in RESEARCH_PIPELINE.md, so that
the codebook handed to a human coder and the schema the code validates against
cannot drift apart. `render_codebook()` builds the coder-facing document from
these same constants; regenerate it with `python label_schema.py` rather than
editing the markdown by hand.

Definitions are transcribed from RESEARCH_PIPELINE.md "Annotation schema".
Where that document and this module disagreed, this module wins, because it is
what validate_annotation() enforces: `specificity` and `causal_link_strength`
each carry an extra `unclear` value here that the design document omits.
"""

SCHEMA_VERSION = "1.0.0"

PRIMARY_LABELS = (
    "ai_opportunity",
    "ai_risk",
    "ai_efficiency",
    "ai_workforce_reduction",
)

GUARDRAIL_LABELS = (
    "ai_adoption",
    "ai_worker_augmentation",
    "generic_ai_marketing",
    "explicit_ai_job_link",
)

MODEL_LABELS = PRIMARY_LABELS + GUARDRAIL_LABELS
DERIVED_LABELS = ("neutral",)

# Risk-type taxonomy. This is NOT part of the original AI-washing label design:
# it was specified by Prof. Schloetzer (2026-08-07) to test whether the
# Infrastructure and Power Adopter groups differ in KIND rather than in degree,
# after the severity scalar returned a null. His two clusters were
#   Infrastructure  -> demand, customer concentration, hyperscaler capex cycles,
#                      export controls, inventory and lead times, competitive
#                      obsolescence
#   Power Adopters  -> implementation cost, model reliability in customer-facing
#                      use, workforce disruption, third-party model dependence,
#                      data governance, IP contamination
# and the six named types below are the agreed reduction of those clusters.
# `other` exists so a passage that fits none of the six is recorded as such
# rather than forced into one -- that is the evidence the taxonomy is
# incomplete, and it must not be silently absorbed.
RISK_TYPE_VALUES = (
    "demand",
    "competition",
    "export_controls",
    "implementation",
    "displacement",
    "governance",
    "other",
    "not_a_risk",
    "unclear",
)

ACTUALITY_VALUES = ("realized", "ongoing", "planned", "hypothetical", "unclear")
SPECIFICITY_VALUES = ("quantified", "specific_unquantified", "vague", "unclear")
CAUSAL_LINK_VALUES = ("explicit", "strongly_implied", "co_occurring_only", "none", "unclear")
REVIEW_STATUS_VALUES = ("unreviewed", "coder_1", "coder_2", "adjudicated")

ANNOTATION_FIELDS = (
    "passage_id",
    *MODEL_LABELS,
    "neutral",
    "risk_type",
    "risk_type_secondary",
    "actuality",
    "specificity",
    "causal_link_strength",
    "coder_id",
    "review_status",
    "annotation_notes",
    "label_schema_version",
)

# ---------------------------------------------------------------------------
# Definitions (coder-facing)
# ---------------------------------------------------------------------------

LABEL_DEFINITIONS = {
    "ai_opportunity":
        "AI is presented as a commercial, strategic, growth, or capability "
        "opportunity. Generic praise with no evidence still counts here, but "
        "must also be marked generic_ai_marketing.",
    "ai_risk":
        "AI creates competitive, operational, regulatory, security, "
        "implementation, financial, or workforce risk for the company.",
    "ai_efficiency":
        "AI is claimed or expected to increase output, speed, quality, or "
        "capacity, or to reduce operating cost.",
    "ai_workforce_reduction":
        "AI or automation explicitly or strongly implicitly lowers labor "
        "demand, hiring, headcount, roles, or human work.",
    "ai_adoption":
        "AI has been deployed or is actively in use. Planned exploration "
        "alone does not qualify.",
    "ai_worker_augmentation":
        "AI helps employees perform work while those employees remain part of "
        "the described process.",
    "generic_ai_marketing":
        "Positive AI language with no operational evidence, scale, realized "
        "use, or concrete mechanism.",
    "explicit_ai_job_link":
        "The passage directly connects AI or automation to a layoff, headcount "
        "reduction, reduced hiring, or role elimination.",
    "neutral":
        "DERIVED, do not code by hand. Set to 1 only when all eight "
        "substantive labels are 0.",
}

RISK_TYPE_DEFINITIONS = {
    "demand":
        "Demand for the firm's own AI products or capacity: customer "
        "concentration, hyperscaler capex cycles, order visibility, inventory "
        "and lead times.",
    "competition":
        "Competitive position: being out-innovated, competitive obsolescence, "
        "commoditisation, losing an AI capability race.",
    "export_controls":
        "Export restrictions, sanctions, or geographic licensing limits on AI "
        "hardware, models, or customers.",
    "implementation":
        "Executing on AI internally: implementation cost, integration "
        "difficulty, model reliability in customer-facing use, dependence on "
        "third-party models or vendors.",
    "displacement":
        "Effects on the firm's own workforce: headcount, roles, hiring, "
        "reskilling, workforce disruption.",
    "governance":
        "Data governance, privacy, IP contamination, model bias, and "
        "regulatory compliance such as the EU AI Act.",
    "other":
        "A genuine AI-related risk that fits none of the six above. Please say "
        "what it is in annotation_notes -- these are how we find out the "
        "taxonomy is incomplete.",
    "not_a_risk":
        "The passage is about AI but is not framing a risk, e.g. promotional "
        "or descriptive language.",
    "unclear": "Cannot be judged from the passage.",
}

ACTUALITY_DEFINITIONS = {
    "realized": "Already happened and is described as complete.",
    "ongoing": "Happening now or continuing.",
    "planned": "Committed to, but not yet done.",
    "hypothetical": "Possible, conditional, or forward-looking risk language.",
    "unclear": "The passage does not say.",
}

SPECIFICITY_DEFINITIONS = {
    "quantified": "Attaches a number, magnitude, or measurable quantity.",
    "specific_unquantified":
        "Names a concrete mechanism, product, function, or group, but no "
        "number.",
    "vague": "Neither a number nor a concrete mechanism.",
    "unclear": "Cannot be judged from the passage.",
}

CAUSAL_LINK_DEFINITIONS = {
    "explicit":
        "The passage states the causal link between AI/automation and the "
        "workforce outcome.",
    "strongly_implied":
        "The link is clearly intended although not stated outright.",
    "co_occurring_only":
        "AI and a workforce outcome both appear, with no link asserted. This "
        "is NOT an AI/job link.",
    "none": "No workforce outcome is present at all.",
    "unclear": "Cannot be judged from the passage.",
}

# Rules that decide the cases coders most often disagree on. Each is taken from
# RESEARCH_PIPELINE.md; none is invented here.
DECISION_RULES = (
    "Labels are MULTI-LABEL. A passage may take several at once, e.g. both "
    "ai_efficiency and ai_workforce_reduction. Do not pick just one.",
    "`neutral` is derived, never coded directly. It is 1 only when all eight "
    "substantive labels are 0, so it is not a fifth topic for mixed text.",
    "Co-occurrence is not causation. AI and layoffs appearing in the same "
    "passage is `co_occurring_only`, and is not explicit_ai_job_link.",
    "`explicit_ai_job_link` is deliberately rare and prioritises precision. "
    "When in doubt, leave it 0 and say why in annotation_notes.",
    "Keyword matches that are not about AI do not get AI labels. "
    "'automatic renewal' or 'automatic extension' is not AI content; code the "
    "passage as all-zero (neutral).",
    "Judge only what the passage itself says. Do not use outside knowledge of "
    "what the company actually did.",
    "Use `unclear` rather than guessing, and use annotation_notes for anything "
    "the schema cannot express.",
)

# Illustrative only, and both are already documented elsewhere in this repo, so
# neither is a new adjudication invented for the codebook: the Oracle sentence
# is the citable admission in RESULTS_PACKET.md E.1, and the AMD text is the
# verified `automat*` false positive in H.5.
WORKED_EXAMPLES = (
    {
        "source": "Oracle FY2026 10-K, Item 1A",
        "text": "In addition, the adoption and deployment of AI technologies "
                "across our operations have resulted, and may continue to "
                "result, in reductions to our workforce.",
        "coding": "ai_workforce_reduction=1, explicit_ai_job_link=1, "
                  "ai_adoption=1; actuality=realized "
                  "(\"have resulted\"), specificity=vague (no number), "
                  "causal_link_strength=explicit.",
    },
    {
        "source": "AMD FY2020 10-K, Item 1A",
        "text": "...subject to automatic extension first to January 26, "
                "2022...",
        "coding": "All labels 0, so neutral=1. The only keyword match is "
                  "\"automatic\", which here is a merger-agreement deadline "
                  "and not AI at all.",
    },
)


def check_definitions_cover_schema():
    """Every coded field must have a definition, and vice versa. Returns the
    problems found; empty means the codebook and the validator agree."""
    problems = []
    expected_labels = set(MODEL_LABELS) | set(DERIVED_LABELS)
    missing = expected_labels - set(LABEL_DEFINITIONS)
    extra = set(LABEL_DEFINITIONS) - expected_labels
    problems += [f"label missing a definition: {n}" for n in sorted(missing)]
    problems += [f"definition for unknown label: {n}" for n in sorted(extra)]
    for field, values, defs in (
            ("risk_type", RISK_TYPE_VALUES, RISK_TYPE_DEFINITIONS),
            ("actuality", ACTUALITY_VALUES, ACTUALITY_DEFINITIONS),
            ("specificity", SPECIFICITY_VALUES, SPECIFICITY_DEFINITIONS),
            ("causal_link_strength", CAUSAL_LINK_VALUES,
             CAUSAL_LINK_DEFINITIONS)):
        problems += [f"{field} value missing a definition: {v}"
                     for v in sorted(set(values) - set(defs))]
        problems += [f"{field} definition for unknown value: {v}"
                     for v in sorted(set(defs) - set(values))]
    return problems


def derived_neutral(labels):
    """Return 1 only when every modeled substantive label is false."""
    return int(not any(int(labels.get(label, 0)) for label in MODEL_LABELS))


def validate_annotation(row, require_adjudicated=False):
    """Return human-readable validation errors for one annotation row."""
    errors = []
    for label in MODEL_LABELS:
        if str(row.get(label, "")) not in {"0", "1"}:
            errors.append(f"{label} must be 0 or 1")

    if str(row.get("neutral", "")) in {"0", "1"}:
        expected = derived_neutral(row)
        if int(row["neutral"]) != expected:
            errors.append("neutral must equal 1 only when all substantive labels are 0")
    else:
        errors.append("neutral must be 0 or 1")

    enums = {
        "risk_type": RISK_TYPE_VALUES,
        "actuality": ACTUALITY_VALUES,
        "specificity": SPECIFICITY_VALUES,
        "causal_link_strength": CAUSAL_LINK_VALUES,
        "review_status": REVIEW_STATUS_VALUES,
    }
    for field, allowed in enums.items():
        if row.get(field, "") not in allowed:
            errors.append(f"{field} must be one of: {', '.join(allowed)}")

    # Optional by design: most passages carry one risk type, and forcing a
    # second would manufacture co-occurrence that isn't there.
    secondary = row.get("risk_type_secondary", "")
    if secondary and secondary not in RISK_TYPE_VALUES:
        errors.append("risk_type_secondary must be blank or one of: "
                      + ", ".join(RISK_TYPE_VALUES))
    if secondary and secondary == row.get("risk_type", ""):
        errors.append("risk_type_secondary must differ from risk_type")

    if require_adjudicated and row.get("review_status") != "adjudicated":
        errors.append("training data must be adjudicated")
    return errors


def render_codebook():
    """Build the coder-facing codebook from the constants above.

    Written out as ANNOTATION_CODEBOOK.md by `python label_schema.py`. Do not
    edit that file directly -- it is generated, and hand edits are the way the
    codebook and the validator start disagreeing.
    """
    problems = check_definitions_cover_schema()
    if problems:
        raise ValueError("schema and definitions disagree: "
                         + "; ".join(problems))

    out = [
        "# Annotation codebook",
        "",
        f"AI/workforce passage labelling · schema version {SCHEMA_VERSION}",
        "",
        "Generated from `label_schema.py`. One row per passage. Read the "
        "passage in the `text` column and fill the blank columns to its right; "
        "everything left of them is provenance and is already filled in.",
        "",
        "## How to code a row",
        "",
        "1. Set `risk_type` — this is the one that speaks to whether the two "
        "groups differ in kind. Add `risk_type_secondary` only if a second "
        "type is genuinely present; leave it blank otherwise.",
        "2. Set each of the eight labels below to **1** or **0**.",
        "3. Leave `neutral` blank — it is derived from the eight.",
        "4. Set `actuality`, `specificity`, and `causal_link_strength` to one "
        "of the listed values.",
        "5. Put your initials in `coder_id` and `coder_1` (or `coder_2`) in "
        "`review_status`.",
        "6. Use `annotation_notes` freely for anything ambiguous.",
        "",
        "If you only have time for one field, code `risk_type` and leave the "
        "rest blank. That alone answers the composition question.",
        "",
        "## Rules that settle the hard cases",
        "",
    ]
    out += [f"- {rule}" for rule in DECISION_RULES]

    out += [
        "",
        "## Risk type — `risk_type` (and optional `risk_type_secondary`)",
        "",
        "What KIND of AI risk the passage is about. Pick the one that best "
        "fits; use `risk_type_secondary` only when a second type is clearly "
        "also present.",
        "",
        "| value | meaning |", "|---|---|",
    ]
    out += [f"| `{v}` | {RISK_TYPE_DEFINITIONS[v]} |" for v in RISK_TYPE_VALUES]
    out.append("")

    out += ["", "## Labels (each 0 or 1)", ""]
    out += ["| label | code 1 when |", "|---|---|"]
    for name in PRIMARY_LABELS + GUARDRAIL_LABELS:
        out.append(f"| `{name}` | {LABEL_DEFINITIONS[name]} |")
    out += ["", f"*Derived:* `neutral` — {LABEL_DEFINITIONS['neutral']}", ""]

    for title, field, values, defs in (
            ("Actuality", "actuality", ACTUALITY_VALUES, ACTUALITY_DEFINITIONS),
            ("Specificity", "specificity", SPECIFICITY_VALUES,
             SPECIFICITY_DEFINITIONS),
            ("Causal link strength", "causal_link_strength",
             CAUSAL_LINK_VALUES, CAUSAL_LINK_DEFINITIONS)):
        out += [f"## {title} — `{field}`", "",
                "| value | meaning |", "|---|---|"]
        out += [f"| `{v}` | {defs[v]} |" for v in values]
        out.append("")

    out += ["## Two worked examples", ""]
    for ex in WORKED_EXAMPLES:
        out += [f"**{ex['source']}**", "", f"> {ex['text']}", "",
                f"{ex['coding']}", ""]

    out += [
        "## If a passage should not have been shown to you",
        "",
        "Candidate passages were retrieved by keyword, so some are not about "
        "AI, automation, or the workforce at all. Code these all-zero "
        "(`neutral`) and note why — those judgements are useful, not wasted.",
        "",
    ]
    return "\n".join(out)


if __name__ == "__main__":
    import os
    problems = check_definitions_cover_schema()
    if problems:
        for problem in problems:
            print(f"[error] {problem}")
        raise SystemExit(1)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "ANNOTATION_CODEBOOK.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render_codebook() + "\n")
    print(f"Wrote codebook (schema {SCHEMA_VERSION}) to {path}")

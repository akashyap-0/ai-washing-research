"""Versioned multi-label schema for the AI/workforce passage classifier."""

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

ACTUALITY_VALUES = ("realized", "ongoing", "planned", "hypothetical", "unclear")
SPECIFICITY_VALUES = ("quantified", "specific_unquantified", "vague", "unclear")
CAUSAL_LINK_VALUES = ("explicit", "strongly_implied", "co_occurring_only", "none", "unclear")
REVIEW_STATUS_VALUES = ("unreviewed", "coder_1", "coder_2", "adjudicated")

ANNOTATION_FIELDS = (
    "passage_id",
    *MODEL_LABELS,
    "neutral",
    "actuality",
    "specificity",
    "causal_link_strength",
    "coder_id",
    "review_status",
    "annotation_notes",
    "label_schema_version",
)


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
        "actuality": ACTUALITY_VALUES,
        "specificity": SPECIFICITY_VALUES,
        "causal_link_strength": CAUSAL_LINK_VALUES,
        "review_status": REVIEW_STATUS_VALUES,
    }
    for field, allowed in enums.items():
        if row.get(field, "") not in allowed:
            errors.append(f"{field} must be one of: {', '.join(allowed)}")

    if require_adjudicated and row.get("review_status") != "adjudicated":
        errors.append("training data must be adjudicated")
    return errors

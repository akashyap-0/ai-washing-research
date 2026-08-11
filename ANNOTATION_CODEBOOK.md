# Annotation codebook

AI/workforce passage labelling · schema version 1.0.0

Generated from `label_schema.py`. One row per passage. Read the passage in the `text` column and fill the blank columns to its right; everything left of them is provenance and is already filled in.

## How to code a row

1. Set `risk_type` — this is the one that speaks to whether the two groups differ in kind. Add `risk_type_secondary` only if a second type is genuinely present; leave it blank otherwise.
2. Set each of the eight labels below to **1** or **0**.
3. Leave `neutral` blank — it is derived from the eight.
4. Set `actuality`, `specificity`, and `causal_link_strength` to one of the listed values.
5. Put your initials in `coder_id` and `coder_1` (or `coder_2`) in `review_status`.
6. Use `annotation_notes` freely for anything ambiguous.

If you only have time for one field, code `risk_type` and leave the rest blank. That alone answers the composition question.

## Rules that settle the hard cases

- Labels are MULTI-LABEL. A passage may take several at once, e.g. both ai_efficiency and ai_workforce_reduction. Do not pick just one.
- `neutral` is derived, never coded directly. It is 1 only when all eight substantive labels are 0, so it is not a fifth topic for mixed text.
- Co-occurrence is not causation. AI and layoffs appearing in the same passage is `co_occurring_only`, and is not explicit_ai_job_link.
- `explicit_ai_job_link` is deliberately rare and prioritises precision. When in doubt, leave it 0 and say why in annotation_notes.
- Keyword matches that are not about AI do not get AI labels. 'automatic renewal' or 'automatic extension' is not AI content; code the passage as all-zero (neutral).
- Judge only what the passage itself says. Do not use outside knowledge of what the company actually did.
- Use `unclear` rather than guessing, and use annotation_notes for anything the schema cannot express.

## Risk type — `risk_type` (and optional `risk_type_secondary`)

What KIND of AI risk the passage is about. Pick the one that best fits; use `risk_type_secondary` only when a second type is clearly also present.

| value | meaning |
|---|---|
| `demand` | Demand for the firm's own AI products or capacity: customer concentration, hyperscaler capex cycles, order visibility, inventory and lead times. |
| `competition` | Competitive position: being out-innovated, competitive obsolescence, commoditisation, losing an AI capability race. |
| `export_controls` | Export restrictions, sanctions, or geographic licensing limits on AI hardware, models, or customers. |
| `implementation` | Executing on AI internally: implementation cost, integration difficulty, model reliability in customer-facing use, dependence on third-party models or vendors. |
| `displacement` | Effects on the firm's own workforce: headcount, roles, hiring, reskilling, workforce disruption. |
| `governance` | Data governance, privacy, IP contamination, model bias, and regulatory compliance such as the EU AI Act. |
| `other` | A genuine AI-related risk that fits none of the six above. Please say what it is in annotation_notes -- these are how we find out the taxonomy is incomplete. |
| `not_a_risk` | The passage is about AI but is not framing a risk, e.g. promotional or descriptive language. |
| `unclear` | Cannot be judged from the passage. |


## Labels (each 0 or 1)

| label | code 1 when |
|---|---|
| `ai_opportunity` | AI is presented as a commercial, strategic, growth, or capability opportunity. Generic praise with no evidence still counts here, but must also be marked generic_ai_marketing. |
| `ai_risk` | AI creates competitive, operational, regulatory, security, implementation, financial, or workforce risk for the company. |
| `ai_efficiency` | AI is claimed or expected to increase output, speed, quality, or capacity, or to reduce operating cost. |
| `ai_workforce_reduction` | AI or automation explicitly or strongly implicitly lowers labor demand, hiring, headcount, roles, or human work. |
| `ai_adoption` | AI has been deployed or is actively in use. Planned exploration alone does not qualify. |
| `ai_worker_augmentation` | AI helps employees perform work while those employees remain part of the described process. |
| `generic_ai_marketing` | Positive AI language with no operational evidence, scale, realized use, or concrete mechanism. |
| `explicit_ai_job_link` | The passage directly connects AI or automation to a layoff, headcount reduction, reduced hiring, or role elimination. |

*Derived:* `neutral` — DERIVED, do not code by hand. Set to 1 only when all eight substantive labels are 0.

## Actuality — `actuality`

| value | meaning |
|---|---|
| `realized` | Already happened and is described as complete. |
| `ongoing` | Happening now or continuing. |
| `planned` | Committed to, but not yet done. |
| `hypothetical` | Possible, conditional, or forward-looking risk language. |
| `unclear` | The passage does not say. |

## Specificity — `specificity`

| value | meaning |
|---|---|
| `quantified` | Attaches a number, magnitude, or measurable quantity. |
| `specific_unquantified` | Names a concrete mechanism, product, function, or group, but no number. |
| `vague` | Neither a number nor a concrete mechanism. |
| `unclear` | Cannot be judged from the passage. |

## Causal link strength — `causal_link_strength`

| value | meaning |
|---|---|
| `explicit` | The passage states the causal link between AI/automation and the workforce outcome. |
| `strongly_implied` | The link is clearly intended although not stated outright. |
| `co_occurring_only` | AI and a workforce outcome both appear, with no link asserted. This is NOT an AI/job link. |
| `none` | No workforce outcome is present at all. |
| `unclear` | Cannot be judged from the passage. |

## Two worked examples

**Oracle FY2026 10-K, Item 1A**

> In addition, the adoption and deployment of AI technologies across our operations have resulted, and may continue to result, in reductions to our workforce.

ai_workforce_reduction=1, explicit_ai_job_link=1, ai_adoption=1; actuality=realized ("have resulted"), specificity=vague (no number), causal_link_strength=explicit.

**AMD FY2020 10-K, Item 1A**

> ...subject to automatic extension first to January 26, 2022...

All labels 0, so neutral=1. The only keyword match is "automatic", which here is a merger-agreement deadline and not AI at all.

## If a passage should not have been shown to you

Candidate passages were retrieved by keyword, so some are not about AI, automation, or the workforce at all. Code these all-zero (`neutral`) and note why — those judgements are useful, not wasted.


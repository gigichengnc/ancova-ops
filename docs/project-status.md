# Project Status — ReasonedOps v1.4.3 audit close-out

ReasonedOps is a completed local research/software prototype that originated from my participation in **HKMU Hackathon 2026** and evolved into its current evidence-aware service-operations form.

The v1.4.3 checkpoint exists because an external audit identified several close-out issues worth correcting before the project is frozen:

- residual wording that could still make the project look like a rebuild of somebody else's project;
- reviewer-facing `request intelligence` language that was broader than the actual deterministic rule/keyword baseline;
- a validity suite that tested visible failure conditions but did not execute an unmeasured-confounding false-negative case;
- a provenance mismatch where the preferred citable Zenodo snapshot and the publicly installable PyPI snapshot had different version numbers.

The corrective sequence is:

```text
early Hackathon-stage concept
      ↓
Operate → Audit → Evaluate
      ↓
public package + citation archive
      ↓
external audit
      ↓
identity wording correction
      ↓
rule-based Operate wording correction
      ↓
explicit hidden-confounding blind-spot benchmark
      ↓
v1.4.3 exact-tag release
      ↓
Zenodo v1.4.3 archive + verified DOI
      ↓
PyPI 1.4.3 from the same tag
      ↓
fresh public-package verification
      ↓
freeze v1
```

**Research/portfolio project:** COMPLETED  
**GitHub release/tag:** v1.4.3 — PUBLISHED / VERIFIED  
**Python distribution build:** VERIFIED IN CI  
**Currently published PyPI artifact:** `reasoned-ops==1.4.0`  
**Target aligned PyPI artifact:** `reasoned-ops==1.4.3` FROM EXACT `v1.4.3` TAG  
**External package install check:** VERIFIED FOR 1.4.0; RECHECK 1.4.3 AFTER PUBLICATION  
**Zenodo GitHub integration:** ENABLED FOR `gigichengnc/reasoned-ops`  
**Zenodo v1.4.1 DOI:** `10.5281/zenodo.22044222` — PUBLISHED  
**Zenodo v1.4.2 DOI:** `10.5281/zenodo.22044621` — PUBLISHED  
**Zenodo v1.4.3 DOI:** `10.5281/zenodo.22046490` — PUBLISHED / VERIFIED  
**Concept DOI:** NOT CLAIMED WITHOUT A DISTINCT VERIFIED `Cite all versions` IDENTIFIER  
**Real private-data pilot:** NOT APPROVED  
**Production deployment:** NOT APPROVED

## What is implemented

| Area | Working behaviour |
| --- | --- |
| Request intake | Accepts a text service request through the FastAPI `/v1/route` endpoint. |
| Operate baseline | Uses transparent deterministic rule/keyword features for issue, urgency, communication intensity, complexity and recurrence; it does not claim a trained NLP model. |
| Routing | Returns a department, priority, human-review flag and reasons. |
| Human review | Staff can confirm or override a routing decision. |
| Audit history | Original machine/rule decisions remain stored after a human override. |
| Outcome capture | Response time, resolution time, reassignment, escalation and satisfaction can be stored separately. |
| Management report | Produces raw summaries, adjusted estimates when supportable, diagnostics and interpretation warnings. |
| Comparison gate | Can withhold a department comparison when department and case type are not separately identifiable. |
| Method gate | Returns `use`, `caution`, `reject` or `recommend_alternative`. |
| Known limitation benchmark | Demonstrates a scenario where an omitted confounder is invisible to implemented checks, the gate still returns `use`, and the adjusted contrast reverses the known truth. |
| Offline policy research | Evaluates candidate routing policies on synthetic logged-policy data. |
| Longitudinal research | Benchmarks recurrence/time-to-next-case models on synthetic histories. |
| Governance check | Enforces the repository's synthetic/private-data development policy. |
| Development-history record | Preserves the reconstructed early concept, before/after comparison, concept audit and model decisions for the same project. |
| Python distribution | Builds wheel + source distribution and verifies clean-wheel installation in CI. |
| PyPI publishing | Uses GitHub OIDC Trusted Publishing with no stored long-lived PyPI token. |
| Citation/archive | GitHub `v1.4.3` is archived by Zenodo with verified version DOI `10.5281/zenodo.22046490`. |

## Validity boundary

The benchmark now contains both supported-behaviour and known-limitation scenarios.

```text
known_effect_recovery               supported behaviour
measured_confounding                supported behaviour
no_overlap                          supported refusal
slope_interaction                   supported diagnostic
unmeasured_confounding_blind_spot   known limitation
```

For the final scenario, `PASS` means the benchmark successfully reproduced the false-negative mode. It does **not** mean ReasonedOps detected an unrecorded confounder.

The current evidence therefore supports a narrower claim: ReasonedOps can detect or refuse some problems visible in the recorded design, while observed-data diagnostics cannot certify absence of unmeasured confounding.

## Portfolio narrative

The repository is intentionally presented as a **project-evolution case study**, not as a startup-style product landing page and not as a rebuild of somebody else's project.

Start with:

1. [`../original/README.md`](../original/README.md) — reconstructed early Hackathon-stage version of this project;
2. [`before-vs-after.md`](before-vs-after.md) — early concept vs current project;
3. [`original-concept-audit.md`](original-concept-audit.md) — assumptions preserved/corrected/deferred;
4. [`model-decisions.md`](model-decisions.md) — why methods/models were selected, rejected or deferred;
5. [`../README.md`](../README.md) — runnable overview and portfolio story;
6. [`pypi.md`](pypi.md) — package reuse and Trusted Publishing procedure;
7. [`publication-verification.md`](publication-verification.md) — public artifact verification;
8. [`citation.md`](citation.md) — citation and Zenodo archive workflow.

## Canonical codebase

There is one application namespace:

```text
src/reasoned_ops/
```

Public commands use the `reasoned-` prefix:

```text
reasoned-showcase
reasoned-evaluate
reasoned-validity
reasoned-applicability
reasoned-analyze
reasoned-management-report
reasoned-policy
reasoned-longitudinal
reasoned-governance-check
```

The Python distribution name is `reasoned-ops`; the import namespace is `reasoned_ops`.

## Artifact provenance close-out

Before v1.4.3, the public state was:

```text
PyPI 1.4.0         = installable + externally exercised
Zenodo v1.4.2      = preferred archived citation snapshot
```

The executable core was largely unchanged across those checkpoints, but they were still different artifacts. v1.4.3 closes that provenance gap by using one exact tag as the source for all final public artifacts:

```text
v1.4.3 Git tag
      ↓
GitHub Release v1.4.3
      ↓
Zenodo v1.4.3 archive
      ↓
PyPI reasoned-ops==1.4.3
```

The GitHub tag and Zenodo archive are now complete and verified. The exact v1.4.3 version DOI is `10.5281/zenodo.22046490`.

A post-release DOI-sync commit on `main` records that identifier in current citation metadata without changing the immutable `v1.4.3` tag. The remaining provenance step is to publish PyPI from the **existing tag**, not from the later DOI-sync commit.

## Evidence currently in the repository

Current quantitative development evidence is limited to:

- a small hand-authored routing fixture;
- synthetic outcome data;
- synthetic known-truth validity scenarios;
- a synthetic known-limitation hidden-confounding scenario;
- deterministic applicability rules;
- synthetic logged-policy data;
- synthetic longitudinal histories.

The external PyPI verification demonstrates installability and executable software behaviour; it does not add a real-world outcome evidence class.

There is no representative real-company or real-resident/customer pilot dataset in v1.4.3.

## What this project does not prove

The repository does **not** prove that ReasonedOps:

- improves real service resolution time;
- improves real routing accuracy;
- uses a trained NLP model in the current Operate baseline;
- has ruled out unmeasured confounding;
- causes better staff or department performance;
- is safe to process private resident/customer data;
- is production-ready;
- delivers a measured commercial return on investment.

Those claims require a separate real-data pilot, governance approval and a defensible evaluation design.

## Next evidence gate

After PyPI 1.4.3 publication and fresh-environment verification, v1 should remain frozen unless a new evidence need justifies reopening development.

If ReasonedOps is resumed for a real use case, the next substantive step is not another synthetic model. It is a controlled real-data evidence process with privacy/governance approval, representative cases, predefined evaluation questions and explicit stop criteria.

## Project origin

ReasonedOps is the same project that originated from my participation in **HKMU Hackathon 2026**. It was originally developed under the name **ANCOVA Ops** and later renamed **ReasonedOps** because ANCOVA/regression is only one method inside the Evaluate layer, not the project itself.

The Hackathon name is included only as a factual origin reference; ReasonedOps is independently developed and is not presented as an official HKMU product or endorsement.

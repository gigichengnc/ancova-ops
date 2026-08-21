# Project Status — ReasonedOps v1.4.3 frozen v1 checkpoint

ReasonedOps is a completed research/software prototype that originated from my participation in **HKMU Hackathon 2026** and evolved into its current evidence-aware service-operations form.

The v1.4.3 checkpoint exists because an external audit identified several close-out issues worth correcting before the project was frozen:

- residual wording that could still make the project look like a rebuild of somebody else's project;
- reviewer-facing `request intelligence` language that was broader than the actual deterministic rule/keyword baseline;
- a validity suite that tested visible failure conditions but did not execute an unmeasured-confounding false-negative case;
- a provenance mismatch where the preferred citable Zenodo snapshot and the publicly installable PyPI snapshot had different version numbers.

The corrective sequence is complete:

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
FREEZE v1
```

**Research/portfolio project:** COMPLETED / FROZEN V1  
**GitHub release/tag:** v1.4.3 — PUBLISHED / VERIFIED  
**Release commit:** `461b5fc81c2b31fc5fcc51c585004d059bb85586`  
**Python distribution build:** VERIFIED IN CI  
**Public PyPI artifact:** `reasoned-ops==1.4.3` — PUBLISHED / EXTERNALLY VERIFIED  
**External package install check:** VERIFIED FOR 1.4.3 ON WINDOWS  
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
| Final public verification | PyPI `reasoned-ops==1.4.3` installs outside the repository; version, five-scenario validity and routing smoke checks were observed successfully. |

## Validity boundary

The benchmark contains both supported-behaviour and known-limitation scenarios.

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

The executable core was largely unchanged across those checkpoints, but they were still different artifacts. v1.4.3 closes that provenance gap by using one exact tag as the source for the final public software artifacts:

```text
v1.4.3 Git tag
      ↓
GitHub Release v1.4.3
      ↓
release commit 461b5fc81c2b31fc5fcc51c585004d059bb85586
      ↓
Zenodo v1.4.3 archive
DOI 10.5281/zenodo.22046490
      ↓
PyPI reasoned-ops==1.4.3
      ↓
fresh Windows install / version / validity / routing verification
```

The immutable tag, GitHub release, Zenodo snapshot and PyPI package are now aligned at version 1.4.3. A later documentation-only DOI-sync commit on `main` records citation metadata without changing the released tag.

Published PyPI distribution digests recorded by the exact-tag workflow are:

```text
wheel SHA-256  677c3c5f853fc692cbecf5afd1689480a291a08bd003a6b18900482e67123bd3
sdist SHA-256  4cffc44a7dce89366de9e65592c07b78e811fabc038071f990cfa706b1415b08
```

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

## Freeze condition — satisfied

ReasonedOps v1 is now frozen at the completed v1.4.3 software checkpoint.

Further substantive work should require a real partner, representative dataset, competition requirement or a genuinely new evidence question. If that occurs, it should be treated as a separate **Phase 2 — real-world pilot** rather than feature accumulation inside v1.

If ReasonedOps is resumed for a real use case, the next substantive step is not another synthetic model. It is a controlled real-data evidence process with privacy/governance approval, representative cases, predefined evaluation questions and explicit stop criteria.

## Project origin

ReasonedOps is the same project that originated from my participation in **HKMU Hackathon 2026**. It was originally developed under the name **ANCOVA Ops** and later renamed **ReasonedOps** because ANCOVA/regression is only one method inside the Evaluate layer, not the project itself.

The Hackathon name is included only as a factual origin reference; ReasonedOps is independently developed and is not presented as an official HKMU product or endorsement.

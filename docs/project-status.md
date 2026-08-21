# Project Status — ReasonedOps v1.4.2

ReasonedOps is a completed local research/software prototype that originated from my participation in **HKMU Hackathon 2026** and evolved into its current evidence-aware service-operations form.

The current project story is:

```text
early Hackathon-stage concept
      ↓
audit assumptions
      ↓
evolve into Operate → Audit → Evaluate
      ↓
validate software behaviour with public development evidence
      ↓
package the reusable Python implementation
      ↓
publish and verify the public PyPI artifact
      ↓
archive a post-enablement release through Zenodo
      ↓
record the stable Zenodo concept DOI
      ↓
define the next real evidence gate
```

**Research/portfolio project:** COMPLETED  
**Current GitHub/citation checkpoint:** v1.4.2  
**Python distribution build:** VERIFIED  
**PyPI publication:** PUBLISHED — `reasoned-ops==1.4.0`  
**External package install check:** VERIFIED FROM PUBLIC PYPI ARTIFACT  
**Zenodo GitHub integration:** ENABLED FOR `gigichengnc/reasoned-ops`  
**Zenodo concept DOI:** `10.5281/zenodo.22044621` — VISIBLE IN THE ZENODO GITHUB INTEGRATION  
**Version-specific v1.4.2 DOI:** NOT YET RECORDED IN THIS REPOSITORY  
**Real private-data pilot:** NOT APPROVED  
**Production deployment:** NOT APPROVED

## What is implemented

| Area | Working behaviour |
| --- | --- |
| Request intake | Accepts a text service request through the FastAPI `/v1/route` endpoint. |
| Request intelligence | Extracts transparent development-stage issue, urgency, communication-intensity and complexity signals. |
| Routing | Returns a department, priority, human-review flag and reasons. |
| Human review | Staff can confirm or override a routing decision. |
| Audit history | Original machine/rule decisions remain stored after a human override. |
| Outcome capture | Response time, resolution time, reassignment, escalation and satisfaction can be stored separately. |
| Management report | Produces raw summaries, adjusted estimates when supportable, diagnostics and interpretation warnings. |
| Comparison gate | Can withhold a department comparison when department and case type are not separately identifiable. |
| Method gate | Returns `use`, `caution`, `reject` or `recommend_alternative`. |
| Offline policy research | Evaluates candidate routing policies on synthetic logged-policy data. |
| Longitudinal research | Benchmarks recurrence/time-to-next-case models on synthetic histories. |
| Governance check | Enforces the repository's synthetic/private-data development policy. |
| Development-history record | Preserves the reconstructed early concept, before/after comparison, concept audit and model decisions for the same project. |
| Python distribution | Builds wheel + source distribution and verifies clean-wheel installation in CI. |
| PyPI publishing | Published through GitHub OIDC Trusted Publishing with no stored long-lived PyPI token. |
| Public artifact verification | `reasoned-ops==1.4.0` installed from PyPI in a Windows environment outside the repository checkout; Operate → Audit → Evaluate paths were exercised successfully. |
| Citation/archive | `CITATION.cff` is aligned to v1.4.2 and records the stable Zenodo concept DOI for the archived project lineage. |

## Portfolio narrative

The repository is intentionally presented as a **project-evolution case study**, not as a startup-style product landing page and not as a rebuild of somebody else's project.

Start with:

1. [`../original/README.md`](../original/README.md) — reconstructed early Hackathon-stage version of this project;
2. [`before-vs-after.md`](before-vs-after.md) — early concept vs current project;
3. [`original-concept-audit.md`](original-concept-audit.md) — assumptions preserved/corrected/deferred;
4. [`model-decisions.md`](model-decisions.md) — why methods/models were selected, rejected or deferred;
5. [`../README.md`](../README.md) — runnable overview and portfolio story;
6. [`pypi.md`](pypi.md) — package reuse and Trusted Publishing procedure;
7. [`publication-verification.md`](publication-verification.md) — public PyPI install and executable workflow verification;
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

The Python distribution name is:

```text
reasoned-ops
```

The import namespace is:

```python
import reasoned_ops
```

## Distribution and publication status

CI separately validates the packaged artifact rather than assuming an editable source install proves distribution quality.

The distribution job builds a wheel and source distribution, installs the wheel into a clean virtual environment, and checks import, routing behaviour and a packaged CLI entry point.

The public PyPI release `reasoned-ops==1.4.0` was then installed in a Windows environment outside the repository checkout. The verification exercised:

```text
PyPI install + version import
      ↓
Operate: routing + explanation + FastAPI
      ↓
Audit: persisted machine decision + human override + outcome
      ↓
Evaluate: deterministic synthetic validity benchmark
```

See [`publication-verification.md`](publication-verification.md) for the exact boundary and observed checks.

This establishes package distribution and executable local behaviour from the public artifact. It is not independent scientific validation.

The v1.4.2 checkpoint is separate: it is a citation/wording correction release prepared for the current Zenodo archive path. It does not imply that `reasoned-ops==1.4.2` has been published on PyPI.

The Zenodo GitHub integration now exposes the stable concept DOI `10.5281/zenodo.22044621` for the ReasonedOps archive lineage. The concept DOI identifies the collection across archived versions; it should not be misrepresented as the version-specific DOI for the v1.4.2 snapshot unless that individual record is separately verified.

## Evaluation boundary

ReasonedOps does not assume every operational comparison is valid.

For a question such as:

```text
Is Department A slower than Department B?
```

it first asks whether the observed case mix allows those departments to be compared. If department and case type cannot be separated, adjusted department estimates and ranking language are withheld.

When the comparison is supportable, the current continuous-outcome workflow can use regression/ANCOVA-style adjustment with diagnostics and uncertainty reporting. ANCOVA is one method inside Evaluate, not the product itself.

Other question types can be redirected to a more appropriate method family rather than forced through the same model.

## Evidence currently in the repository

Current quantitative development evidence is limited to:

- a small hand-authored routing fixture;
- synthetic outcome data;
- synthetic known-truth validity scenarios;
- deterministic applicability rules;
- synthetic logged-policy data;
- synthetic longitudinal histories.

The external PyPI verification demonstrates installability and executable software behaviour; it does not add a real-world outcome evidence class.

There is no representative real-company or real-resident/customer pilot dataset in v1.4.2.

## What this project does not prove

The repository does **not** prove that ReasonedOps:

- improves real service resolution time;
- improves real routing accuracy;
- causes better staff or department performance;
- is safe to process private resident/customer data;
- is production-ready;
- delivers a measured commercial return on investment.

Those claims require a separate real-data pilot, governance approval and a defensible evaluation design.

Publishing and verifying the package on PyPI, or archiving a release in Zenodo, does not change these evidence boundaries.

## Next evidence gate

The research/portfolio project is complete. If ReasonedOps is ever resumed for a real use case, the next substantive step is not another synthetic model. It is a controlled real-data evidence process with privacy/governance approval, representative cases, predefined evaluation questions and explicit stop criteria.

## Project origin

ReasonedOps is the same project that originated from my participation in **HKMU Hackathon 2026**. It was originally developed under the name **ANCOVA Ops** and later renamed **ReasonedOps** because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.

The Hackathon name is included only as a factual origin reference; ReasonedOps is independently developed and is not presented as an official HKMU product or endorsement.

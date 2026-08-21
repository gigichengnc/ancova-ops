# Release Readiness — ReasonedOps v1.4.0

ReasonedOps v1.4.0 is a **completed local research/software prototype and portfolio rebuild case study** with a validated Python distribution build. That is different from being approved for a real private-data pilot or production deployment.

## What is ready now

- [x] `reasoned_ops` is the single canonical Python package.
- [x] public CLI commands use the `reasoned-` prefix.
- [x] FastAPI routing can accept and persist a service request.
- [x] human routing reviews can confirm or override a recommendation without erasing the original decision.
- [x] outcomes are stored separately from routing decisions.
- [x] management reports separate raw summaries from adjusted evidence.
- [x] department × case-type overlap and identifiability are checked before adjusted ranking.
- [x] unsupported comparisons can be withheld instead of converted into a league table.
- [x] the applicability gate returns `use`, `caution`, `reject` or `recommend_alternative`.
- [x] binary, censored/time-to-event, clustered, routing-policy and causal-intent questions can be redirected instead of being forced through ordinary ANCOVA/regression.
- [x] known-effect recovery, measured-confounding adjustment, no-overlap refusal and slope-interaction behaviour are tested on synthetic scenarios.
- [x] Python 3.11 and 3.12 CI covers lint, tests and the main CLI workflows.
- [x] CI separately builds a wheel and source distribution and smoke-tests installation from the wheel.
- [x] Apache-2.0 licensing and `CITATION.cff` are present.
- [x] the original Hackathon concept is reconstructed separately under `original/`.
- [x] a before/after comparison explains how and why the project changed.
- [x] the original concept audit distinguishes useful ideas from corrected or unsupported assumptions.
- [x] major model/method decisions are recorded, including explicit decisions not to escalate complexity.

## Portfolio/rebuild readiness

The reviewer path is intentionally narrative:

```text
original concept
      ↓
before / after
      ↓
concept audit
      ↓
model decisions
      ↓
runnable current implementation
      ↓
evidence boundary
      ↓
next real evidence gate
```

This structure makes the project learning history visible instead of presenting the final code as if it appeared fully formed.

## Python distribution readiness

The v1.4.0 distribution path is intentionally separate from the ordinary editable development install.

CI now verifies:

```text
pyproject metadata
      ↓
python -m build
      ↓
wheel + source distribution
      ↓
clean virtual environment
      ↓
install built wheel
      ↓
import reasoned_ops
      ↓
routing + packaged CLI smoke checks
```

A dedicated `.github/workflows/publish-pypi.yml` workflow is present for PyPI Trusted Publishing using GitHub OIDC. The first upload is manually dispatched so publication is not attempted before the repository owner configures the matching PyPI Trusted Publisher.

**PyPI code/workflow readiness: READY.**  
**PyPI account-side publisher registration: PENDING until completed by the repository owner.**  
**PyPI upload: NOT YET CLAIMED AS COMPLETE until the package page and clean install are verified.**

See `docs/pypi.md` for the exact publisher identity and verification procedure.

## What is not ready

### Real private-data pilot

A real pilot still requires, at minimum:

- jurisdiction-specific privacy/legal review;
- documented purpose and data-use basis;
- notice/consent design where required;
- retention and deletion schedule;
- pseudonymisation/identity-linkage design;
- authenticated staff identities and RBAC;
- secure storage and secrets management;
- correction/deletion procedures;
- incident/breach response;
- external model/provider data-processing review where relevant;
- real-data annotation and outcome-quality protocol;
- pilot monitoring and stop criteria.

**Pilot status: NOT READY / NOT APPROVED.**

### Production deployment

Production additionally requires representative real-data validation, deployment architecture, authenticated APIs, observability, backups/recovery, security testing, change control, rollback/fallback procedures and operational acceptance criteria.

**Production status: NOT READY / NOT APPROVED.**

## Claims supported by the current repository

Reasonable:

> ReasonedOps is a runnable evidence-aware service-operations research prototype rebuilt from an HKMU Hackathon concierge concept. It can route requests, preserve machine and human decision history, record outcomes, and refuse or redirect unsupported analytical comparisons.

> The repository documents how the original concept was audited and technically corrected.

> The Python project can be built as a wheel/source distribution and installed from the built wheel in a clean environment.

Not supported without new evidence:

> ReasonedOps improves real service performance.

> ANCOVA proves that one department performs better than another.

> Passing CI or publishing to PyPI means the software is safe for real private data or production deployment.

## Citation/archive and package-index status

Repository-side citation and distribution metadata are ready. External publication steps are separate:

- [ ] connect the repository owner account to Zenodo;
- [ ] archive a release and verify the DOI;
- [ ] add the verified DOI back to `CITATION.cff`;
- [ ] register the `reasoned-ops` PyPI Trusted Publisher using `.github/workflows/publish-pypi.yml` and environment `pypi`;
- [ ] manually publish a released tag through the trusted workflow;
- [ ] verify `pip install reasoned-ops==<version>` from a clean environment.

A DOI or PyPI publication improves distribution and citation. It does not create real-world validation.

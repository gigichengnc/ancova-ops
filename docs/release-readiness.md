# Release Readiness — ReasonedOps v1.4.0

ReasonedOps v1.4.0 is a **completed local research/software prototype and portfolio rebuild case study** with a validated and publicly published Python distribution. That is different from being approved for a real private-data pilot or production deployment.

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
- [x] `reasoned-ops==1.4.0` is published on PyPI through GitHub OIDC Trusted Publishing.
- [x] the public PyPI artifact has been installed and exercised outside the repository checkout.
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
public package verification
      ↓
evidence boundary
      ↓
next real evidence gate
```

This structure makes the project learning history visible instead of presenting the final code as if it appeared fully formed.

## Python distribution and PyPI status

The v1.4.0 distribution path is intentionally separate from the ordinary editable development install.

CI verifies:

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

A dedicated `.github/workflows/publish-pypi.yml` workflow publishes through PyPI Trusted Publishing using GitHub OIDC rather than a stored long-lived API token.

`reasoned-ops==1.4.0` was successfully published through that workflow. The public artifact was then installed in a Windows environment outside the repository checkout and used to exercise:

```text
Operate
routing + FastAPI
      ↓
Audit
machine decision + human override + outcome persistence
      ↓
Evaluate
known-truth validity benchmark
```

**PyPI code/workflow readiness: COMPLETE.**  
**PyPI publication: COMPLETE for v1.4.0.**  
**Public artifact install/execution check: COMPLETE.**

See `docs/pypi.md` for reuse and publishing details and `docs/publication-verification.md` for the verification record.

The verification demonstrates package distribution and executable local behaviour. It is not independent scientific validation.

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

> ReasonedOps is publicly distributed on PyPI as `reasoned-ops==1.4.0`; the released artifact has been installed and its local Operate → Audit → Evaluate workflow exercised outside the repository checkout.

Not supported without new evidence:

> ReasonedOps improves real service performance.

> ANCOVA proves that one department performs better than another.

> Passing CI or publishing to PyPI means the software is safe for real private data or production deployment.

## Citation/archive and package-index status

Package-index publication is complete for v1.4.0. Repository-side citation metadata is ready; archival publication remains separate:

- [x] register the `reasoned-ops` PyPI Trusted Publisher;
- [x] publish `reasoned-ops==1.4.0` through the trusted workflow;
- [x] verify the public package in an environment outside the repository checkout;
- [ ] connect the repository owner account to Zenodo;
- [ ] enable `reasoned-ops` for GitHub release archiving;
- [ ] create a new post-enablement release for Zenodo ingestion;
- [ ] verify the Zenodo DOI;
- [ ] add the verified DOI back to `CITATION.cff`.

A DOI or PyPI publication improves distribution and citation. It does not create real-world validation.

# Release Readiness — ReasonedOps v1.4.4

**Release status: COMPLETE. v1 is frozen at 1.4.4.**

v1.4.4 is a narrow post-audit bugfix release. It does not add a trained NLP model, production authentication, new statistical model families, real-data evidence or deployment approval.

## Code checkpoint

- [x] package and runtime version are `1.4.4`;
- [x] request matching uses word/phrase boundaries rather than raw substring matching;
- [x] emergency language enters an explicit human-triage path;
- [x] integrated API emergency routing assigns critical priority and human review;
- [x] safety context and explicit security incidents require human review;
- [x] `current` / `feedback` negative controls are covered by regression tests;
- [x] standalone applicability CLI defaults to `not_assessed` and cannot self-clear `use` from caller-declared supported overlap;
- [x] data-derived applicability still uses `assess_from_ancova_report()`;
- [x] VIF diagnostics are limited to declared numeric covariates;
- [x] hand-authored routing fixture is version 2 and remains labelled design expectation rather than ground truth;
- [x] release workflow is manual-only;
- [x] CI no longer targets the historical `phase-0-foundation` branch;
- [x] Python 3.11, Python 3.12 and distribution CI pass for the hardening checkpoint.

## Public release checklist

- [x] merge the v1.4.4 release-prep documentation after CI;
- [x] manually dispatch the **Release checkpoint** workflow and create Git tag / GitHub Release `v1.4.4`;
- [x] verify Zenodo ingests exactly `v1.4.4`;
- [x] verify immutable v1.4.4 version DOI: `10.5281/zenodo.22051819`;
- [x] sync the verified v1.4.4 DOI to current citation metadata without changing the immutable tag;
- [x] manually publish PyPI from input tag exactly `v1.4.4`;
- [x] verify PyPI reports `reasoned-ops==1.4.4`;
- [x] verify workflow checkout is exact tag `v1.4.4` and package version is `1.4.4`;
- [x] record published wheel / sdist hashes and Trusted Publishing attestations;
- [x] install 1.4.4 in a fresh Windows environment and verify `reasoned_ops.__version__ == "1.4.4"`;
- [x] rerun the five-scenario validity benchmark with `Overall pass: True`;
- [x] run external routing smoke checks for normal maintenance, emergency human review and substring negative controls;
- [x] confirm the integrated FastAPI emergency regression path returns critical priority;
- [x] record the observed v1.4.4 results in `publication-verification.md`;
- [x] freeze v1 again.

Final public-artifact state:

```text
GitHub release: v1.4.4
Release commit: 9b2724354f43a5ed03fca6f3998f88be8c2bb513
Zenodo:        v1.4.4 — 10.5281/zenodo.22051819
PyPI:          reasoned-ops==1.4.4
External check: Windows version / validity / routing smoke passed
Status:         COMPLETED / FROZEN V1
```

## Evidence / deployment boundary

Passing the release checklist establishes artifact provenance and executable behaviour; it does not establish real-world routing accuracy, service improvement, causal effects, absence of unmeasured confounding, private-data approval or production readiness.

Real private-data pilot status: **NOT APPROVED**.  
Production deployment status: **NOT APPROVED**.

# Release Readiness — ReasonedOps v1.4.4

v1.4.4 is a narrow post-audit bugfix release. It does not add a trained NLP model, production authentication, new statistical model families, real-data evidence or deployment approval.

## Code checkpoint

- [x] package and runtime version are `1.4.4`;
- [x] `CITATION.cff` is `1.4.4` and does not reuse the v1.4.3 DOI;
- [x] request matching uses word/phrase boundaries rather than raw substring matching;
- [x] emergency language enters a critical human-triage path;
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

- [ ] merge the v1.4.4 release-prep documentation after CI;
- [ ] manually dispatch the **Release checkpoint** workflow on the final `main` commit; the workflow creates Git tag / GitHub Release `v1.4.4` targeting that commit;
- [ ] verify Zenodo ingests exactly `v1.4.4` and record the new immutable version DOI;
- [ ] sync the verified v1.4.4 DOI to current citation metadata without changing the immutable tag;
- [ ] manually publish PyPI from input tag exactly `v1.4.4`;
- [ ] verify PyPI reports `reasoned-ops==1.4.4`;
- [ ] install 1.4.4 in a fresh environment and verify `reasoned_ops.__version__ == "1.4.4"`;
- [ ] rerun the five-scenario validity benchmark;
- [ ] run routing smoke checks covering a normal maintenance request plus emergency/safety negative-control cases;
- [ ] record the observed v1.4.4 results in `publication-verification.md`;
- [ ] freeze v1 again.

Until those publication steps are complete, **v1.4.3 remains the latest externally verified public artifact**:

```text
GitHub / Zenodo / PyPI: v1.4.3
Zenodo DOI: 10.5281/zenodo.22046490
```

## Evidence / deployment boundary

The current evidence remains synthetic or hand-authored development evidence. Passing the release checklist establishes artifact provenance and executable behaviour; it does not establish real-world routing accuracy, service improvement, causal effects, absence of unmeasured confounding, private-data approval or production readiness.

Real private-data pilot status: **NOT APPROVED**.  
Production deployment status: **NOT APPROVED**.

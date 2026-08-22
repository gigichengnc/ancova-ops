# Project Status — ReasonedOps v1.4.4

**Status: COMPLETED / FROZEN V1**

ReasonedOps is a local research/software prototype organised around **Operate → Audit → Evaluate**. It originated from the author's participation in HKMU Hackathon 2026 and does not claim to be an official HKMU product.

## Current status

| Item | Status |
| --- | --- |
| Frozen v1 checkpoint | **v1.4.4** |
| GitHub release | **v1.4.4 published** |
| Zenodo archive | **v1.4.4 published — `10.5281/zenodo.22051819`** |
| PyPI artifact | **`reasoned-ops==1.4.4` published from exact tag** |
| Fresh external verification | **Windows install / version / validity / routing checks passed** |
| Python 3.11 / 3.12 CI | **Passing** |
| Real private-data pilot | **Not approved** |
| Production deployment | **Not approved** |

v1.4.4 is a narrow bugfix checkpoint opened after an additional adversarial review found reproducible issues in the public v1.4.3 implementation. It is not a new product phase.

## What v1.4.4 fixed

- Operate uses word/phrase-boundary matching rather than raw substring matching, preventing false matches such as `rent` inside `current` and `fee` inside `feedback`.
- Emergency language enters an explicit human-triage path; the integrated API path assigns emergency cases critical priority.
- Non-emergency safety context and explicit security incidents require human review.
- The standalone applicability CLI cannot obtain `use` solely from a caller-declared `supported` overlap status; observed-data clearance is derived from an actual analysis report.
- VIF diagnostics are restricted to declared numeric covariates rather than categorical dummy columns.
- Release creation is manual-only so a green documentation commit does not imply a new software release.

## Evidence boundary

Current quantitative evidence is synthetic or hand-authored development evidence. The routing fixture is a small design benchmark, not an external accuracy estimate. The repository does not establish real-world service improvement, causal effects, absence of unmeasured confounding, private-data approval, production readiness or commercial ROI.

## Final public-artifact provenance

```text
Git tag v1.4.4
      ↓
GitHub Release v1.4.4
      ↓
release commit 9b2724354f43a5ed03fca6f3998f88be8c2bb513
      ↓
Zenodo DOI 10.5281/zenodo.22051819
      ↓
PyPI reasoned-ops==1.4.4
      ↓
fresh Windows install / version / validity / routing verification
```

The immutable `v1.4.4` tag remains the source of the GitHub release, Zenodo archive and PyPI build. Later citation / verification commits on `main` do not rewrite that release snapshot.

## Freeze rule

v1 is frozen after this close-out. Further synthetic feature accumulation, new NLP/ML models, or additional statistical families should not be added merely to expand the repository.

A substantive next phase should begin only when there is a concrete real-world evidence question, representative cases, privacy/governance approval, predefined evaluation criteria and explicit stop conditions.

# Project Status — ReasonedOps v1.4.4

ReasonedOps is a local research/software prototype organised around **Operate → Audit → Evaluate**. It originated from the author's participation in HKMU Hackathon 2026 and does not claim to be an official HKMU product.

## Current status

| Item | Status |
| --- | --- |
| Package/runtime checkpoint | `1.4.4` |
| GitHub release | **v1.4.4 published** |
| Zenodo archive | **v1.4.4 published — `10.5281/zenodo.22051819`** |
| Latest verified public PyPI artifact | `reasoned-ops==1.4.3` |
| PyPI v1.4.4 | **Pending exact-tag publication** |
| Python 3.11 / 3.12 CI | Passing on the v1.4.4 hardening checkpoint |
| Real private-data pilot | **Not approved** |
| Production deployment | **Not approved** |

v1.4.4 is a bugfix checkpoint opened after an additional adversarial review found reproducible issues in the public v1.4.3 implementation. It is not a new product phase.

## What v1.4.4 fixes

- Operate uses word/phrase-boundary matching rather than raw substring matching, preventing false matches such as `rent` inside `current` and `fee` inside `feedback`.
- Emergency language enters an explicit critical human-triage path.
- Non-emergency safety context and explicit security incidents require human review.
- The standalone applicability CLI cannot obtain `use` solely from a caller-declared `supported` overlap status; observed-data clearance is derived from an actual analysis report.
- VIF diagnostics are restricted to the declared numeric covariates rather than categorical dummy columns.
- Release creation is manual-only so a green documentation commit does not imply a new scientific/software release.

## Evidence boundary

Current quantitative evidence is synthetic or hand-authored development evidence. The routing fixture is a small design benchmark, not an external accuracy estimate. The repository does not establish real-world service improvement, causal effects, absence of unmeasured confounding, private-data approval, production readiness or commercial ROI.

## Public-artifact provenance

The v1.4.4 chain is currently:

```text
Git tag v1.4.4
      ↓
GitHub Release v1.4.4
      ↓
Zenodo DOI 10.5281/zenodo.22051819
      ↓
PyPI reasoned-ops==1.4.4       PENDING
      ↓
fresh Windows verification     PENDING
```

The immutable `v1.4.4` tag remains the required source for PyPI publication. The later DOI-sync commit only updates current citation metadata and does not alter the archived release snapshot.

## Next gate

Publish PyPI from exact tag `v1.4.4`, install that public artifact in a fresh environment, rerun the five-scenario validity benchmark and routing smoke checks, record the observed results, then freeze v1 again.

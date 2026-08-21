# Project Status — ReasonedOps v1.4.4 release candidate

ReasonedOps is a local research/software prototype organised around **Operate → Audit → Evaluate**. It originated from the author's participation in HKMU Hackathon 2026 and does not claim to be an official HKMU product.

## Current status

| Item | Status |
| --- | --- |
| Package/runtime checkpoint | `1.4.4` |
| Latest verified public PyPI artifact | `reasoned-ops==1.4.3` |
| Latest verified Zenodo archive | v1.4.3 — `10.5281/zenodo.22046490` |
| v1.4.4 GitHub release / DOI / PyPI | **Pending** |
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

## What is implemented

Operate accepts a service request through FastAPI and returns deterministic rule-based features, routing, priority, human-review status and a rule trace. Audit stores the original case, machine/rule decision, human confirmation or override, effective route and outcome separately. Evaluate checks comparison support and method applicability before reporting adjusted evidence; unsupported comparisons can be withheld.

The validity benchmark includes four supported-behaviour/refusal scenarios plus `unmeasured_confounding_blind_spot`, a known-limitation scenario where observed checks can pass while an omitted confounder makes the adjusted result materially wrong. `PASS` for that scenario means the failure mode was successfully reproduced, not detected or solved.

## Evidence boundary

Current quantitative evidence is synthetic or hand-authored development evidence. The routing fixture is a small design benchmark, not an external accuracy estimate. The repository does not establish real-world service improvement, causal effects, absence of unmeasured confounding, private-data approval, production readiness or commercial ROI.

## Public-artifact provenance

v1.4.3 remains the last completed public chain:

```text
Git tag v1.4.3
      ↓
GitHub Release v1.4.3
      ↓
Zenodo DOI 10.5281/zenodo.22046490
      ↓
PyPI reasoned-ops==1.4.3
      ↓
fresh Windows verification
```

v1.4.4 should replace it as the frozen checkpoint only after the same sequence is completed from the exact `v1.4.4` tag. The release-candidate `CITATION.cff` therefore does not reuse the v1.4.3 DOI.

## Next gate

After v1.4.4 exact-tag GitHub/Zenodo/PyPI alignment and a fresh external install check, v1 should be frozen again. Any later substantive phase should require a concrete real-world evidence question, representative cases and privacy/governance approval rather than more synthetic feature accumulation.

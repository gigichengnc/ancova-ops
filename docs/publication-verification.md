# Public package verification — ReasonedOps

This document separates **observed public-artifact verification** from the final v1.4.3 alignment work.

## Verified historical public artifact: 1.4.0

ReasonedOps 1.4.0 was published as the public PyPI distribution **`reasoned-ops`** and then installed from PyPI in a Windows environment outside the repository checkout.

Observed installed version:

```text
1.4.0
```

The verification exercised the public package through:

```text
Operate
request → rule-based route → explanation
        ↓
Audit
machine decision → human override → persisted history → outcome
        ↓
Evaluate
known-effect recovery → measured-confounding adjustment → no-overlap refusal → interaction detection
```

Observed Operate behaviour for the recurring air-conditioning example included:

```text
Department: maintenance
Priority: high
Human review: True
```

The installed FastAPI application started through:

```powershell
python -m uvicorn reasoned_ops.api:app --reload
```

A persisted case retained the original machine recommendation after a human override to `community_management`, and outcome data was stored separately.

The installed `reasoned-validity` command reported the original four deterministic scenarios as passing:

```text
Overall pass: True
- known_effect_recovery: PASS
- measured_confounding: PASS
- no_overlap: PASS
- slope_interaction: PASS
```

This is a historical verification record for the exact public artifact `reasoned-ops==1.4.0`. It remains valid and should not be rewritten as if those observations had already been made against 1.4.3.

## What changed after 1.4.0

The final audit-closeout work adds or tightens:

- project-origin wording so current-facing docs describe the same project evolving from HKMU Hackathon 2026 rather than an external rebuild;
- reviewer-facing Operate wording so the deterministic rule/keyword baseline is not mistaken for a trained NLP model;
- `reasoned-validity-v2`, including `unmeasured_confounding_blind_spot`;
- publication metadata intended to align the citable and installable artifact at v1.4.3.

The hidden-confounding scenario is a **known limitation benchmark**. It deliberately removes a true confounder before the normal Evaluate pipeline sees the data. Passing the scenario means the benchmark successfully demonstrates that the current observed-data safeguards can return `use` while the adjusted answer is materially wrong. It does not mean the hidden variable was detected.

## Required v1.4.3 verification

After the exact `v1.4.3` tag has produced the GitHub release, Zenodo archive and PyPI artifact, repeat the public install check in a clean environment.

Minimum commands:

```powershell
pip install reasoned-ops==1.4.3
python -c "import reasoned_ops; print(reasoned_ops.__version__)"
reasoned-validity --n 1200 --seed 23 --json
```

Expected version:

```text
1.4.3
```

Expected validity scenario names:

```text
known_effect_recovery
measured_confounding
no_overlap
slope_interaction
unmeasured_confounding_blind_spot
```

Also repeat a small public API/routing smoke path so the final aligned package is verified as executable rather than merely present on PyPI.

Only after those observations are made should this document record **v1.4.3 public verification: complete**.

## Artifact chain to verify

The final close-out requires the same version checkpoint across public channels:

```text
Git tag v1.4.3
      ↓
GitHub Release v1.4.3
      ↓
Zenodo archived v1.4.3
      ↓
PyPI reasoned-ops==1.4.3
      ↓
fresh-environment install / version / validity smoke check
```

## Evidence boundary

Public-package verification establishes package distribution and executable local behaviour. It is **not** independent scientific validation and does not establish:

- real-world service effectiveness;
- causal impact;
- absence of unmeasured confounding;
- private-data approval;
- production readiness.

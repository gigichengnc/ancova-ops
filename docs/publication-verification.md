# Public package verification — ReasonedOps

This document separates **observed public-artifact verification** from scientific or production validation.

## Final aligned public artifact: 1.4.4

ReasonedOps 1.4.4 was published to public PyPI from the immutable Git tag **`v1.4.4`** after that same release had been archived by Zenodo.

The GitHub publishing workflow was manually dispatched with:

```text
tag = v1.4.4
```

The workflow log verified that it checked out `refs/tags/v1.4.4`, resolved to release commit:

```text
9b2724354f43a5ed03fca6f3998f88be8c2bb513
```

and then printed:

```text
Publishing reasoned-ops 1.4.4
```

The build produced:

```text
reasoned_ops-1.4.4-py3-none-any.whl
reasoned_ops-1.4.4.tar.gz
```

Both uploads returned `200 OK` from PyPI.

Published distribution digests recorded by the workflow were:

```text
wheel SHA-256:
7b83297b8dc7e74408b353a743b4d0a0e2fca05e0cca832d1c38df710f7997d4

sdist SHA-256:
37dd14d34af83ef7bcf1f6f687bce7cb6fa0c902466b6998f89e0b3e7b530f55
```

The PyPI publishing action generated digital attestations through the Trusted Publishing / Sigstore path.

## Zenodo archive

The exact v1.4.4 GitHub release was archived by Zenodo with immutable **version DOI**:

```text
10.5281/zenodo.22051819
```

This identifier is recorded as the v1.4.4 version DOI. No all-versions/concept DOI is inferred from it.

## Fresh Windows verification

After publication, `reasoned-ops==1.4.4` was installed from public PyPI in a Windows environment outside the repository checkout.

Observed package version:

```text
1.4.4
```

The command used was:

```powershell
python -c "import reasoned_ops; print(reasoned_ops.__version__)"
```

Observed validity command:

```powershell
reasoned-validity --n 1200 --seed 23
```

Observed result:

```text
ReasonedOps evaluation validity benchmark
Overall pass: True
- known_effect_recovery: PASS
- measured_confounding: PASS
- no_overlap: PASS
- slope_interaction: PASS
- unmeasured_confounding_blind_spot: PASS
```

The final scenario is a **known limitation benchmark**. `PASS` means the benchmark successfully reproduced and disclosed a false-negative mode in which observed-data checks can pass while an omitted confounder still makes the adjusted answer materially wrong. It does **not** mean ReasonedOps detected hidden confounding.

### Raw-router smoke checks

A normal recurring air-conditioning request was routed to:

```text
department = maintenance
priority = high
requires_human_review = True
secondary_notify = community_management
```

A raw `ServiceCase` containing `fire` and `smoke` was routed to:

```text
department = emergency_response
requires_human_review = True
secondary_notify = community_management
```

That direct `baseline_route()` smoke call used the `ServiceCase` default urgency rather than the full request-intelligence pipeline, so its raw-router priority value is not treated as the full API emergency-priority result. The integrated FastAPI regression test separately verifies the intended end-to-end behaviour:

```text
issue_category = emergency
department = emergency_response
priority = critical
requires_human_review = True
secondary_notify = community_management
```

A substring negative-control request:

```text
I want to give feedback about the current service.
```

was routed to `community_management` and did **not** misclassify `feedback` as `fee` or `current` as `rent`. This externally exercises the v1.4.4 word/phrase-boundary fix.

These observations establish that the public 1.4.4 package is installable and that the released rule-based routing and validity CLI execute outside the repository checkout.

## Final public artifact chain

The completed v1 close-out has one aligned software version across the public channels:

```text
Git tag v1.4.4
      ↓
GitHub Release v1.4.4
      ↓
release commit 9b2724354f43a5ed03fca6f3998f88be8c2bb513
      ↓
Zenodo archived v1.4.4
DOI 10.5281/zenodo.22051819
      ↓
PyPI reasoned-ops==1.4.4
      ↓
fresh Windows install / version / validity / routing verification
```

Later documentation-only commits on `main` do not alter the immutable `v1.4.4` tag. PyPI 1.4.4 was built from that tag, not from later citation or verification commits.

## Historical verified public artifact: 1.4.3

The previous aligned checkpoint was v1.4.3:

```text
Git tag / GitHub Release v1.4.3
Zenodo DOI 10.5281/zenodo.22046490
PyPI reasoned-ops==1.4.3
fresh Windows version / validity / routing verification
```

Its published wheel SHA-256 was `677c3c5f853fc692cbecf5afd1689480a291a08bd003a6b18900482e67123bd3` and sdist SHA-256 was `4cffc44a7dce89366de9e65592c07b78e811fabc038071f990cfa706b1415b08`.

v1.4.3 remains historical evidence for the pre-hardening public artifact; v1.4.4 supersedes it as the frozen v1 checkpoint.

## Historical public artifact: 1.4.0

ReasonedOps 1.4.0 was the first public PyPI distribution installed and manually exercised outside the repository checkout. That historical verification covered the Operate → Audit → Evaluate flow, FastAPI startup, persistence of the original machine recommendation after human override, separate outcome storage, and the earlier four-scenario validity benchmark.

## Evidence boundary

Public-package verification establishes package distribution, provenance alignment and executable local behaviour. It is **not** independent scientific validation and does not establish:

- real-world service effectiveness;
- causal impact;
- absence of unmeasured confounding;
- private-data approval;
- production readiness.

Those questions require representative real-world data, governance approval and a defensible evaluation design beyond v1.

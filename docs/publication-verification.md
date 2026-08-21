# Public package verification — ReasonedOps

This document separates **observed public-artifact verification** from scientific or production validation.

## Final aligned public artifact: 1.4.3

ReasonedOps 1.4.3 was published to public PyPI from the exact existing Git tag **`v1.4.3`** after that same release had been archived by Zenodo.

The GitHub publishing workflow was manually dispatched with:

```text
tag = v1.4.3
```

The workflow log verified that it checked out `refs/tags/v1.4.3`, resolved to release commit:

```text
461b5fc81c2b31fc5fcc51c585004d059bb85586
```

and then printed:

```text
Publishing reasoned-ops 1.4.3
```

The build produced:

```text
reasoned_ops-1.4.3-py3-none-any.whl
reasoned_ops-1.4.3.tar.gz
```

Both uploads returned `200 OK` from PyPI.

Published distribution digests recorded by the workflow were:

```text
wheel SHA-256:
677c3c5f853fc692cbecf5afd1689480a291a08bd003a6b18900482e67123bd3

sdist SHA-256:
4cffc44a7dce89366de9e65592c07b78e811fabc038071f990cfa706b1415b08
```

The PyPI publishing action also generated digital attestations through the Trusted Publishing / Sigstore path.

## Fresh Windows verification

After publication, `reasoned-ops==1.4.3` was installed from public PyPI in a Windows environment outside the repository checkout.

Observed package version:

```text
1.4.3
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

A public routing smoke check was also run against the installed 1.4.3 package using the recurring air-conditioning example:

```text
The air conditioner is leaking again.
This is the third time and the wet floor could be dangerous.
```

Observed routing decision included:

```text
department = maintenance
priority = high
requires_human_review = True
secondary_notify = community_management
```

The returned reasons referenced maintenance-related terms, high-priority context, recurrence / unresolved history, and secondary community-management notification.

These observations establish that the public 1.4.3 package is installable and that the released rule-based routing and validity CLI execute outside the repository checkout.

## Final public artifact chain

The v1 close-out now has one aligned software version across the public channels:

```text
Git tag v1.4.3
      ↓
GitHub Release v1.4.3
      ↓
release commit 461b5fc81c2b31fc5fcc51c585004d059bb85586
      ↓
Zenodo archived v1.4.3
DOI 10.5281/zenodo.22046490
      ↓
PyPI reasoned-ops==1.4.3
      ↓
fresh Windows install / version / validity / routing verification
```

The post-release DOI-sync commits on `main` do not alter the immutable `v1.4.3` tag. PyPI 1.4.3 was built from the tag, not from those later documentation-only commits.

## Historical public artifact: 1.4.0

ReasonedOps 1.4.0 was the first public PyPI distribution that was installed and manually exercised outside the repository checkout.

That historical verification included:

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

The installed FastAPI application also started through:

```powershell
python -m uvicorn reasoned_ops.api:app --reload
```

A persisted case retained the original machine recommendation after a human override to `community_management`, and outcome data was stored separately.

That 1.4.0 record remains historical evidence for the earlier public artifact; the final aligned public checkpoint is now 1.4.3.

## Evidence boundary

Public-package verification establishes package distribution, provenance alignment and executable local behaviour. It is **not** independent scientific validation and does not establish:

- real-world service effectiveness;
- causal impact;
- absence of unmeasured confounding;
- private-data approval;
- production readiness.

Those questions require representative real-world data, governance approval and a defensible evaluation design beyond v1.

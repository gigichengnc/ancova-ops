# Citation and Zenodo archiving

ReasonedOps uses the root [`CITATION.cff`](../CITATION.cff) as its citation metadata source. The project was formerly called **ANCOVA Ops**; current citations use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

HKMU Hackathon 2026 is referenced only as project-origin context and does not imply official HKMU endorsement.

## Verified v1.4.4 archive

Zenodo has ingested the immutable GitHub release `v1.4.4` and published the exact version DOI:

```text
v1.4.4  →  10.5281/zenodo.22051819
```

The current-branch `CITATION.cff` records this verified DOI. This DOI-sync commit does **not** rewrite the immutable `v1.4.4` tag and must not replace that tag as the PyPI build source.

## Verified version DOIs

```text
v1.4.1  →  10.5281/zenodo.22044222
v1.4.2  →  10.5281/zenodo.22044621
v1.4.3  →  10.5281/zenodo.22046490
v1.4.4  →  10.5281/zenodo.22051819
```

## v1.4.4 provenance rule

The intended publication chain is:

```text
Git tag v1.4.4
      = source of GitHub Release v1.4.4
      = source of Zenodo v1.4.4 archive
      = source of PyPI reasoned-ops==1.4.4
```

The first three checkpoints are now established. PyPI publication must still use the immutable exact input tag `v1.4.4`, not a later default-branch DOI-sync commit.

## Version DOI vs concept DOI

Every identifier listed above is treated as a **version DOI** for its archived snapshot. The repository does not infer or invent an all-versions concept DOI from numeric patterns or from a latest-version badge. A concept DOI should only be recorded if Zenodo independently exposes a distinct `Cite all versions` identifier.

## Why there is no `.zenodo.json`

ReasonedOps does not currently need Zenodo-only grants/community metadata, so duplicate citation metadata is avoided. `CITATION.cff` remains the single citation source unless a concrete Zenodo-specific need arises.

## Evidence boundary

A DOI makes a software snapshot persistently identifiable and citable. It does not constitute peer review, real-world validation, causal identification, private-data approval or production readiness. Current quantitative evidence remains synthetic or hand-authored development evidence, including the explicit unmeasured-confounding known-limitation benchmark.

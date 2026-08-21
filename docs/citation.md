# Citation and Zenodo archiving

ReasonedOps uses the root [`CITATION.cff`](../CITATION.cff) as its citation metadata source. The project was formerly called **ANCOVA Ops**; current citations use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

HKMU Hackathon 2026 is referenced only as project-origin context and does not imply official HKMU endorsement.

## Current release candidate

The current code checkpoint is **v1.4.4**. Its release-candidate `CITATION.cff` records the title, author, version, date, Apache-2.0 licence, repository URL and evidence boundary, but intentionally has **no DOI yet**.

A v1.4.3 DOI must not be copied into v1.4.4 metadata. The v1.4.4 immutable version DOI only exists after Zenodo ingests the exact `v1.4.4` GitHub release.

## Verified historical version DOIs

```text
v1.4.1  →  10.5281/zenodo.22044222
v1.4.2  →  10.5281/zenodo.22044621
v1.4.3  →  10.5281/zenodo.22046490
```

v1.4.3 is the latest fully verified public chain at the time of v1.4.4 release preparation:

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

## v1.4.4 publication rule

The same provenance rule applies to v1.4.4:

```text
one immutable Git tag v1.4.4
      = source of GitHub Release v1.4.4
      = source of Zenodo v1.4.4 archive
      = source of PyPI reasoned-ops==1.4.4
```

After Zenodo mints the v1.4.4 version DOI, current-branch citation metadata may be updated to record that verified identifier. That later DOI-sync commit must not replace the immutable `v1.4.4` tag as the PyPI build source.

## Version DOI vs concept DOI

Each verified identifier above is treated as a **version DOI** for its archived snapshot. The repository does not infer or invent an all-versions concept DOI from numeric patterns or from a latest-version badge. A concept DOI should only be recorded if Zenodo independently exposes a distinct `Cite all versions` identifier.

## Why there is no `.zenodo.json`

ReasonedOps does not currently need Zenodo-only grants/community metadata, so duplicate citation metadata is avoided. `CITATION.cff` remains the single citation source unless a concrete Zenodo-specific need arises.

## Evidence boundary

A DOI makes a software snapshot persistently identifiable and citable. It does not constitute peer review, real-world validation, causal identification, private-data approval or production readiness. Current quantitative evidence remains synthetic or hand-authored development evidence, including the explicit unmeasured-confounding known-limitation benchmark.

# Citation and Zenodo archiving

ReasonedOps ships a root [`CITATION.cff`](../CITATION.cff) file so the software has one human- and machine-readable citation source.

The project was formerly called **ANCOVA Ops**. From v1.1.0 onward, new citations should use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

ReasonedOps is the author's own project. **HKMU Hackathon 2026** is referenced only to describe where the project began; it is not presented as an official HKMU product or endorsement.

## GitHub citation

When `CITATION.cff` is present on the default branch, GitHub can expose a **Cite this repository** control and render citation formats from the file.

The v1.4.3 release-candidate metadata records:

- software title: ReasonedOps;
- author: Gigi Cheng;
- software version: v1.4.3;
- release date;
- Apache-2.0 license;
- repository URL;
- the tightened rule-based Operate description;
- the explicit unmeasured-confounding limitation benchmark;
- no fabricated ORCID, email, affiliation or future DOI.

## Why the v1.4.3 release candidate has no top-level DOI yet

Zenodo's GitHub integration mints an immutable **version DOI after it ingests a GitHub release**. Therefore a v1.4.3 release candidate cannot truthfully contain its own version DOI before the release exists.

The previous v1.4.2 DOI must not be copied forward into the v1.4.3 `CITATION.cff`, because that would make the new snapshot cite a different archived snapshot.

The intended sequence is:

```text
prepare v1.4.3 metadata without a top-level version DOI
      ↓
merge after CI
      ↓
GitHub Release v1.4.3 is created from that exact commit
      ↓
Zenodo ingests v1.4.3 and mints its immutable version DOI
      ↓
verify the DOI + creator/title/version/license
      ↓
post-release sync the verified DOI into main-branch citation docs
```

The release workflow is idempotent for an existing tag. Once `v1.4.3` exists, a later documentation-only DOI sync on `main` does **not** require or justify another version bump.

## Existing verified Zenodo archives

The Zenodo GitHub integration already shows:

```text
v1.4.1  →  10.5281/zenodo.22044222
v1.4.2  →  10.5281/zenodo.22044621
```

Those remain valid immutable version DOIs for those historical snapshots.

`10.5281/zenodo.22044621` is specifically the **v1.4.2 version DOI**. It is not reused as the DOI for v1.4.3.

## Version DOI vs concept DOI

Zenodo can distinguish an immutable **version DOI** from a **concept DOI** representing all versions.

The screenshots verified the v1.4.1 and v1.4.2 version DOIs, but the all-versions concept DOI has not yet been independently captured in this repository. The README therefore does not currently show a DOI badge rather than silently using the latest version DOI as though it were an all-versions identifier.

After v1.4.3 is archived, verify both identifiers if Zenodo displays both:

- **version DOI** → use for the exact v1.4.3 citation;
- **concept / all-versions DOI** → suitable for a stable project-level README badge.

Do not infer either identifier from record-number patterns.

## PyPI / Zenodo provenance alignment

The earlier public state had a deliberate but awkward distinction:

```text
PyPI installable artifact  = 1.4.0
preferred Zenodo snapshot  = 1.4.2
```

The executable project logic between those checkpoints was largely unchanged, but the artifacts were still different snapshots. For an audit/provenance-oriented project, that distinction is worth closing.

v1.4.3 is the audit-closeout checkpoint. The goal is:

```text
GitHub tag v1.4.3
      = source of GitHub Release v1.4.3
      = source of Zenodo v1.4.3 archive
      = source of PyPI reasoned-ops==1.4.3
```

The PyPI workflow should therefore be run with the exact existing tag `v1.4.3` only after the release has passed CI and been archived.

## Why there is no `.zenodo.json`

Zenodo supports both `CITATION.cff` and `.zenodo.json` for GitHub software metadata. ReasonedOps currently does not need Zenodo-only metadata such as grants or community identifiers, so `CITATION.cff` remains the single source of citation metadata. This reduces duplicate metadata and version drift.

Add `.zenodo.json` later only if a concrete Zenodo-specific requirement justifies maintaining a second metadata source.

## Publication boundary

Citation/archive completion does not change the operational status of ReasonedOps:

- current quantitative evidence remains synthetic or hand-authored development evidence;
- the validity benchmark explicitly demonstrates an unmeasured-confounding false-negative mode;
- private-data pilot use remains not approved;
- production deployment remains not approved;
- adaptive-policy activation remains separated from the live route path;
- sequence modelling remains deferred until incremental value is demonstrated.

A Zenodo DOI makes the software persistently identifiable and citable. It does **not** constitute peer review and does not upgrade synthetic or hand-authored development results into real-world evidence.

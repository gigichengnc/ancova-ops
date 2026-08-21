# Citation and Zenodo archiving

ReasonedOps ships a root [`CITATION.cff`](../CITATION.cff) file so the software has one human- and machine-readable citation source.

The project was formerly called **ANCOVA Ops**. From v1.1.0 onward, new citations should use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

ReasonedOps is the author's own project. **HKMU Hackathon 2026** is referenced only to describe where the project began; it is not presented as an official HKMU product or endorsement.

## GitHub citation

When `CITATION.cff` is present on the default branch, GitHub can expose a **Cite this repository** control and render citation formats from the file.

The current v1.4.3 citation metadata records:

- software title: ReasonedOps;
- author: Gigi Cheng;
- software version: v1.4.3;
- release date;
- Apache-2.0 license;
- repository URL;
- the tightened rule-based Operate description;
- the explicit unmeasured-confounding limitation benchmark;
- verified v1.4.3 Zenodo version DOI: `10.5281/zenodo.22046490`;
- no fabricated ORCID, email or affiliation.

## Verified v1.4.3 archive

The GitHub `v1.4.3` tag is identical to the intended v1.4.3 release commit. Zenodo's GitHub integration has ingested that release and shows it as **Published**.

The verified immutable v1.4.3 version DOI is:

```text
10.5281/zenodo.22046490
```

The repository therefore records that exact DOI in `CITATION.cff` on the default branch.

This DOI identifies the archived v1.4.3 snapshot. It must not be retroactively inserted into the immutable Git tag itself; the release tag remains the source snapshot that Zenodo archived.

## Existing verified Zenodo archives

The Zenodo GitHub integration shows:

```text
v1.4.1  →  10.5281/zenodo.22044222
v1.4.2  →  10.5281/zenodo.22044621
v1.4.3  →  10.5281/zenodo.22046490
```

Each is an immutable version DOI for its corresponding archived snapshot.

## Version DOI vs concept DOI

Zenodo can distinguish an immutable **version DOI** from a **concept DOI** representing all versions.

The v1.4.3 integration screen displays `10.5281/zenodo.22046490` both on the v1.4.3 release row and in the repository DOI badge area. That is sufficient evidence to record it as the **v1.4.3 version DOI**. It is not sufficient, by itself, to relabel it as a separate all-versions concept DOI.

The repository therefore does **not** claim a concept DOI unless Zenodo independently exposes a distinct `Cite all versions` identifier and that identifier is captured directly.

This is also why the README does not infer a project-level concept DOI from record-number patterns or from the latest-version badge.

## PyPI / Zenodo provenance alignment

Before v1.4.3, the public state was:

```text
PyPI installable artifact  = 1.4.0
preferred Zenodo snapshot  = 1.4.2
```

v1.4.3 closes that provenance gap by using one exact source tag:

```text
GitHub tag v1.4.3
      = source of GitHub Release v1.4.3
      = source of Zenodo v1.4.3 archive
      = source of PyPI reasoned-ops==1.4.3
```

The GitHub/Zenodo side is now verified. The remaining publication step is to run the PyPI Trusted Publishing workflow with the exact existing tag `v1.4.3`, then verify the public wheel in a fresh environment.

A later DOI-sync commit on `main` is documentation/citation metadata only. It must **not** become the source for the PyPI 1.4.3 artifact; PyPI must still publish from the immutable `v1.4.3` tag.

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

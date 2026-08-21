# Citation and Zenodo archiving

ReasonedOps ships a root [`CITATION.cff`](../CITATION.cff) file so the software has one human- and machine-readable citation source.

The project was formerly called **ANCOVA Ops**. From v1.1.0 onward, new citations should use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

ReasonedOps is the author's own project. **HKMU Hackathon 2026** is referenced only to describe where the project began; it is not presented as an official HKMU product or endorsement.

## GitHub citation

When `CITATION.cff` is present on the default branch, GitHub can expose a **Cite this repository** control and render citation formats from the file.

The citation metadata records:

- software title: ReasonedOps;
- author: Gigi Cheng;
- current software version: v1.4.2;
- release date;
- Apache-2.0 license;
- repository URL;
- the verified Zenodo DOI for the v1.4.2 archive;
- a short research-software abstract and keywords.

No ORCID, email address or affiliation is invented. Those fields should only be added when a verified identifier or public attribution is intentionally supplied.

## Why there is no `.zenodo.json`

Zenodo supports both `CITATION.cff` and `.zenodo.json` for GitHub software metadata. ReasonedOps currently does not need Zenodo-only metadata such as grants or community identifiers, so `CITATION.cff` remains the single source of citation metadata. This reduces duplicate metadata and version drift.

Add `.zenodo.json` later only if a concrete Zenodo-specific requirement justifies maintaining a second metadata source.

## Verified Zenodo archive status

The GitHub account is connected to Zenodo and `gigichengnc/reasoned-ops` is enabled for automatic preservation of new GitHub releases.

The Zenodo GitHub integration shows two published ReasonedOps releases:

```text
v1.4.1  →  10.5281/zenodo.22044222
v1.4.2  →  10.5281/zenodo.22044621
```

The current preferred citation checkpoint is **v1.4.2**, because that release contains the corrected project-origin wording and represents the final v1 publication checkpoint.

The verified v1.4.2 DOI is therefore:

```text
10.5281/zenodo.22044621
```

That DOI is recorded in `CITATION.cff` using the top-level `doi` field and is used by the README DOI badge.

## Version DOI vs concept DOI

Zenodo can distinguish an immutable **version DOI** from a **concept DOI** that represents a collection of versions.

For ReasonedOps, `10.5281/zenodo.22044621` is verified here as the **v1.4.2 version DOI** because the Zenodo GitHub integration explicitly lists that DOI on the v1.4.2 release row. The repository-level badge shown by that integration currently displays the same DOI as the latest release.

A separate concept DOI is **not recorded in this repository unless it is independently identified and verified**. Do not relabel the verified v1.4.2 DOI as a concept DOI without that evidence.

## Publication close-out

Current status:

1. GitHub account connected to Zenodo — **complete**.
2. `gigichengnc/reasoned-ops` enabled in the Zenodo GitHub integration — **complete**.
3. ReasonedOps v1.4.1 archived — **complete**, DOI `10.5281/zenodo.22044222`.
4. ReasonedOps v1.4.2 archived — **complete**, DOI `10.5281/zenodo.22044621`.
5. v1.4.2 DOI recorded in README and `CITATION.cff` — **publication close-out change**.
6. No additional software version is required merely to record this DOI.

The earlier v1.4.0 release existed before Zenodo enablement. v1.4.2 is the preferred archived citation checkpoint with corrected project-origin wording.

## README badge

The README uses the verified v1.4.2 Zenodo DOI:

```text
10.5281/zenodo.22044621
```

If a separate concept DOI is later independently verified and a project-level all-versions badge is preferred, the badge can be changed deliberately. That is optional and does not require another functional software release.

## PyPI and Zenodo version note

The currently published and externally verified PyPI artifact is `reasoned-ops==1.4.0`.

v1.4.2 is a GitHub/Zenodo citation/wording checkpoint. Unless it is separately published through the PyPI Trusted Publishing workflow, do not claim that PyPI contains version 1.4.2.

This distinction is intentional because v1.4.2 changes citation/presentation metadata, not functional behaviour.

## Publication boundary

Citation/archive completion does not change the operational status of ReasonedOps:

- current quantitative evidence remains synthetic or hand-authored development evidence;
- private-data pilot use remains not approved;
- production deployment remains not approved;
- adaptive-policy activation remains separated from the live route path;
- sequence modelling remains deferred until incremental value is demonstrated.

A Zenodo DOI makes the software persistently identifiable and citable. It does **not** constitute peer review and does not upgrade synthetic or hand-authored development results into real-world evidence.

# Citation and Zenodo archiving

ReasonedOps ships a root [`CITATION.cff`](../CITATION.cff) file so the software has one human- and machine-readable citation source.

The project was formerly called **ANCOVA Ops**. From v1.1.0 onward, new citations should use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

ReasonedOps is the author's own project. **HKMU Hackathon 2026** is referenced only to describe where the project began; it is not presented as an official HKMU product or endorsement.

## GitHub citation

When `CITATION.cff` is present on the default branch, GitHub can expose a **Cite this repository** control and render citation formats from the file.

The citation metadata records:

- software title: ReasonedOps;
- author: Gigi Cheng;
- current software version;
- release date;
- Apache-2.0 license;
- repository URL;
- the stable Zenodo concept DOI for the archived ReasonedOps version collection;
- a short research-software abstract and keywords.

No ORCID, email address, affiliation or version-specific DOI is invented. Those fields should only be added when a verified identifier or public attribution is intentionally supplied.

## Why there is no `.zenodo.json`

Zenodo supports both `CITATION.cff` and `.zenodo.json` for GitHub software metadata. ReasonedOps currently does not need Zenodo-only metadata such as grants or community identifiers, so `CITATION.cff` remains the single source of citation metadata. This reduces duplicate metadata and version drift.

Add `.zenodo.json` later only if a concrete Zenodo-specific requirement justifies maintaining a second metadata source.

## Current Zenodo status

The GitHub account is connected to Zenodo and `gigichengnc/reasoned-ops` is enabled for automatic preservation of new GitHub releases.

The Zenodo GitHub integration now displays the DOI:

```text
10.5281/zenodo.22044621
```

This repository records that identifier as the **Zenodo concept DOI** for the collection of archived ReasonedOps versions. A concept DOI is intentionally stable across versions and is therefore appropriate for the README project badge and for identifying the archived project lineage.

v1.4.1 was the first checkpoint created after Zenodo enablement. v1.4.2 is the preferred current citation checkpoint because it corrects project-origin wording so the software is described as one project that evolved from its Hackathon starting point, rather than as a rebuild of another project.

Current sequence:

```text
Zenodo integration enabled
      ↓
release v1.4.2 after successful main CI
      ↓
Zenodo archive created / linked
      ↓
concept DOI visible: 10.5281/zenodo.22044621
      ↓
record concept DOI in README + CITATION.cff
      ↓
optionally record the exact v1.4.2 version DOI after separately verifying that record
```

## Concept DOI vs version DOI

Zenodo versioning distinguishes two identifiers:

- **Concept DOI** — identifies the collection of all archived versions and remains stable as later versions are added.
- **Version DOI** — identifies one immutable archived snapshot.

ReasonedOps currently records `10.5281/zenodo.22044621` as the concept DOI because that is the DOI shown for the enabled repository in the Zenodo GitHub integration.

Do not describe this concept DOI as the version-specific DOI for v1.4.2 unless the individual v1.4.2 record is separately opened and verified. If that version DOI is later recorded, `CITATION.cff` can contain both identifiers with explicit descriptions rather than replacing or ambiguously relabelling the concept DOI.

## Archiving a release in Zenodo

Repository metadata readiness and Zenodo account integration are separate steps.

Current status:

1. GitHub account connected to Zenodo — **complete**.
2. `gigichengnc/reasoned-ops` enabled in the Zenodo GitHub integration — **complete**.
3. Current archive checkpoint is v1.4.2 — **complete**.
4. Stable concept DOI is visible in the Zenodo GitHub integration — **complete**.
5. Concept DOI is recorded in repository citation metadata — **in this publication close-out change**.
6. Exact v1.4.2 version DOI and record-level metadata can be recorded after separate verification — **optional follow-up for version-specific citation**.

The earlier v1.4.0 release existed before Zenodo enablement. v1.4.2 is therefore the preferred current post-enablement citation checkpoint with corrected project-origin wording.

## README badge

The README uses the stable concept DOI for the Zenodo badge:

```text
10.5281/zenodo.22044621
```

Using the concept DOI avoids needing to replace the project-level badge every time a future archived release receives its own version DOI.

## PyPI and Zenodo version note

The currently published and externally verified PyPI artifact is `reasoned-ops==1.4.0`.

v1.4.2 is a GitHub/Zenodo citation/wording checkpoint. Unless it is separately published through the PyPI Trusted Publishing workflow, do not claim that PyPI contains version 1.4.2.

This distinction is intentional because v1.4.2 changes citation/presentation metadata, not functional behaviour.

## Publication boundary

Citation/archive readiness does not change the operational status of ReasonedOps:

- current quantitative evidence remains synthetic or hand-authored development evidence;
- private-data pilot use remains not approved;
- production deployment remains not approved;
- adaptive-policy activation remains separated from the live route path;
- sequence modelling remains deferred until incremental value is demonstrated.

A Zenodo DOI makes the software persistently identifiable and citable. It does **not** constitute peer review and does not upgrade synthetic or hand-authored development results into real-world evidence.

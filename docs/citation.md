# Citation and Zenodo archiving

ReasonedOps ships a root [`CITATION.cff`](../CITATION.cff) file so the software has one human- and machine-readable citation source.

The project was formerly called **ANCOVA Ops**. From v1.1.0 onward, new citations should use **ReasonedOps** and the canonical repository `gigichengnc/reasoned-ops`.

## GitHub citation

When `CITATION.cff` is present on the default branch, GitHub can expose a **Cite this repository** control and render citation formats from the file.

The citation metadata records:

- software title: ReasonedOps;
- author: Gigi Cheng;
- current software version;
- release date;
- Apache-2.0 license;
- repository URL;
- a short research-software abstract and keywords.

No DOI, ORCID, email address or affiliation is invented. Those fields should only be added when a verified identifier or public attribution is intentionally supplied.

## Why there is no `.zenodo.json`

Zenodo supports both `CITATION.cff` and `.zenodo.json` for GitHub software metadata. ReasonedOps currently does not need Zenodo-only metadata such as grants or community identifiers, so `CITATION.cff` remains the single source of citation metadata. This reduces duplicate metadata and version drift.

Add `.zenodo.json` later only if a concrete Zenodo-specific requirement justifies maintaining a second metadata source.

## Current Zenodo status

The GitHub account is connected to Zenodo and `gigichengnc/reasoned-ops` has been enabled for automatic preservation of **new** GitHub releases.

v1.4.1 is the first checkpoint intentionally prepared after that enablement. Its purpose is archival/citation synchronization rather than new functionality.

Current sequence:

```text
Zenodo integration enabled
      ↓
release v1.4.1 after successful main CI
      ↓
Zenodo ingests the GitHub release
      ↓
verify archived metadata + DOI
      ↓
add the verified DOI back to CITATION.cff
```

Do not add a DOI to the repository before the actual Zenodo record is visible and verified.

## Archiving a release in Zenodo

Repository metadata readiness and Zenodo account integration are separate steps.

The current process is:

1. GitHub account connected to Zenodo — **complete**.
2. `gigichengnc/reasoned-ops` enabled in the Zenodo GitHub integration — **complete**.
3. Create GitHub Release v1.4.1 after successful `main` CI — **pending until the release workflow completes**.
4. Wait for Zenodo to ingest the release and create the software record.
5. Review creator, title, version, license and archive metadata.
6. Record the verified DOI in repository citation metadata.

The earlier v1.4.0 release existed before Zenodo enablement, so v1.4.1 is used as the clean post-enablement archive checkpoint rather than assuming retroactive ingestion.

## After a DOI exists

Once Zenodo has minted a DOI for the v1.4.1 ReasonedOps release:

1. verify the creator, title, version, license and release metadata in Zenodo;
2. add the verified version DOI to `CITATION.cff` using the `doi` field;
3. update README citation guidance if a DOI badge or direct citation link is desired;
4. distinguish the version DOI from any Zenodo concept DOI if both are shown;
5. keep the package/checkpoint version, GitHub release tag and CFF version aligned for future archive releases;
6. run CI before publishing another release.

A Zenodo DOI makes the software release persistently identifiable and citable. It does **not** constitute peer review and does not upgrade synthetic or hand-authored development results into real-world evidence.

## PyPI and Zenodo version note

The currently published and externally verified PyPI artifact is `reasoned-ops==1.4.0`.

v1.4.1 is being created as a GitHub/Zenodo archive checkpoint. Unless it is separately published through the PyPI Trusted Publishing workflow, do not claim that PyPI contains version 1.4.1.

This distinction is intentional because v1.4.1 changes citation/archive metadata, not functional behaviour.

## Publication boundary

Citation/archive readiness does not change the operational status of ReasonedOps:

- current quantitative evidence remains synthetic or hand-authored development evidence;
- private-data pilot use remains not approved;
- production deployment remains not approved;
- adaptive-policy activation remains separated from the live route path;
- sequence modelling remains deferred until incremental value is demonstrated.

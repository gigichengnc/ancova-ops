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

## Archiving a release in Zenodo

Repository metadata readiness and Zenodo account integration are separate steps.

To enable automatic archiving for future releases:

1. Sign in to Zenodo and connect the GitHub account that owns this repository.
2. Open the Zenodo GitHub integration page.
3. Sync repositories and enable `gigichengnc/reasoned-ops`.
4. Create a new GitHub release after the repository is enabled in Zenodo.
5. Wait for Zenodo to ingest the release and create the software record.
6. Review the archived metadata and DOI before citing it externally.

Do not assume that a release created before repository integration will be ingested retroactively. If necessary, use Zenodo's supported manual software-upload route or create a later release after enabling the integration.

## After a DOI exists

Once Zenodo has minted a DOI for a specific ReasonedOps release:

1. verify the creator, title, version, license and release metadata in Zenodo;
2. add the verified version DOI to `CITATION.cff` using the `doi` field;
3. update README citation guidance if a DOI badge or direct citation link is desired;
4. keep the package version, GitHub release tag and CFF version aligned;
5. run CI before publishing another release.

A Zenodo DOI makes the software release persistently identifiable and citable. It does **not** constitute peer review and does not upgrade synthetic or hand-authored development results into real-world evidence.

## Publication boundary

Citation/archive readiness does not change the operational status of ReasonedOps:

- current quantitative evidence remains synthetic or hand-authored development evidence;
- private-data pilot use remains not approved;
- production deployment remains not approved;
- adaptive-policy activation remains separated from the live route path;
- sequence modelling remains deferred until incremental value is demonstrated.

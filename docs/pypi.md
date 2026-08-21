# PyPI distribution and reuse

ReasonedOps is published on PyPI as **`reasoned-ops`** with import namespace **`reasoned_ops`**.

The final v1 audit-closeout target is to make the publicly installable artifact match the exact GitHub/Zenodo release snapshot.

## Current and target publication state

Current public PyPI artifact:

```text
reasoned-ops==1.4.0
```

Final aligned artifact to publish after the `v1.4.3` GitHub release is archived:

```text
reasoned-ops==1.4.3
```

The v1.4.3 package must be built from the exact existing Git tag `v1.4.3`. Do not rebuild it from a later moving `main` commit and call it the same release.

## Install

Until v1.4.3 is published, the historically verified exact install remains:

```bash
pip install reasoned-ops==1.4.0
```

After final publication and verification, the preferred exact install becomes:

```bash
pip install reasoned-ops==1.4.3
```

For another project that intentionally accepts compatible v1 updates:

```text
reasoned-ops>=1.4,<2
```

Pin an exact version when artifact reproducibility matters.

## Trusted Publishing

ReasonedOps uses PyPI Trusted Publishing rather than a stored long-lived API token.

The dedicated workflow is:

```text
.github/workflows/publish-pypi.yml
```

Trusted Publisher identity:

```text
PyPI project name: reasoned-ops
GitHub owner:        gigichengnc
Repository:          reasoned-ops
Workflow filename:   publish-pypi.yml
Environment:         pypi
```

The workflow is manually dispatched with an existing release tag. It checks out that tag, reads the embedded package version, and refuses publication when the requested tag does not match the package metadata.

For the final close-out, dispatch it with exactly:

```text
v1.4.3
```

## What CI verifies before publication

The distribution job:

1. builds a wheel and source distribution with `python -m build`;
2. checks that both artifacts exist;
3. creates a clean virtual environment;
4. installs the built wheel rather than the editable source tree;
5. imports `reasoned_ops` from that installed wheel;
6. executes a routing smoke check;
7. verifies a packaged CLI entry point.

The Python 3.11 / 3.12 matrix separately runs lint, tests and the major command-line workflows, including the current `reasoned-validity-v2` benchmark.

## Historical public verification

`reasoned-ops==1.4.0` was successfully published and then installed in a Windows environment outside the repository checkout. That check exercised Operate → Audit → Evaluate and established that the public package was installable and executable.

That historical record remains valid for 1.4.0; it should not be silently relabelled as a 1.4.3 verification.

See [`publication-verification.md`](publication-verification.md).

## Required 1.4.3 post-publication check

After PyPI reports `reasoned-ops==1.4.3`, use a fresh environment and run at minimum:

```bash
pip install reasoned-ops==1.4.3
python -c "import reasoned_ops; print(reasoned_ops.__version__)"
reasoned-validity --n 1200 --seed 23 --json
```

Expected version:

```text
1.4.3
```

The validity JSON should include all five scenarios:

```text
known_effect_recovery
measured_confounding
no_overlap
slope_interaction
unmeasured_confounding_blind_spot
```

For `unmeasured_confounding_blind_spot`, PASS means the benchmark reproduced the known false-negative mode. It does **not** mean hidden confounding was detected.

A small routing/import smoke check should also confirm the public API surface still works.

## Evidence boundary

Successful publication and external installation establish artifact distribution and executable local behaviour. They do **not** establish:

- real-world routing accuracy;
- real service improvement;
- absence of unmeasured confounding;
- causal effects;
- private-data approval;
- production readiness.

## Final provenance target

The close-out is complete only when these refer to the same release checkpoint:

```text
Git tag v1.4.3
      = GitHub Release v1.4.3
      = Zenodo v1.4.3 archived snapshot
      = PyPI reasoned-ops==1.4.3
```

The Zenodo **version DOI** identifies the archived v1.4.3 snapshot. If Zenodo separately exposes a verified all-versions / concept DOI, that identifier can be used for a stable project-level README badge.

# PyPI distribution and reuse

ReasonedOps is packaged as the Python distribution **`reasoned-ops`** with the import namespace **`reasoned_ops`**.

The purpose of PyPI publication is practical reuse: another Python project should be able to depend on a released ReasonedOps version instead of copying source files from this repository.

## Intended user experience

After the first PyPI publication succeeds:

```bash
pip install reasoned-ops
```

Then:

```python
from reasoned_ops import ServiceCase, baseline_route

case = ServiceCase(
    case_id="example-001",
    message="The air conditioner is leaking again.",
    previous_related_cases=2,
)

decision = baseline_route(case)
print(decision.department)
print(decision.reasons)
```

For another project, prefer a version constraint rather than an unbounded dependency, for example:

```text
reasoned-ops>=1.4,<2
```

Pin an exact version when reproducibility is more important than automatically receiving compatible updates.

## What CI verifies before publication

The repository CI has a separate distribution job that:

1. builds a wheel and source distribution with `python -m build`;
2. checks that both artifacts exist;
3. creates a clean virtual environment;
4. installs the built wheel rather than the editable source tree;
5. imports `reasoned_ops` from that installed wheel;
6. executes a routing smoke check;
7. verifies that a packaged CLI entry point is installed.

This is deliberately separate from the ordinary editable-install test matrix.

## Trusted Publishing

ReasonedOps uses PyPI Trusted Publishing rather than a stored long-lived API token.

The dedicated workflow is:

```text
.github/workflows/publish-pypi.yml
```

It is manually dispatched for the first publication. The build job does not receive OIDC publishing permission. A separate publish job downloads the built distributions and receives only the permissions needed for PyPI Trusted Publishing.

The publishing job uses the GitHub environment:

```text
pypi
```

## One-time PyPI account setup

Before running the publishing workflow for the first time, register a matching **pending Trusted Publisher** in the PyPI account that will own the project.

Use these exact values:

```text
PyPI project name: reasoned-ops
GitHub owner:        gigichengnc
Repository:          reasoned-ops
Workflow filename:   publish-pypi.yml
Environment:         pypi
```

The PyPI project name must match the distribution metadata exactly. Do not register a slightly different name and then try to publish the current wheel.

If PyPI reports that `reasoned-ops` cannot be created because the normalized project name is already owned by someone else, stop before publishing and choose a new distribution name deliberately. The import package `reasoned_ops` does not necessarily have to change if only the PyPI distribution name changes.

## First publication

After the pending Trusted Publisher is configured and the intended GitHub release tag exists:

1. open the repository **Actions** tab;
2. choose **Publish to PyPI**;
3. choose **Run workflow**;
4. enter the release tag, for example `v1.4.0`;
5. review/approve the `pypi` environment if repository protection rules require it;
6. wait for the build and publish jobs to complete;
7. verify the new project/version on PyPI;
8. install it in a fresh environment and run a minimal import test.

The workflow refuses to publish when the requested tag does not match the package version embedded in that tag.

## Post-publication verification

Use a clean environment that does not contain the Git checkout:

```bash
python -m venv /tmp/reasoned-pypi-check
source /tmp/reasoned-pypi-check/bin/activate
pip install reasoned-ops==1.4.0
python -c "import reasoned_ops; print(reasoned_ops.__version__)"
reasoned-applicability --help
```

A successful PyPI upload establishes package distribution and reuse. It does **not** establish real-world service effectiveness, private-data approval, or production readiness.

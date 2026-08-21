# PyPI distribution and reuse

ReasonedOps is published on PyPI as the Python distribution **`reasoned-ops`** with the import namespace **`reasoned_ops`**.

The purpose of PyPI publication is practical reuse: another Python project can depend on a released ReasonedOps version instead of copying source files from this repository.

## Install from PyPI

```bash
pip install reasoned-ops
```

For an exact reproducible release:

```bash
pip install reasoned-ops==1.4.0
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

The build job does not receive OIDC publishing permission. A separate publish job downloads the built distributions and receives only the permissions needed for PyPI Trusted Publishing.

The publishing job uses the GitHub environment:

```text
pypi
```

The first publication used a matching pending Trusted Publisher with this identity:

```text
PyPI project name: reasoned-ops
GitHub owner:        gigichengnc
Repository:          reasoned-ops
Workflow filename:   publish-pypi.yml
Environment:         pypi
```

## Publication status

`reasoned-ops==1.4.0` was successfully published through the Trusted Publishing workflow.

The public artifact was subsequently installed in a Windows environment outside the repository checkout. The verification confirmed:

- `import reasoned_ops` reports version `1.4.0`;
- the reusable routing surface returns a maintenance route, high priority and human-review requirement for a recurring air-conditioning case;
- `reasoned_ops.api:app` starts through Uvicorn;
- a routed case can be persisted through the API;
- a human override is stored without overwriting the original machine recommendation;
- a case outcome is stored separately;
- a later case fetch returns the original request, machine decision, human review, effective route and outcome together;
- `reasoned-validity` reports all four deterministic synthetic validity scenarios as passing.

See [`publication-verification.md`](publication-verification.md) for the detailed verification record and evidence boundary.

## Post-publication verification commands

A minimal package check is:

```bash
pip install reasoned-ops==1.4.0
python -c "import reasoned_ops; print(reasoned_ops.__version__)"
```

A reusable API/import check is:

```python
from reasoned_ops import ServiceCase, baseline_route

case = ServiceCase(
    case_id="test-001",
    message="The air conditioner is leaking again.",
    previous_related_cases=2,
)

decision = baseline_route(case)
assert decision.department == "maintenance"
```

The deterministic evaluation check is:

```bash
reasoned-validity
```

A successful PyPI publication and external install check establish package distribution and executable local behaviour. They do **not** establish real-world service effectiveness, causal impact, private-data approval, or production readiness.

## Future releases

For a future release:

1. update package/citation/release metadata deliberately;
2. merge only after CI and distribution checks pass;
3. allow the GitHub release checkpoint to create the matching release tag;
4. manually dispatch **Publish to PyPI** with that exact tag;
5. verify the published version from a clean environment.

The publishing workflow refuses to publish when the requested tag does not match the package version embedded in that tag.

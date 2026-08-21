from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "publish-pypi.yml"


def test_pypi_description_uses_canonical_distribution_name() -> None:
    text = (PROJECT_ROOT / "PYPI.md").read_text(encoding="utf-8")

    assert "pip install reasoned-ops" in text
    assert "from reasoned_ops import ServiceCase, baseline_route" in text


def test_publish_workflow_uses_manual_oidc_trusted_publishing() -> None:
    text = PUBLISH_WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "environment: pypi" in text
    assert "id-token: write" in text
    assert "pypa/gh-action-pypi-publish@release/v1" in text
    assert "PYPI_TOKEN" not in text
    assert "password:" not in text


def test_pypi_guide_matches_trusted_publisher_identity() -> None:
    text = (PROJECT_ROOT / "docs" / "pypi.md").read_text(encoding="utf-8")

    expected_lines = {
        "PyPI project name: reasoned-ops",
        "GitHub owner:        gigichengnc",
        "Repository:          reasoned-ops",
        "Workflow filename:   publish-pypi.yml",
        "Environment:         pypi",
    }

    for line in expected_lines:
        assert line in text

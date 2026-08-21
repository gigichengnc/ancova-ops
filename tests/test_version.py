import tomllib
from pathlib import Path

import ancova_ops
import reasoned_ops

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.1.1"
EXPECTED_REPOSITORY = "https://github.com/gigichengnc/reasoned-ops"
EXPECTED_SCRIPTS = {
    "reasoned-analyze",
    "reasoned-applicability",
    "reasoned-evaluate",
    "reasoned-governance-check",
    "reasoned-longitudinal",
    "reasoned-management-report",
    "reasoned-policy",
    "reasoned-showcase",
    "reasoned-validity",
}


def _project_metadata() -> dict[str, object]:
    return tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_package_version_matches_project_metadata() -> None:
    project = _project_metadata()

    assert reasoned_ops.__version__ == project["version"]
    assert reasoned_ops.__version__ == EXPECTED_VERSION
    assert ancova_ops.__version__ == EXPECTED_VERSION


def test_v111_cli_surface_is_registered() -> None:
    project = _project_metadata()

    assert project["name"] == "reasoned-ops"
    assert set(project["scripts"]) == EXPECTED_SCRIPTS


def test_apache_license_metadata_and_file_are_present() -> None:
    project = _project_metadata()
    license_text = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert project["license"] == "Apache-2.0"
    assert "Apache License" in license_text
    assert "Version 2.0, January 2004" in license_text


def test_citation_metadata_matches_release_metadata() -> None:
    project = _project_metadata()
    citation = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")

    assert project["authors"] == [{"name": "Gigi Cheng"}]
    assert project["urls"]["Repository"] == EXPECTED_REPOSITORY
    assert "cff-version: 1.2.0" in citation
    assert f'version: "{EXPECTED_VERSION}"' in citation
    assert 'title: "ReasonedOps"' in citation
    assert "license: Apache-2.0" in citation
    assert 'given-names: "Gigi"' in citation
    assert 'family-names: "Cheng"' in citation
    assert f'repository-code: "{EXPECTED_REPOSITORY}"' in citation
    assert "doi:" not in citation
    assert "orcid:" not in citation

import tomllib
from pathlib import Path

import reasoned_ops

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.4.4"
EXPECTED_REPOSITORY = "https://github.com/gigichengnc/reasoned-ops"
EXPECTED_DOI = "10.5281/zenodo.22051819"
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


def test_v144_cli_surface_is_registered() -> None:
    project = _project_metadata()

    assert project["name"] == "reasoned-ops"
    assert set(project["scripts"]) == EXPECTED_SCRIPTS


def test_pypi_distribution_metadata_is_explicit() -> None:
    project = _project_metadata()

    assert project["readme"] == {"file": "PYPI.md", "content-type": "text/markdown"}
    assert (PROJECT_ROOT / "PYPI.md").exists()
    assert project["requires-python"] == ">=3.11"
    assert "Programming Language :: Python :: 3.11" in project["classifiers"]
    assert "Programming Language :: Python :: 3.12" in project["classifiers"]


def test_legacy_namespace_is_removed() -> None:
    legacy_name = "ancova" + "_ops"
    assert not (PROJECT_ROOT / "src" / legacy_name).exists()

    for path in (PROJECT_ROOT / "src" / "reasoned_ops").rglob("*.py"):
        assert legacy_name not in path.read_text(encoding="utf-8")


def test_project_evolution_files_are_present() -> None:
    required = [
        PROJECT_ROOT / "original" / "README.md",
        PROJECT_ROOT / "docs" / "before-vs-after.md",
        PROJECT_ROOT / "docs" / "original-concept-audit.md",
        PROJECT_ROOT / "docs" / "model-decisions.md",
    ]

    for path in required:
        assert path.exists(), f"missing project-evolution file: {path.relative_to(PROJECT_ROOT)}"


def test_current_docs_do_not_reintroduce_identity_contradictions() -> None:
    contradiction_phrases = {
        "formerly called **ReasonedOps**",
        "formerly called ReasonedOps",
        "ReasonedOps is the renamed continuation of the completed v1 research/portfolio prototype formerly called **ReasonedOps**",
        "Treat `reasoned_ops` as temporary legacy compatibility only",
        "legacy `reasoned_ops` namespace",
    }
    external_rebuild_phrases = {
        "rebuild of an hkmu hackathon",
        "retrospective rebuild of an hkmu hackathon",
        "rebuilt independently",
        "was later rebuilt",
    }

    paths = [
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "PYPI.md",
        PROJECT_ROOT / "CITATION.cff",
        PROJECT_ROOT / "AGENTS.md",
    ]
    paths.extend((PROJECT_ROOT / "docs").glob("*.md"))

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for phrase in contradiction_phrases:
            assert phrase not in text, f"identity contradiction in {path.relative_to(PROJECT_ROOT)}"

        normalized = text.replace("**", "").lower()
        for phrase in external_rebuild_phrases:
            assert phrase not in normalized, (
                f"external-rebuild framing in {path.relative_to(PROJECT_ROOT)}"
            )


def test_current_identity_describes_project_evolution_not_external_rebuild() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    pypi = (PROJECT_ROOT / "PYPI.md").read_text(encoding="utf-8")
    citation = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")

    assert "originated from my participation in **HKMU Hackathon 2026**" in readme
    assert "A retrospective rebuild of an **HKMU Hackathon 2026**" not in readme
    assert "rebuilt independently" not in readme.lower()
    assert "originated from the author's participation in HKMU Hackathon 2026" in pypi
    assert "retrospective rebuild of an HKMU Hackathon 2026" not in pypi
    assert "originated from the author's participation in HKMU Hackathon 2026" in citation
    assert "retrospective rebuild of an HKMU Hackathon 2026" not in citation


def test_current_presentation_calls_operate_rule_based() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    comparison = (PROJECT_ROOT / "docs" / "before-vs-after.md").read_text(encoding="utf-8")

    assert "Rule-based request features + deterministic routing baseline" in readme
    assert "It does not claim a trained NLP model" in readme
    assert "Rule-based request features" in comparison
    assert "Transparent operational request intelligence" not in readme
    assert "Runnable FastAPI request-intelligence" not in readme


def test_current_readme_discloses_unmeasured_confounding_blind_spot() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "unmeasured_confounding_blind_spot" in readme
    assert "PASS" in readme
    assert "does **not** mean ReasonedOps detected hidden confounding" in readme
    assert "observed-data diagnostics cannot rule out unmeasured confounding" in readme


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
    assert f'doi: "{EXPECTED_DOI}"' in citation
    assert "10.5281/zenodo.22046490" not in citation
    assert "orcid:" not in citation

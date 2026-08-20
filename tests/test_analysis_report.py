import json

import pytest

from ancova_ops.analysis_report import main


def test_analysis_cli_emits_machine_readable_report(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--synthetic-n", "120", "--seed", "41", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["provenance"] == ["synthetic"]
    assert payload["sample"]["n_rows"] == 120
    assert payload["sample"]["n_complete_cases"] == 120
    assert len(payload["adjusted_estimates"]) == 4
    assert "department_by_covariate_interactions" in payload["diagnostics"]


def test_analysis_cli_rejects_invalid_alpha() -> None:
    with pytest.raises(ValueError, match="alpha"):
        main(["--synthetic-n", "100", "--alpha", "1.5"])

import pytest

from ancova_ops.analytics import fit_ancova
from ancova_ops.synthetic import generate_outcomes


def test_synthetic_data_is_explicitly_labelled() -> None:
    data = generate_outcomes(n=100, seed=7)
    assert set(data["data_provenance"]) == {"synthetic"}


def test_ancova_fit_contains_department_term() -> None:
    data = generate_outcomes(n=200, seed=7)
    result = fit_ancova(data)

    assert "C(department)" in result.formula
    assert "C(department)" in result.anova_table.index


def test_generator_rejects_tiny_dataset() -> None:
    with pytest.raises(ValueError):
        generate_outcomes(n=10)

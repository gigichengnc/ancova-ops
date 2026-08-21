from __future__ import annotations

from .analytics import fit_ancova
from .models import ServiceCase
from .routing import baseline_route
from .synthetic import generate_outcomes


def main() -> None:
    case = ServiceCase(
        case_id="demo-001",
        message=(
            "The air conditioner is leaking again. This is the third time and an elderly "
            "resident could slip on the wet floor."
        ),
        issue_category="air_conditioning",
        urgency=8.5,
        frustration=8.5,
        complexity=7.5,
        previous_related_cases=2,
        vulnerability_flag=True,
    )
    decision = baseline_route(case)

    print("=== Routing demonstration ===")
    print(f"Department: {decision.department}")
    print(f"Priority: {decision.priority}")
    print(f"Human review: {decision.requires_human_review}")
    print(f"Secondary notify: {decision.secondary_notify}")
    for reason in decision.reasons:
        print(f"- {reason}")

    print("\n=== Synthetic ANCOVA demonstration ===")
    data = generate_outcomes(n=500, seed=2026)
    result = fit_ancova(data)
    print(f"Formula: {result.formula}")
    print(result.anova_table.to_string())
    print("\nSynthetic data only — do not interpret as observed project performance.")


if __name__ == "__main__":
    main()

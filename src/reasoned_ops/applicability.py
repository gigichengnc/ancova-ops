from __future__ import annotations

import argparse
import json

from ancova_ops.applicability import (
    ApplicabilityDecision,
    EvaluationQuestion,
    assess_evaluation_question,
    assess_from_ancova_report,
)

__all__ = [
    "ApplicabilityDecision",
    "EvaluationQuestion",
    "assess_evaluation_question",
    "assess_from_ancova_report",
    "main",
]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Assess which evaluation method family is supportable for a declared ReasonedOps "
            "question. The gate returns use, caution, reject, or recommend_alternative."
        )
    )
    parser.add_argument(
        "--outcome-type",
        choices=["continuous", "binary", "time_to_event"],
        default="continuous",
    )
    parser.add_argument(
        "--comparison",
        choices=["department_outcome", "descriptive", "routing_policy"],
        default="department_outcome",
    )
    parser.add_argument(
        "--overlap-status",
        choices=["supported", "weak_overlap", "not_identifiable", "not_assessed"],
        default="supported",
    )
    parser.add_argument("--censored", action="store_true")
    parser.add_argument("--repeated-or-clustered", action="store_true")
    parser.add_argument("--causal-intent", action="store_true")
    parser.add_argument(
        "--interaction-flag",
        action="append",
        default=[],
        help="Name of a covariate with a material department-specific slope; may be repeated.",
    )
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    decision = assess_evaluation_question(
        EvaluationQuestion(
            outcome_type=args.outcome_type,
            comparison=args.comparison,
            overlap_status=args.overlap_status,
            censored=args.censored,
            repeated_or_clustered=args.repeated_or_clustered,
            causal_intent=args.causal_intent,
            interaction_flags=tuple(args.interaction_flag),
        )
    )

    if args.json:
        print(json.dumps(decision.to_dict(), indent=2, sort_keys=True))
    else:
        print("ReasonedOps evaluation applicability gate")
        print(f"Disposition: {decision.disposition}")
        print(f"Method family: {decision.method_family}")
        print("Reasons:")
        for reason in decision.reasons:
            print(f"- {reason}")
        print(f"Next step: {decision.next_step}")
        print(f"Boundary: {decision.interpretation_boundary}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

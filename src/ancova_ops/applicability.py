from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Literal

OutcomeType = Literal["continuous", "binary", "time_to_event"]
ComparisonType = Literal["department_outcome", "descriptive", "routing_policy"]
OverlapStatus = Literal["supported", "weak_overlap", "not_identifiable", "not_assessed"]
Disposition = Literal["use", "caution", "reject", "recommend_alternative"]


@dataclass(frozen=True, slots=True)
class EvaluationQuestion:
    """Declare the analytical question before selecting a method."""

    outcome_type: OutcomeType = "continuous"
    comparison: ComparisonType = "department_outcome"
    overlap_status: OverlapStatus = "not_assessed"
    censored: bool = False
    repeated_or_clustered: bool = False
    causal_intent: bool = False
    interaction_flags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ApplicabilityDecision:
    """High-level evaluation-method decision returned by the applicability gate."""

    disposition: Disposition
    method_family: str
    reasons: tuple[str, ...]
    next_step: str
    interpretation_boundary: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def assess_evaluation_question(question: EvaluationQuestion) -> ApplicabilityDecision:
    """Return use/caution/reject/alternative without forcing ANCOVA onto every question."""

    _validate_question(question)

    if (
        question.comparison == "department_outcome"
        and question.overlap_status == "not_identifiable"
    ):
        return ApplicabilityDecision(
            disposition="reject",
            method_family="no_adjusted_department_comparison",
            reasons=(
                "Department and case type are not separately identifiable from the declared "
                "routing design.",
                "Changing statistical model family cannot recover a department contrast that the "
                "observed design does not identify.",
            ),
            next_step=(
                "Do not rank departments. Collect overlapping comparable cases, restrict the "
                "estimand to a supported subset, or change the analytical question."
            ),
            interpretation_boundary=(
                "Raw descriptive summaries may still be reported, but they do not support an "
                "adjusted or causal department ranking."
            ),
        )

    if question.comparison == "routing_policy":
        return ApplicabilityDecision(
            disposition="recommend_alternative",
            method_family="offline_policy_evaluation",
            reasons=(
                "The question compares routing policies or counterfactual routing actions rather "
                "than ordinary observed department means.",
            ),
            next_step=(
                "Use logged-policy support/propensity-aware evaluation or a prospective policy "
                "experiment instead of ordinary ANCOVA."
            ),
            interpretation_boundary=(
                "Observed outcomes under one routing action are not automatically counterfactual "
                "outcomes for another action."
            ),
        )

    if question.causal_intent:
        return ApplicabilityDecision(
            disposition="recommend_alternative",
            method_family="causal_design_and_identification",
            reasons=(
                "The declared question asks for a causal effect, while ordinary observational "
                "case-mix adjustment only establishes model-based association.",
            ),
            next_step=(
                "Define the intervention, target estimand, assignment mechanism and identification "
                "assumptions before selecting an appropriate causal design or method."
            ),
            interpretation_boundary=(
                "A significant adjusted department term is not sufficient evidence that changing "
                "a route will cause the outcome to improve."
            ),
        )

    if question.comparison == "descriptive":
        return ApplicabilityDecision(
            disposition="use",
            method_family="descriptive_analysis",
            reasons=(
                "The declared goal is description rather than an adjusted group or policy effect.",
            ),
            next_step=(
                "Report counts, distributions and raw summaries with provenance and uncertainty "
                "where appropriate."
            ),
            interpretation_boundary=(
                "Descriptive differences should not be relabelled as adjusted, causal or "
                "staff-performance effects."
            ),
        )

    if question.outcome_type == "binary":
        return ApplicabilityDecision(
            disposition="recommend_alternative",
            method_family="logistic_type_model",
            reasons=(
                "The declared outcome is binary, so an ordinary continuous-outcome ANCOVA model "
                "does not match the outcome scale.",
            ),
            next_step=(
                "Use a logistic/binomial-type model or another binary-outcome method appropriate to "
                "the study design, while retaining overlap and case-mix checks."
            ),
            interpretation_boundary=(
                "Changing the link/distribution does not remove confounding or overlap requirements."
            ),
        )

    if question.outcome_type == "time_to_event" or question.censored:
        return ApplicabilityDecision(
            disposition="recommend_alternative",
            method_family="survival_time_to_event_model",
            reasons=(
                "The declared outcome is time-to-event or contains unresolved/censored cases, so "
                "ordinary completed-case resolution-time ANCOVA can discard follow-up information.",
            ),
            next_step=(
                "Use a survival/time-to-event framework that represents censoring explicitly and "
                "retains the same case-mix and comparison-support discipline."
            ),
            interpretation_boundary=(
                "Analysing only completed cases can produce a selected sample when unresolved cases "
                "remain under observation."
            ),
        )

    if question.repeated_or_clustered:
        return ApplicabilityDecision(
            disposition="recommend_alternative",
            method_family="clustered_or_hierarchical_model",
            reasons=(
                "Repeated or clustered observations violate the ordinary independence assumption "
                "when within-group dependence is material.",
            ),
            next_step=(
                "Use clustered standard errors, a hierarchical/mixed model, GEE, or another design "
                "that represents the declared dependence structure."
            ),
            interpretation_boundary=(
                "Treating repeated cases from the same site, team or customer as independent can "
                "understate uncertainty and distort inference."
            ),
        )

    reasons: list[str] = []
    if question.overlap_status == "not_assessed":
        reasons.append(
            "Department/case-type overlap has not been assessed, so the adjusted comparison should "
            "not yet be treated as cleared for use."
        )
    elif question.overlap_status == "weak_overlap":
        reasons.append(
            "The comparison is structurally estimable but practical department/case-type overlap is "
            "weak."
        )

    if question.interaction_flags:
        reasons.append(
            "Department-specific covariate slopes were flagged for: "
            + ", ".join(question.interaction_flags)
            + "."
        )

    if reasons:
        method_family = (
            "interaction_aware_regression"
            if question.interaction_flags
            else "regression_ancova_style"
        )
        next_step = (
            "Fit and interpret an interaction-aware model; do not hide the flagged slope "
            "differences behind a common-slope ANCOVA."
            if question.interaction_flags
            else (
                "Run/inspect the v0.6 overlap diagnostics before adjusted comparison."
                if question.overlap_status == "not_assessed"
                else "Restrict conclusions to supported case mix or collect more overlapping cases."
            )
        )
        return ApplicabilityDecision(
            disposition="caution",
            method_family=method_family,
            reasons=tuple(reasons),
            next_step=next_step,
            interpretation_boundary=(
                "Any adjusted result remains associational and should not be converted into a "
                "causal or staff-performance ranking."
            ),
        )

    return ApplicabilityDecision(
        disposition="use",
        method_family="regression_ancova_style",
        reasons=(
            "The declared outcome is continuous and uncensored.",
            "The department comparison has supported case-type overlap.",
            "No department-specific covariate slope has been declared as materially flagged.",
        ),
        next_step=(
            "Use the regression/ANCOVA-style outcome workflow with diagnostics, case-mix "
            "standardisation and non-causal reporting."
        ),
        interpretation_boundary=(
            "This gate says the method family is plausible for the declared question; it does not "
            "prove model correctness, absence of unmeasured confounding, or causal identification."
        ),
    )


def assess_from_ancova_report(
    report: Any,
    *,
    alpha: float = 0.05,
    censored: bool = False,
    repeated_or_clustered: bool = False,
    causal_intent: bool = False,
) -> ApplicabilityDecision:
    """Build the final gate decision from an existing ANCOVA Ops outcome report."""

    interaction_flags = tuple(
        str(name)
        for name, pvalue in report.interaction_checks.items()
        if math.isfinite(float(pvalue)) and float(pvalue) < alpha
    )
    return assess_evaluation_question(
        EvaluationQuestion(
            outcome_type="continuous",
            comparison="department_outcome",
            overlap_status=str(report.identifiability["status"]),
            censored=censored,
            repeated_or_clustered=repeated_or_clustered,
            causal_intent=causal_intent,
            interaction_flags=interaction_flags,
        )
    )


def _validate_question(question: EvaluationQuestion) -> None:
    if question.outcome_type not in {"continuous", "binary", "time_to_event"}:
        raise ValueError(f"unsupported outcome_type: {question.outcome_type}")
    if question.comparison not in {"department_outcome", "descriptive", "routing_policy"}:
        raise ValueError(f"unsupported comparison: {question.comparison}")
    if question.overlap_status not in {
        "supported",
        "weak_overlap",
        "not_identifiable",
        "not_assessed",
    }:
        raise ValueError(f"unsupported overlap_status: {question.overlap_status}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Assess which evaluation method family is supportable for a declared ANCOVA Ops "
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
        print("ANCOVA Ops evaluation applicability gate")
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

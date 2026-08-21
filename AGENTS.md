# AGENTS.md

## Purpose

This repository is developed collaboratively by humans and coding agents. Keep changes small, reviewable, evidence-oriented, and aligned with the completed research-project scope.

ReasonedOps is also a retrospective rebuild case study. Preserve the distinction between the reconstructed HKMU Hackathon starting concept under `original/` and the current implementation under `src/reasoned_ops/`.

## Product direction

ReasonedOps is an evidence-aware service-operations prototype organised around:

> **Operate → Audit → Evaluate**

It is not an "ANCOVA chatbot". ANCOVA/regression is one method inside the Evaluate layer.

The system separates:

1. request understanding and feature extraction;
2. explainable routing / human hand-off;
3. operational outcome collection;
4. auditable machine and human decision history;
5. comparison support / identifiability checks;
6. method applicability and guarded statistical evaluation;
7. separately evaluated adaptive or longitudinal research workflows.

Do not implement ANCOVA as a sentiment classifier or message filter. Do not force ANCOVA onto questions that need binary, survival, clustered, causal, policy-evaluation, or refusal handling.

## Development rules

- Use English for code, documentation, issues, PRs and commit messages.
- Use **ReasonedOps** as the canonical current project name.
- `src/reasoned_ops/` is the single canonical application package.
- Use `reasoned_ops` for Python imports and `reasoned-*` for public CLI examples.
- Do not recreate the removed `ancova_ops` compatibility package.
- Preserve **ANCOVA Ops** only where it describes genuine project history, such as pre-v1.1 changelog entries or the reconstructed original concept.
- Preserve **ANCOVA** where it names the actual statistical method.
- Prefer transparent baseline logic before complex ML.
- Do not claim project performance from synthetic data.
- Label synthetic, hand-authored, benchmark, pilot and measured data distinctly.
- Keep personal or resident data out of the repository.
- Add tests for new routing or analytical behaviour.
- Preserve human-readable explanations for routing decisions.
- Statistical code must state the model formula, applicability limits, and interpretation boundary.
- A supported model is not automatically a causal result or a staff-performance ranking.
- Do not silently rewrite historical material to make the original project look more correct than it was.

## Project scope

The finite research/portfolio prototype is complete. Further model-building should require a concrete user, research question, competition requirement, reuse request, or pilot opportunity rather than being added simply because more complexity is possible.

Real private-data pilot and production deployment remain separate post-project stages.

## Commands

```bash
pip install -e ".[dev]"
pytest
python -m reasoned_ops.demo
reasoned-showcase
reasoned-applicability --json
```

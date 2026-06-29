"""Evaluation result model for the PM Opportunity Agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    """Structured result of a completed job evaluation produced by the evaluator."""

    match_score: int
    recommendation: str
    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]
    red_flags: list[str]
    reasoning: str

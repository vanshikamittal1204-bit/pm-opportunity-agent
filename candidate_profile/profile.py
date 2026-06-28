"""Candidate profile data model for the PM Opportunity Agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateProfile:
    """Immutable representation of the candidate's professional profile and job preferences."""

    full_name: str
    current_location: str
    work_authorization: str
    willing_to_relocate: bool
    open_to_remote: bool
    years_of_experience: float
    current_role: str
    current_company: str
    target_roles: list[str]
    preferred_industries: list[str]
    preferred_locations: list[str]
    product_skills: list[str]
    technical_skills: list[str]
    tools: list[str]
    degree: str
    university: str
    graduation_year: int
    minimum_match_score: int
    preferred_company_stages: list[str]
    reject_keywords: list[str]
    resume_filename: str

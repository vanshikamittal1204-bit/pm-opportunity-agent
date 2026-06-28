"""Candidate profile data model for the PM Opportunity Agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateProfile:
    """Immutable representation of the candidate's professional profile and job preferences."""

    full_name: str
    target_role: str
    years_of_experience: float
    current_location: str
    work_authorization: str
    preferred_locations: list[str]
    required_skills: list[str]
    preferred_skills: list[str]
    industries: list[str]
    education: list[str]
    certifications: list[str]
    resume_path: str

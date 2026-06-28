"""Normalized job model for the PM Opportunity Agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedJob:
    """Canonical representation of a single PM opportunity after normalization."""

    job_id: str
    title: str
    company: str
    location: str
    remote: bool
    employment_type: str
    source: str
    url: str
    description: str
    posting_date: str
    experience_level: str
    salary: str
    tags: list[str]

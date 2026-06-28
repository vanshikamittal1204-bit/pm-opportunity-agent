"""Candidate profile loader for the PM Opportunity Agent."""

import yaml

from candidate_profile.profile import CandidateProfile


class CandidateProfileLoader:
    """Loads and validates a CandidateProfile from a YAML file."""

    def load(self, path: str) -> CandidateProfile:
        """Read, validate, and return a CandidateProfile from the given YAML file path."""
        data = self._read_yaml(path)
        self._validate_sections(data)
        self._validate_fields(data)
        return self._build_profile(data)

    # ── Reading ──────────────────────────────────────────────────────────────

    def _read_yaml(self, path: str) -> dict:
        """Open and parse the YAML file, raising FileNotFoundError if absent."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Candidate profile file not found: {path}")
        if not isinstance(data, dict):
            raise ValueError("Candidate profile YAML must contain a top-level mapping.")
        return data

    # ── Section validation ────────────────────────────────────────────────────

    def _validate_sections(self, data: dict) -> None:
        """Raise ValueError if any required top-level section is missing or not a mapping."""
        required = ["candidate", "experience", "preferences", "skills", "education", "resume"]
        for section in required:
            if section not in data or not isinstance(data[section], dict):
                raise ValueError(
                    f"Required section '{section}' is missing or invalid in the profile YAML."
                )

    # ── Field validation ──────────────────────────────────────────────────────

    def _validate_fields(self, data: dict) -> None:
        """Validate every required field within each section."""
        self._validate_candidate(data["candidate"])
        self._validate_experience(data["experience"])
        self._validate_preferences(data["preferences"])
        self._validate_skills(data["skills"])
        self._validate_education(data["education"])
        self._validate_resume(data["resume"])

    def _validate_candidate(self, section: dict) -> None:
        self._require_str(section, "candidate", "full_name")
        self._require_str(section, "candidate", "current_location")
        self._require_str(section, "candidate", "work_authorization")
        self._require_bool(section, "candidate", "willing_to_relocate")
        self._require_bool(section, "candidate", "open_to_remote")

    def _validate_experience(self, section: dict) -> None:
        self._require_number(section, "experience", "years_of_experience")
        self._require_str(section, "experience", "current_role")
        self._require_str(section, "experience", "current_company")

    def _validate_preferences(self, section: dict) -> None:
        self._require_list_of_str(section, "preferences", "target_roles")
        self._require_list_of_str(section, "preferences", "preferred_industries")
        self._require_list_of_str(section, "preferences", "preferred_locations")
        self._require_int(section, "preferences", "minimum_match_score")
        self._require_list_of_str(section, "preferences", "preferred_company_stages")
        self._require_list_of_str(section, "preferences", "reject_keywords")

    def _validate_skills(self, section: dict) -> None:
        self._require_list_of_str(section, "skills", "product_skills")
        self._require_list_of_str(section, "skills", "technical_skills")
        self._require_list_of_str(section, "skills", "tools")

    def _validate_education(self, section: dict) -> None:
        self._require_str(section, "education", "degree")
        self._require_str(section, "education", "university")
        self._require_int(section, "education", "graduation_year")

    def _validate_resume(self, section: dict) -> None:
        self._require_str(section, "resume", "resume_filename")

    # ── Type-checking helpers ─────────────────────────────────────────────────

    def _require_str(self, section: dict, section_name: str, field: str) -> None:
        if field not in section:
            raise ValueError(f"Missing required field '{field}' in section '{section_name}'.")
        if not isinstance(section[field], str):
            raise ValueError(
                f"Field '{field}' in section '{section_name}' must be a string."
            )

    def _require_bool(self, section: dict, section_name: str, field: str) -> None:
        if field not in section:
            raise ValueError(f"Missing required field '{field}' in section '{section_name}'.")
        if not isinstance(section[field], bool):
            raise ValueError(
                f"Field '{field}' in section '{section_name}' must be a boolean."
            )

    def _require_int(self, section: dict, section_name: str, field: str) -> None:
        if field not in section:
            raise ValueError(f"Missing required field '{field}' in section '{section_name}'.")
        value = section[field]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                f"Field '{field}' in section '{section_name}' must be an integer."
            )

    def _require_number(self, section: dict, section_name: str, field: str) -> None:
        if field not in section:
            raise ValueError(f"Missing required field '{field}' in section '{section_name}'.")
        value = section[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"Field '{field}' in section '{section_name}' must be a number."
            )

    def _require_list_of_str(self, section: dict, section_name: str, field: str) -> None:
        if field not in section:
            raise ValueError(f"Missing required field '{field}' in section '{section_name}'.")
        value = section[field]
        if not isinstance(value, list):
            raise ValueError(
                f"Field '{field}' in section '{section_name}' must be a list."
            )
        for item in value:
            if not isinstance(item, str):
                raise ValueError(
                    f"All items in '{field}' in section '{section_name}' must be strings."
                )

    # ── Profile construction ──────────────────────────────────────────────────

    def _build_profile(self, data: dict) -> CandidateProfile:
        """Map validated YAML data into a CandidateProfile instance."""
        candidate = data["candidate"]
        experience = data["experience"]
        preferences = data["preferences"]
        skills = data["skills"]
        education = data["education"]
        resume = data["resume"]

        return CandidateProfile(
            full_name=candidate["full_name"],
            current_location=candidate["current_location"],
            work_authorization=candidate["work_authorization"],
            willing_to_relocate=candidate["willing_to_relocate"],
            open_to_remote=candidate["open_to_remote"],
            years_of_experience=float(experience["years_of_experience"]),
            current_role=experience["current_role"],
            current_company=experience["current_company"],
            target_roles=preferences["target_roles"],
            preferred_industries=preferences["preferred_industries"],
            preferred_locations=preferences["preferred_locations"],
            product_skills=skills["product_skills"],
            technical_skills=skills["technical_skills"],
            tools=skills["tools"],
            degree=education["degree"],
            university=education["university"],
            graduation_year=education["graduation_year"],
            minimum_match_score=preferences["minimum_match_score"],
            preferred_company_stages=preferences["preferred_company_stages"],
            reject_keywords=preferences["reject_keywords"],
            resume_filename=resume["resume_filename"],
        )

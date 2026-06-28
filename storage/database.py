"""SQLite storage layer for the PM Opportunity Agent."""

import sqlite3
from typing import Optional


class DatabaseManager:
    """Manages SQLite database connections and operations for job storage."""

    def __init__(self, database_path: str) -> None:
        """Store the path to the SQLite database file."""
        self._database_path = database_path
        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Open a connection to the SQLite database. Does nothing if already connected."""
        if self._connection is not None:
            return
        self._connection = sqlite3.connect(self._database_path)

    def close(self) -> None:
        """Close the database connection if one is open."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def initialize_database(self) -> None:
        """Create the jobs table if it does not already exist."""
        if self._connection is None:
            raise RuntimeError("Database connection has not been established.")
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                job_id        TEXT PRIMARY KEY,
                title         TEXT NOT NULL,
                company       TEXT NOT NULL,
                location      TEXT,
                source        TEXT,
                url           TEXT,
                description   TEXT,
                discovered_at TEXT,
                match_score   REAL,
                strengths     TEXT,
                weaknesses    TEXT,
                recommendation TEXT,
                reasoning     TEXT,
                status        TEXT
            )
            """
        )
        self._connection.commit()

    def job_exists(self, job_id: str) -> bool:
        """Return True if the given job_id is already present in the database."""
        if self._connection is None:
            raise RuntimeError("Database connection has not been established.")
        cursor = self._connection.execute(
            "SELECT 1 FROM jobs WHERE job_id = ?", (job_id,)
        )
        return cursor.fetchone() is not None

    def insert_job(self, job: dict) -> None:
        """Insert one job record into the jobs table.

        Raises sqlite3.IntegrityError if job_id already exists.
        """
        if self._connection is None:
            raise RuntimeError("Database connection has not been established.")
        self._connection.execute(
            """
            INSERT INTO jobs (
                job_id, title, company, location, source, url, description,
                discovered_at, match_score, strengths, weaknesses,
                recommendation, reasoning, status
            ) VALUES (
                :job_id, :title, :company, :location, :source, :url, :description,
                :discovered_at, :match_score, :strengths, :weaknesses,
                :recommendation, :reasoning, :status
            )
            """,
            job,
        )
        self._connection.commit()

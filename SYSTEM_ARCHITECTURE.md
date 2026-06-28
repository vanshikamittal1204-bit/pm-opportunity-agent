# PM Opportunity Agent

## 1. Purpose

The PM Opportunity Agent is an autonomous system for continuous Product Management job discovery and evaluation.

It runs on a fixed schedule without human intervention. On each cycle it discovers new PM opportunities from multiple sources, normalizes them into a common structure, prevents duplicate processing, evaluates each opportunity against the candidate profile using Gemini, stores results persistently in SQLite, exports a human-readable view to Google Sheets, and sends Telegram notifications for only the highest-quality matches.

The system is designed to operate reliably and continuously, surfacing the most relevant opportunities to the candidate with no manual effort.

---

## 2. System Goals

**Automation** — The system runs end-to-end without human initiation. Each pipeline cycle is triggered by the scheduler and completes without intervention.

**Modularity** — Each component in the pipeline has a single, well-defined responsibility. Components are independent of each other and communicate through shared data structures, not direct coupling.

**Extensibility** — New job sources, evaluation criteria, storage backends, or notification channels can be added without restructuring the existing pipeline.

**Reliability** — A failure in any single component does not terminate the entire run. The system continues processing remaining jobs and sources even when one fails.

**Maintainability** — The codebase is written for readability. Configuration is externalized. Logic is not hardcoded. Each module is easy to understand, modify, and test independently.

---

## 3. Repository Structure

```
app/
sources/
services/
storage/
models/
candidate_profile/
prompts/
data/
tests/
```

### `app/`

Contains the entry point and the top-level pipeline orchestrator. Responsible for loading configuration, loading the candidate profile, invoking each pipeline stage in order, and handling run-level errors.

### `sources/`

Contains one module per job source. Each module is responsible for discovering raw job listings from a single external source such as LinkedIn, Wellfound, Greenhouse, Lever, YC Jobs, or company career pages. Sources are independent of each other.

### `services/`

Contains the business logic of the pipeline. Each service implements one stage: normalization, duplicate detection, Gemini evaluation, filtering, Google Sheets export, and Telegram notification.

### `storage/`

Contains all database interaction logic. Responsible for reading from and writing to the SQLite database. No other component interacts with the database directly.

### `models/`

Contains the data models shared across the system. Defines the structure of a normalized job, an evaluation result, and any other shared data objects. Models have no business logic.

### `candidate_profile/`

Contains the candidate's profile information including resume content, skills, experience, and preferences. This is the reference data used during Gemini evaluation.

### `prompts/`

Contains the prompt templates used to instruct Gemini. Prompts are stored as separate files and loaded at evaluation time. They are not hardcoded in the evaluation service.

### `data/`

Contains the SQLite database file and any other local data artifacts produced by the system at runtime.

### `tests/`

Contains all unit and integration tests. Test files mirror the structure of the modules they test.

---

## 4. High-Level Pipeline

```
Scheduler
    ↓
Load Configuration
    ↓
Load Candidate Profile
    ↓
Discover Jobs
    ↓
Normalize Jobs
    ↓
Duplicate Detection
    ↓
Gemini Evaluation
    ↓
Filtering
    ↓
SQLite Storage
    ↓
Google Sheets Update
    ↓
Telegram Notification
    ↓
End Run
```

---

## 5. Component Responsibilities

### Scheduler

Triggers the pipeline on a fixed interval defined in configuration. Responsible only for timing. Does not participate in any pipeline logic.

---

### Job Discovery

Executes each enabled source module. Each source independently fetches raw job listings from its target platform. Sources return raw data without normalizing or filtering it. Sources are enabled or disabled through configuration.

---

### Normalization

Accepts raw job data from any source and converts it into the common normalized job model. Ensures that all downstream components work with a consistent data structure regardless of the originating source.

---

### Duplicate Detection

Checks each normalized job against the SQLite database to determine whether it has already been processed. Jobs that already exist in the database are dropped before evaluation. SQLite is the authoritative source of truth for duplicate detection.

---

### Candidate Profile Loader

Reads the candidate profile from the `candidate_profile/` directory. Makes the profile available to the evaluation service. The profile includes the candidate's resume, skills, experience, and job preferences.

---

### Gemini Evaluation

Sends each new job to Gemini along with the candidate profile and the appropriate prompt template. Gemini returns a structured evaluation including a match score, recommendation, strengths, weaknesses, missing skills, red flags, confidence level, and reasoning. The evaluation service does not interpret or filter the results — it returns the raw Gemini output to the next stage.

---

### Filtering

Reads the configured score threshold. Passes only jobs whose match score meets or exceeds the threshold to the storage and notification stages. Jobs below the threshold are discarded.

---

### SQLite Storage

Writes all jobs that pass filtering to the SQLite database, including their normalized data and full evaluation results. Also records processing state and timestamps for each job. SQLite is the system's primary and persistent data store.

---

### Google Sheets Export

After a job is written to SQLite, exports a summary row to the configured Google Sheets spreadsheet. Google Sheets is a human-readable reporting layer only. It is not used for duplicate detection, state management, or any pipeline logic.

---

### Telegram Notification

Sends a formatted notification to the configured Telegram chat for each job that passed filtering, was stored in SQLite, and was exported to Google Sheets. Notifications are sent only for high-quality matches. Telegram is used only for alerting the candidate.

---

### Configuration Loader

Reads the system configuration at the start of each run. Makes all settings available to the pipeline. Configuration controls scheduler interval, enabled sources, score threshold, Telegram settings, Google Sheets settings, and Gemini settings.

---

## 6. Execution Flow

1. **Scheduler trigger** — The scheduler fires at the configured interval and initiates a new pipeline run.

2. **Configuration loading** — The configuration loader reads all settings from the configuration file. The pipeline does not proceed if configuration is invalid or missing required values.

3. **Candidate profile loading** — The candidate profile loader reads the candidate's resume, skills, experience, and preferences from the `candidate_profile/` directory.

4. **Source execution** — Each enabled source module runs independently. Each source fetches raw job listings from its platform. If one source fails, the others continue.

5. **Normalization** — The normalization service processes all raw job listings collected from all sources. Each listing is converted into the common normalized job model.

6. **Deduplication** — Each normalized job is checked against the SQLite database. Jobs that have already been processed are dropped. Only new, unseen jobs continue.

7. **Evaluation** — The Gemini evaluation service sends each new job to Gemini along with the candidate profile and the prompt template. Gemini returns a structured evaluation for each job.

8. **Filtering** — Jobs are compared against the configured score threshold. Jobs that do not meet the threshold are discarded. Jobs that meet or exceed the threshold continue.

9. **Storage** — Each job that passed filtering is written to the SQLite database with its normalized data, evaluation results, processing state, and timestamps.

10. **Reporting** — A summary row for each stored job is exported to the Google Sheets spreadsheet for human review.

11. **Notification** — A formatted Telegram message is sent for each stored job, alerting the candidate to the opportunity.

12. **Run completion** — The pipeline run ends. The scheduler waits for the next interval before triggering again.

---

## 7. Normalized Job Model

The normalized job model is the common data structure that all downstream components work with. Every source produces jobs in this format after normalization.

**title** — The job title as listed in the posting.

**company** — The name of the hiring company.

**location** — The city, region, or country of the role.

**remote** — Whether the role is fully remote, hybrid, or on-site.

**employment type** — Whether the role is full-time, part-time, contract, or other.

**source** — The name of the platform or source where the job was discovered.

**url** — The direct link to the job posting.

**description** — The full text of the job description.

**posting date** — The date the job was first published.

**experience level** — The seniority or years of experience required.

**salary** — The compensation range if disclosed.

**tags** — Keywords or categories associated with the role such as domain, industry, or required skills.

---

## 8. Evaluation Output Model

Gemini produces a structured evaluation for each job.

**Match Score** — A numeric score representing how well the candidate fits the role.

**Recommendation** — A brief directive indicating whether the candidate should pursue the opportunity.

**Strengths** — Specific aspects of the candidate's background that align well with the role.

**Weaknesses** — Specific gaps between the candidate's profile and the role requirements.

**Missing Skills** — Skills explicitly required by the role that are absent from the candidate's profile.

**Red Flags** — Concerns about the role itself such as unrealistic requirements, unclear scope, or misaligned expectations.

**Confidence** — Gemini's confidence level in the evaluation, given the completeness of the job description.

**Reasoning** — A narrative explanation of how the score and recommendation were reached.

---

## 9. Job Lifecycle

```
Discovered

↓

Normalized

↓

Duplicate Checked

↓

Evaluated

↓

Stored in SQLite

↓

Exported to Google Sheets

↓

Notification Sent

↓

Completed
```

---

## 10. Data Ownership

**Candidate profile** — Owned by the `candidate_profile/` directory. Read by the Candidate Profile Loader. Consumed by the Gemini Evaluation service. No other component modifies it.

**Prompts** — Owned by the `prompts/` directory. Read by the Gemini Evaluation service. Prompts are not modified at runtime.

**Configuration** — Owned by the configuration file at the project root. Read by the Configuration Loader at the start of each run. All components receive only the settings they need.

**Normalized jobs** — Produced by the Normalization service. Passed through the pipeline as the shared job representation. Written to SQLite by the Storage component.

**Evaluation results** — Produced by the Gemini Evaluation service. Attached to each normalized job. Written to SQLite alongside the job record. Summarized in Google Sheets.

**Notifications** — Produced by the Telegram Notification service. Sent externally. Not stored by the system.

---

## 11. Configuration Philosophy

All runtime behavior is controlled through configuration. Nothing that a user might need to change is hardcoded in the system.

Configuration controls:

* **Scheduler interval** — How frequently the pipeline runs.
* **Enabled sources** — Which job sources are active on a given run.
* **Score threshold** — The minimum match score required for a job to be stored and reported.
* **Telegram notifications** — Whether notifications are enabled and which chat to send to.
* **Google Sheets export** — Whether export is enabled and which spreadsheet to write to.
* **Gemini settings** — Which model to use and any generation parameters.

Configuration is loaded once at the start of each run. Components do not read configuration directly — they receive the values they need from the pipeline orchestrator.

---

## 12. Error Handling Strategy

The system is designed so that a failure in one component does not terminate the entire run.

**Source failure** — If a job source fails to fetch listings, that source is skipped. All other sources continue. The error is recorded and the pipeline proceeds with whatever jobs were successfully collected.

**Gemini failure** — If Gemini fails to evaluate a job, that job is skipped. Remaining jobs continue through evaluation. The failure is recorded against the specific job record.

**SQLite failure** — If a write to SQLite fails, the affected job is not exported to Google Sheets and no notification is sent for it. The failure is recorded. Other jobs in the same run are not affected.

**Google Sheets failure** — If the export to Google Sheets fails, the job remains in SQLite. A notification is still attempted. The Google Sheets failure is recorded but does not block the notification.

**Telegram failure** — If the Telegram notification fails, the job is already stored in SQLite and exported to Google Sheets. The notification failure is recorded. No retry is performed within the same run.

---

## 13. Retry Strategy

The system supports retry behaviour for transient failures such as network timeouts or temporary service unavailability.

Retries are configured, not hardcoded. The number of attempts and the delay between attempts are defined in configuration.

Retries apply to external calls only: source fetching, Gemini API calls, Google Sheets API calls, and Telegram API calls.

Retries are not applied to SQLite operations or internal logic.

If all retry attempts are exhausted, the component records the failure and the pipeline continues without the affected job or source.

---

## 14. Design Principles

**Modular** — Each component has a clearly defined boundary. It has one job and does only that job. Components are replaceable without affecting the rest of the pipeline.

**Single Responsibility** — No component takes on more than one responsibility. Discovery does not normalize. Storage does not evaluate. Notification does not store.

**Service-Oriented** — Components communicate through well-defined inputs and outputs. There is no shared mutable state between components. Data flows in one direction through the pipeline.

**Configuration Driven** — All behavior that may need to change is externalized to configuration. Source selection, thresholds, intervals, and API settings are all configurable.

**Extensible** — Adding a new source requires creating one new module in `sources/`. Adding a new output channel requires creating one new service in `services/`. No existing code needs to change.

**Fail Gracefully** — Errors are caught at the component level. The pipeline handles partial failures and continues processing. No single point of failure terminates a run.

**Readability First** — Code is written to be read. Naming is descriptive. Functions are small. Logic is not clever. A new contributor should be able to understand any module without needing to read the entire codebase.

---

## 15. Future Extensions

The architecture is designed to accommodate future capabilities without requiring structural changes.

Future additions may include:

* **Resume tailoring** — Generating a version of the candidate's resume optimized for a specific role.
* **Cover letter generation** — Producing a tailored cover letter for high-scoring opportunities.
* **Automatic applications** — Submitting applications on behalf of the candidate for approved opportunities.
* **Recruiter tracking** — Recording recruiter contact information and managing outreach history.
* **Company ranking** — Scoring companies based on candidate preferences, funding stage, or domain.
* **Learning from previous evaluations** — Using historical evaluation data to improve future scoring and filtering.
* **Analytics dashboard** — A reporting interface showing trends, source performance, and match quality over time.

These are future capabilities only. They are not part of the current system and are not reflected in the current implementation.

---

## 16. Non-Goals

The current system explicitly does not include:

* **Automatic job applications** — The system discovers and evaluates opportunities but does not apply to them.
* **Browser automation** — The system does not control a browser or simulate user interaction with job platforms.
* **Recruiter messaging** — The system does not contact recruiters or hiring managers on behalf of the candidate.
* **Resume rewriting** — The system does not modify or regenerate the candidate's resume.
* **Interview preparation** — The system does not generate interview questions, coaching content, or practice materials.

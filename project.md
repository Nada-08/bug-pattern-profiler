# Bug Pattern Profiler Notes

## Quick Split

This file has two parts:

- Part A: Project and code structure (what exists in this repo and what each code/data part does)
- Part B: Domain explanation (what NVD/CVE/CWE/KEV mean and why they matter)

---

## Part A: Project and Code Structure

This section is a quick orientation for new contributors.
It focuses on the three folders you will touch most often:

- packages/
- data/
- tests/

### Project Structure (High-Level)

```text
packages/
     common/
          settings.py
     ingestion/
          cli.py
          sources/
          normalize/
          chunking/
          storage/

data/
     raw/
          cisa_kev/
          nvd/
          test/
     normalized/
          cisa_kev/
          nvd/
     chunks/
          cisa_kev/
          nvd/

tests/
     test_nvd_normalizer.py
```

### packages/: Application Code

This is where the main Python code lives.

- packages/common/: shared config and settings used across modules.
- packages/ingestion/: ingestion pipeline code (fetch, normalize, chunk, store).
- packages/ingestion/sources/: source-specific data fetchers (NVD, CISA KEV).
- packages/ingestion/normalize/: converts source payloads into a consistent record shape.
- packages/ingestion/chunking/: turns normalized records into chunked text for downstream use.
- packages/ingestion/storage/: local storage helpers for writing/reading JSON and JSONL.
- packages/ingestion/cli.py: command entry point for running ingestion workflows.

Guidance for new contributors:

- Start here when changing behavior, fixing logic, or adding new ingestion features.
- If adding a new data source, follow the same pattern: source fetcher -> normalizer -> chunking/storage usage.

### data/: Pipeline Artifacts

This folder stores generated and sample data at each pipeline stage.

- data/raw/: original downloaded source payloads.
- data/normalized/: cleaned and unified records.
- data/chunks/: chunked text output.

Guidance for new contributors:

- Treat this as output/data artifacts, not core application logic.
- Use it to inspect pipeline results and verify transformations across stages.

### tests/: Validation and Safety Net

This folder contains tests for the codebase (for example, normalizer tests).

Also note: there are additional test files at repo root (for example, test_chunker.py, test_cisa_fetch.py, test_storage.py), so tests currently exist in both places.

Guidance for new contributors:

- Update or add tests whenever you change logic in packages/.
- When debugging ingestion behavior, check matching tests first to understand expected outputs.

### Pipeline in One Line

Ingestion means bringing data into your system in stages:

1. Fetch data from sources (NVD, KEV)
2. Normalize to a consistent schema
3. Chunk text for search/AI workflows

---

## Part B: Domain Explanation (NVD, CVE, CWE, KEV)

### Core Terms

- NVD = National Vulnerability Database
- CVE = Common Vulnerabilities and Exposures

Each CVE is:

- a known security bug
- with a unique ID like: CVE-2025-12345

### What Is CISA KEV?

CISA KEV = Known Exploited Vulnerabilities.

It is a list of vulnerabilities that are known to be exploited in the real world.

Why it's useful:

NVD tells you:

- what the vulnerability is

KEV tells you:

- this one is actively exploited / important in practice

So it is a very good second source.

### What Are NVD, CVE, CWE (In Plain English)

Forget code for a moment.

Imagine this:

There are thousands of security bugs in software:

- websites
- operating systems
- apps
- libraries

We need a global system to track them.

#### 1) CVE = the "ID card" of a bug

CVE = Common Vulnerabilities and Exposures.

Each bug gets a unique ID like:

- CVE-2026-20122

Think of it like:

- Student -> Student ID
- Bug -> CVE ID

Example:

- CVE-1999-0095

Means:

- "This is a specific known vulnerability"

#### 2) NVD = the "database with details"

NVD = National Vulnerability Database.

It stores detailed information about each CVE.

So:

- CVE = ID
- NVD = full description + details

Example (your real data):

You saw:

- CVE-1999-0095
- "The debug command in Sendmail is enabled..."

This means:

- There is a bug in Sendmail that allows attackers to run commands as root.

#### 3) CWE = the "type of mistake"

CWE = Common Weakness Enumeration.

This tells you what kind of bug it is.

Examples:

- CWE-79 -> Cross-Site Scripting (XSS)
- CWE-89 -> SQL Injection
- CWE-120 -> Buffer Overflow

Think of it like:

| Thing | Meaning |
|---|---|
| CVE | this exact bug |
| CWE | type/category of the bug |

### Putting It All Together

Example:

- CVE-2026-20122

NVD tells you:

- description
- severity
- references

CWE tells you:

- what kind of bug it is (e.g. file handling issue)

#### 4) CISA KEV = "this bug is actually being exploited"

KEV = Known Exploited Vulnerabilities.

This is VERY important.

It means:

- "Hackers are actively using this vulnerability in real attacks"

So:

| Source | Meaning |
|---|---|
| NVD | all known vulnerabilities |
| KEV | the dangerous ones used in real attacks |

### Why YOU Are Fetching This Data

Your project is:

- Bug Pattern Profiler

You are NOT just storing bugs.

You want to discover patterns like:

- "buffer overflows often happen in image parsers"
- "XSS vulnerabilities often occur in login forms"
- "deserialization bugs lead to remote code execution"

So your data is:

- Real-world bug examples

Each CVE = one example of a bug.

You are collecting thousands of them to learn patterns.

### Simple Analogy

Think of NVD as: a giant library of bug reports.

You are:

- downloading books (CVE records)
- cleaning them
- organizing them
- making them searchable

### Real Analogy

Think of your system like:

You are a cybersecurity researcher.

You:

- collect bug reports (NVD)
- mark important ones (KEV)
- organize them
- analyze patterns
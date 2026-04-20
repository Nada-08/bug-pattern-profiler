What each folder is for
packages/ingestion/ → code that fetches, normalizes, and chunks data
packages/common/ → shared config/settings
tests/ → test files
data/raw/ → original downloaded files
data/normalized/ → cleaned unified records
data/chunks/ → chunked text ready for embeddings later

pyproject.toml
What this did (simple explanation)
pydantic → for clean data models (very important later)
httpx → for API requests (NVD, CISA)
tenacity → retry logic (avoid crashes on network errors)
pytest → testing
dotenv → environment variables later

local_store.py
This module provides simple local file storage helpers for JSON data. It ensures parent directories exist before writing, saves and loads JSON files with UTF-8 encoding, and writes newline-delimited JSON records for streaming or batch data export.


NVD = National Vulnerability Database
CVE = Common Vulnerabilities and Exposures
Each CVE is:
a known security bug
with a unique ID like: CVE-2025-12345

Bug Pattern Profiler

That means you want to learn patterns like:

“XSS happens often in login forms”
“buffer overflows happen in image parsing”
“deserialization bugs lead to RCE”

To do that, you need:

lots of real vulnerabilities
structured data
NVD gives you exactly that


Simple analogy
Think of NVD as: a giant library of bug reports
You are:
downloading books (CVE records)
cleaning them
organizing them
making them searchable

data
 └── vulnerabilities (list)
      └── item
           └── cve
                ├── id
                ├── descriptions
                ├── metrics
                ├── weaknesses
                └── references
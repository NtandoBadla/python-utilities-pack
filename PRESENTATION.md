# IT Operations Automation Toolkit
### Python Capstone Project Presentation

---

## Slide 1 — Project Overview

**What is it?**
A full-stack IT automation toolkit built in Python, designed to help IT professionals automate repetitive operations, monitor systems, and process data — all from a single platform.

**Two ways to use it:**
- A **command-line interface** for running tasks directly from the terminal
- A **web application** (React + FastAPI) with a browser-based dashboard

**Core principle:** Replace manual, error-prone IT tasks with automated, logged, and reportable processes.

---

## Slide 2 — Project Structure

```
python-utilities-pack-1/
├── scripts/              # All Python automation modules
│   ├── main.py           # Central CLI entry point
│   ├── file_organizer.py
│   ├── log_analyzer.py
│   ├── system_health_checker.py
│   ├── data_validator.py
│   ├── report_generator.py
│   ├── performance_monitor.py
│   ├── api_client.py
│   └── config_manager.py
├── backend/              # FastAPI web server
│   ├── app.py
│   └── api/
│       ├── health.py
│       └── tools.py
├── frontend/             # React + TypeScript web UI
├── reports/              # Generated reports saved here
├── output/               # Cleaned CSV files saved here
└── logs/                 # All log files saved here
```

---

## Slide 3 — Feature 1: File Automation

**Script:** `file_organizer.py`

**What it does:**
- Scans a folder and sorts files into category subfolders automatically
  - Documents, Images, Audio, Videos, Spreadsheets, Presentations
- Detects **content-based duplicates** using MD5 hashing — finds identical files even if they have different names
- Detects **misnamed files** by reading magic bytes — flags a file named `.jpg` that is actually a PNG
- Records every move, skip, and error to `logs/file_organizer.log`

**Example CLI usage:**
```bash
python main.py organize --path "C:\Users\user\Downloads"
```

**Example output:**
```
Moved: report.pdf → Documents/
Moved: photo.jpg → Images/
⚠ Possibly misnamed: document.jpg — content looks like Documents not Images
[MD5 a1b2c3d4…] duplicate: backup.pdf, backup_copy.pdf
```

---

## Slide 4 — Feature 2: Log Analysis

**Script:** `log_analyzer.py`

**What it does:**
- Reads any system or application log file
- Uses **regular expressions** to detect INFO, WARNING, and ERROR entries — works with any log format (bracketed, plain, uppercase/lowercase)
- Groups repeated errors by normalising away timestamps and PIDs so the same fault is counted once
- Generates an error summary showing the top most-frequent errors
- Writes analysis results to `logs/log_analyzer.log`

**Example CLI usage:**
```bash
python main.py analyze-logs --file "C:\logs\app.log"
```

**Example output:**
```
Total Log Entries : 1,204
INFO Messages     : 980
WARNING Messages  : 186
ERROR Messages    : 38

REPEATED ERRORS (top 3)
  x12  ERROR Connection refused to database host
  x 8  ERROR Failed to authenticate user
  x 3  ERROR Disk quota exceeded
```

---

## Slide 5 — Feature 3: System Health Monitoring

**Script:** `system_health_checker.py`

**What it does:**
- Checks **CPU usage**, **memory usage**, and **disk usage** using the `psutil` library
- Compares each metric against configurable thresholds (default: 75% = WARNING, 90% = CRITICAL)
- Displays a clear HEALTHY / WARNING / CRITICAL status for each metric
- Handles unavailable metrics safely — returns UNKNOWN instead of crashing
- Thresholds are loaded from `config.json` and can be overridden with environment variables (for cloud/VM deployment)

**Example CLI usage:**
```bash
python main.py health
```

**Example output:**
```
Hostname: DESKTOP-IT01
Operating System: Windows
CPU Usage:    23.4% [HEALTHY]
Memory Usage: 78.1% [WARNING]
Disk Usage:   91.0% [CRITICAL]
```

---

## Slide 6 — Feature 4: User & Device Data Processing

**Script:** `data_validator.py`

**What it does:**
- Reads employee or device records from a CSV file
- Validates that all required fields are present: `name`, `email`, `department`, `device_id`
- Flags records with missing or whitespace-only fields as **invalid**
- Detects **duplicate records** using case-insensitive matching on name + email
- Writes only the clean, deduplicated records to a new output CSV file

**Example CLI usage:**
```bash
python main.py validate-csv --file "employees.csv" --output "output/cleaned.csv"
```

**Example output:**
```
Clean records:     142
Invalid records:     6  (missing email, missing device_id)
Duplicate records:   3
Cleaned file saved to: output/cleaned_records.csv
```

---

## Slide 7 — Feature 5: Reporting

**Script:** `report_generator.py`

**What it does:**
- Generates a structured health report in **4 formats**: JSON, CSV, HTML, plain text
- Every report includes:
  - Date and time generated
  - Hostname and operating system
  - Checks performed with results
  - Problems detected (e.g. "Memory Usage is WARNING at 78%")
  - Recommended actions (human-readable guidance, not just raw numbers)
- Reports are saved to the `reports/` folder and downloadable via the web UI

**Example CLI usage:**
```bash
python main.py health --report html
```

**HTML report includes:**
```
Generated: 2026-09-17T09:30:00
Hostname: DESKTOP-IT01

Checks Performed:
• CPU Usage: 23.4% [HEALTHY]
• Memory Usage: 78.1% [WARNING]
• Disk Usage: 91.0% [CRITICAL]

Problems Detected:
• Memory Usage is WARNING (78.1%)
• Disk Usage is CRITICAL (91.0%)

Recommended Actions:
• Close unused applications; consider adding more RAM.
• Free up disk space — remove temporary files.
```

---

## Slide 8 — Feature 6: Professional Development Practices

| Practice | How it was applied |
|---|---|
| **Functions & reusable modules** | Every feature is a separate importable module; `main.py` wires them all together |
| **Exception handling** | Every script handles `FileNotFoundError`, `PermissionError`, and general `Exception` — none crash silently |
| **Logging** | All scripts write timestamped logs to `logs/` using Python's `logging` module |
| **Configuration management** | `config_manager.py` loads `config.json`, validates values, supports environment variable overrides, and falls back to safe defaults |
| **Git & GitHub** | Repository tracked with Git throughout; `api_client.py` queries the live GitHub repo status |
| **Documentation** | Every module has a docstring explaining its purpose; every function has a docstring explaining parameters and return values |
| **Tests** | `test_data_validator.py` — 10 unit tests; `test_system_health_checker.py` — 10 unit tests; all 20 pass |

---

## Slide 9 — Web Application

**Backend:** FastAPI (`backend/`)
- REST API exposing all toolkit features as HTTP endpoints
- Endpoints: `/api/health`, `/api/performance`, `/api/file-organizer`, `/api/log-analyzer`, `/api/csv-validator`, `/api/reports/health`, `/api/full-scan`, `/api/public-ip`, `/api/github`

**Frontend:** React + TypeScript (`frontend/`)
- Browser-based dashboard for all features
- File upload for log analysis and CSV validation
- Downloadable reports and cleaned CSV files
- Live system health display

**Deployment ready:**
- `Dockerfile` included for containerised deployment
- `CLOUD_DEPLOYMENT.md` documents cloud setup steps
- Environment variable support in `config_manager.py` for cloud configuration

---

## Slide 10 — Summary

**6 features, all fully implemented and working:**

1. ✅ File Automation — organise, detect duplicates, detect misnames, log changes
2. ✅ Log Analysis — regex parsing, repeated error grouping, error summary
3. ✅ System Health Monitoring — CPU/memory/disk, threshold warnings, safe handling
4. ✅ Data Processing — CSV validation, duplicate detection, cleaned output
5. ✅ Reporting — 4 formats, date, checks, problems, recommendations
6. ✅ Professional Practices — modules, exception handling, logging, config, Git, docs, tests

**Technologies used:**
Python · FastAPI · React · TypeScript · psutil · unittest · Git · Docker

---

*IT Operations Automation Toolkit — Python Capstone Project*

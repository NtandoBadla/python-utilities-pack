<div align="center">

# 🐍 Python Utilities Pack

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code\&size=22\&pause=1000\&color=2E9EF7\&center=true\&vCenter=true\&width=650\&lines=IT+Operations+Automation+with+Python;System+Health+%7C+Performance+%7C+File+Automation;CSV+Validation+%7C+Log+Analysis+%7C+Web+Dashboard)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi\&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react\&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-Frontend-646CFF?logo=vite\&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows\&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Ready-2496ED?logo=docker\&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

A practical **IT Operations Automation Platform** built with Python, FastAPI, and React.

The project started as a collection of command-line Python utilities and evolved into an integrated system for performing common IT operations tasks such as **system health monitoring, performance analysis, file organization, log analysis, CSV validation, report generation, and API integration**.

The platform now provides both:

* 🖥️ **Command-line tools** for automation and scripting
* 🌐 **Web dashboard** for interacting with the tools through a professional interface

The project was developed progressively through four learning stages, moving from Python fundamentals to automation, troubleshooting, configuration management, testing, API development, and frontend integration.

---

## 📖 Table of Contents

* [Project Overview](#-project-overview)
* [Architecture](#-architecture)
* [Week 1 — Python Fundamentals](#-week-1--python-fundamentals)
* [Week 2 — Automation & Git Workflow](#-week-2--automation--git-workflow)
* [Week 3 — Troubleshooting, Configuration & Cloud](#-week-3--troubleshooting-configuration--cloud)
* [Week 4 — Capstone: IT Operations Automation Platform](#-week-4--capstone-it-operations-automation-platform)
* [Web Dashboard](#-web-dashboard)
* [API Endpoints](#-api-endpoints)
* [CSV Validation](#-csv-validation)
* [Project Structure](#-project-structure)
* [Configuration](#-configuration)
* [Installation](#-installation)
* [Running the CLI Tools](#-running-the-cli-tools)
* [Running the Web Platform](#-running-the-web-platform)
* [Running with Docker](#-running-with-docker)
* [Testing](#-testing)
* [Python Concepts Practised](#-python-concepts-practised)
* [IT Department Applications](#-it-department-applications)
* [Future Improvements](#-future-improvements)
* [Author](#-author)

---

## 📌 Project Overview

The **Python Utilities Pack** is designed around practical problems that an IT department may encounter during day-to-day operations.

The toolkit can:

* Monitor CPU, memory, and disk usage
* Identify processes consuming system resources
* Organize files automatically
* Analyze application/system logs
* Validate employee and device CSV records
* Detect duplicate records
* Generate health reports
* Retrieve public IP information
* Retrieve GitHub repository information
* Perform a complete system scan
* Expose automation functionality through a FastAPI backend
* Provide a React-based web dashboard for operating the tools

The project demonstrates how standalone Python scripts can evolve into a reusable automation platform with an API and web interface.

---

## 🏗️ Architecture

The platform follows a layered architecture:

```text
┌─────────────────────────────────────────────┐
│              React Web Dashboard            │
│                                             │
│ Dashboard │ Health │ Performance │ Reports  │
│ Files │ Logs │ CSV │ Activity │ Settings   │
└──────────────────────┬──────────────────────┘
                       │
                       │ REST API
                       ▼
┌─────────────────────────────────────────────┐
│               FastAPI Backend               │
│                                             │
│ /api/health                                 │
│ /api/performance                            │
│ /api/file-organizer                         │
│ /api/log-analyzer                           │
│ /api/csv-validator                          │
│ /api/reports                                │
│ /api/public-ip                              │
│ /api/github                                 │
│ /api/full-scan                              │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             Python Automation Layer         │
│                                             │
│ System Health │ Performance │ File Tools    │
│ Log Analyzer │ CSV Validator │ Reports      │
│ API Client │ Configuration                  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             Windows / File System           │
│             External APIs / Data            │
└─────────────────────────────────────────────┘
```

This separation allows the underlying Python utilities to remain reusable while the FastAPI backend provides a consistent interface for other applications.

---

# 🗂️ Week 1 — Python Fundamentals

Week 1 focused on Python fundamentals and building the first practical IT utilities.

| Tool                      | File                            | Purpose                                                               |
| ------------------------- | ------------------------------- | --------------------------------------------------------------------- |
| System Information Tool   | `scripts/system_information.py` | Displays computer name, OS, processor, architecture, and current user |
| Password Strength Checker | `scripts/password_checker.py`   | Categorizes a password as WEAK, MEDIUM, or STRONG                     |
| IT User & Device Manager  | `scripts/IT_manager.py`         | Command-line tool for managing basic employee and device records      |

### Example — System Information Tool

```text
=============================================
          SYSTEM INFORMATION
=============================================
Computer Name   : CPT001
Operating System: Windows
OS Version      : 10.0.26200
Processor       : Intel64 Family 6 Model 158 Stepping 9, GenuineIntel
Architecture    : AMD64
CPU Cores       : 4
Python Version  : 3.14.6
Current User    : Ntando.Badla
=============================================
```

---

# ⚙️ Week 2 — Automation & Git Workflow

Week 2 introduced automation, command-line arguments, regular expressions, system monitoring, and a structured Git/GitHub workflow.

| Tool                  | File                               | Purpose                                     |
| --------------------- | ---------------------------------- | ------------------------------------------- |
| File Organizer        | `scripts/file_organizer.py`        | Automatically sorts files into categories   |
| Regex Log Analyzer    | `scripts/log_analyzer.py`          | Parses logs and extracts useful information |
| System Health Checker | `scripts/system_health_checker.py` | Monitors CPU, memory, and disk usage        |

### Example — System Health Checker

```bash
python scripts/system_health_checker.py --all
```

Example output:

```text
===== SYSTEM HEALTH REPORT =====
Hostname: LAPTOP-17TBAUFS
Operating System: Windows
OS Version: 10.0.26200
CPU Usage: 50.8% [HEALTHY]
Memory Usage: 89.4% [WARNING]
Disk Usage: 95.4% [CRITICAL]
```

---

# 🛠️ Week 3 — Troubleshooting, Configuration & Cloud

Week 3 focused on making the toolkit more production-minded.

The project introduced:

* Structured logging
* Exception handling
* Unit testing
* Performance monitoring
* External configuration
* Environment-variable overrides
* Docker/container readiness
* Troubleshooting methodology

## 1. Troubleshooting Methodology

A consistent troubleshooting process was applied:

```text
Reproduce
   ↓
Read the Error
   ↓
Isolate the Problem
   ↓
Form a Hypothesis
   ↓
Test
   ↓
Fix
   ↓
Prevent Recurrence
```

See [`WEEK3_REPORT.md`](WEEK3_REPORT.md) for the detailed troubleshooting report.

---

## 2. Logging, Exception Handling & Testing

**Files:**

```text
scripts/system_health_checker.py
scripts/test_system_health_checker.py
```

The system health checker:

* Logs activity to `logs/system_health_checker.log`
* Handles individual metric failures
* Continues collecting other metrics where possible
* Uses configurable health thresholds
* Includes unit tests for status and formatting logic

Run the tests:

```bash
cd scripts
python -m unittest test_system_health_checker -v
```

---

## 3. Performance Monitoring

**File:**

```text
scripts/performance_monitor.py
```

The performance monitor provides:

* CPU-based process ranking
* Memory-based process ranking
* Configurable process limits
* A reusable `@timed` decorator

Example:

```bash
python scripts/performance_monitor.py --sort-by cpu --limit 5
```

Example output:

```text
===== TOP 5 PROCESSES BY CPU % =====
PID     Name                          CPU %
--------------------------------------------------
8000    python.exe                    61.60
9456    OneDrive.exe                  34.50
4596    OneDrive.Sync.Service.exe     27.60
```

---

## 4. Configuration Management

**Files:**

```text
scripts/config_manager.py
scripts/config.json
```

Example configuration:

```json
{
    "thresholds": {
        "warning": 75,
        "critical": 90
    },
    "performance": {
        "top_process_limit": 5,
        "sort_by": "cpu"
    }
}
```

Environment variables can override configuration without modifying the source code:

```bash
export HEALTH_WARNING_THRESHOLD=80
python scripts/system_health_checker.py --all
```

---

## 5. Cloud & Container Readiness

The project includes:

```text
requirements.txt
Dockerfile
CLOUD_DEPLOYMENT.md
```

The configuration and dependency structure allow the toolkit to be prepared for execution on different environments such as local machines, virtual machines, and containers.

---

# 🎓 Week 4 — Capstone: IT Operations Automation Platform

Week 4 brought the individual utilities together into an integrated IT automation platform.

The capstone includes:

* System health monitoring
* Performance monitoring
* CSV validation
* Structured reporting
* API integration
* File organization
* Log analysis
* Full system scanning
* FastAPI REST API
* React web dashboard

---

## 1. Structured Reporting

**File:**

```text
scripts/report_generator.py
```

Health information can be exported as:

* JSON
* CSV
* HTML
* Plain text

Example:

```bash
python main.py health --report html
```

Generated reports are stored in the project's `reports/` directory.

---

## 2. API Integration

**File:**

```text
scripts/api_client.py
```

The project integrates with external services to retrieve:

* Public IP information
* GitHub repository information

Examples:

```bash
python main.py ip
```

```bash
python main.py repo-status \
    --owner NtandoBadla \
    --repo python-utilities-pack
```

---

## 3. CSV Data Validation

**File:**

```text
scripts/data_validator.py
```

The CSV validator processes employee/device records and:

* Reads CSV records
* Checks required fields
* Detects missing data
* Detects duplicate records
* Produces cleaned records
* Generates a cleaned CSV output
* Supports automated validation through the web API

### Required fields

```text
name
email
department
device_id
```

### Sample dataset

The project includes:

```text
scripts/Spreadsheets/sample_employees.csv
```

The sample dataset intentionally contains both invalid and duplicate records.

For the current sample:

```text
Total records:       8
Clean records:       3
Invalid records:     3
Duplicate records:   2
```

The invalid records demonstrate:

```text
Bob Jones
Missing 'email'

Alice Brown
Missing 'department'

Charlie Lee
Missing 'device_id'
```

The duplicate records demonstrate duplicate employee/device entries for:

```text
John Smith
Jane Doe
```

The cleaned dataset can be generated with:

```bash
python main.py validate-csv \
    --file sample_employees.csv \
    --output output/cleaned.csv
```

---

# 🌐 Web Dashboard

The project now includes a React frontend connected to the FastAPI backend.

The dashboard provides a graphical interface for operating the Python automation tools without requiring users to execute every command manually.

### Dashboard sections

```text
Dashboard
System Health
Performance
File Organizer
Log Analyzer
CSV Validator
Reports
Activity Log
Settings
```

### System Health

Displays:

* Hostname
* Operating system
* OS version
* CPU usage
* Memory usage
* Disk usage
* Health status

Statuses include:

```text
HEALTHY
WARNING
CRITICAL
UNKNOWN
```

### Performance

Displays the processes consuming the most:

* CPU
* Memory

The number of processes and sorting method can be controlled through the API.

### File Organizer

Allows users to provide a folder path and execute the existing Python file organization functionality through the web interface.

The API returns:

* Files moved
* Files skipped
* Errors
* Summary information

### Log Analyzer

Users can upload a log file through the dashboard.

The backend then uses the existing Python log analyzer to return:

* INFO count
* WARNING count
* ERROR count
* Detected errors

### CSV Validator

Users can upload a CSV file directly from the dashboard.

The API returns:

* Clean records
* Invalid records
* Validation problems
* Duplicate records
* Record counts
* Cleaned CSV file
* Download link

### Reports

The dashboard can request system health reports in:

```text
JSON
CSV
HTML
Text
```

### API Integration

The dashboard also exposes functionality for:

* Public IP lookup
* GitHub repository information
* Full system scan

---

# 🔌 API Endpoints

The FastAPI backend provides the following REST endpoints:

| Method | Endpoint                                 | Purpose                                |
| ------ | ---------------------------------------- | -------------------------------------- |
| `GET`  | `/`                                      | API status                             |
| `GET`  | `/api`                                   | API information                        |
| `GET`  | `/api/health/`                           | System health                          |
| `GET`  | `/api/performance`                       | Top processes                          |
| `POST` | `/api/file-organizer`                    | Organize files                         |
| `POST` | `/api/log-analyzer`                      | Analyze uploaded log                   |
| `POST` | `/api/csv-validator`                     | Validate uploaded CSV                  |
| `GET`  | `/api/csv-validator/download/{filename}` | Download cleaned CSV                   |
| `POST` | `/api/reports/health`                    | Generate health report                 |
| `GET`  | `/api/reports/download/{filename}`       | Download report                        |
| `GET`  | `/api/public-ip`                         | Retrieve public IP                     |
| `GET`  | `/api/github`                            | Retrieve GitHub repository information |
| `GET`  | `/api/full-scan`                         | Run combined system scan               |

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 📁 Project Structure

```text
python-utilities-pack/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── health.py
│       └── tools.py
│
├── frontend/
│   ├── src/
│   │   ├── api.ts
│   │   ├── App.tsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/
│   ├── system_information.py
│   ├── password_checker.py
│   ├── IT_manager.py
│   ├── file_organizer.py
│   ├── log_analyzer.py
│   ├── system_health_checker.py
│   ├── test_system_health_checker.py
│   ├── performance_monitor.py
│   ├── config_manager.py
│   ├── config.json
│   ├── report_generator.py
│   ├── api_client.py
│   ├── data_validator.py
│   ├── test_data_validator.py
│   ├── Spreadsheets/
│   │   └── sample_employees.csv
│   └── main.py
│
├── output/
│   ├── csv_uploads/
│   ├── cleaned_csv/
│   └── uploads/
│
├── reports/
│
├── requirements.txt
├── Dockerfile
├── .gitignore
├── CLOUD_DEPLOYMENT.md
├── WEEK3_REPORT.md
├── DEMO_SCRIPT.md
├── REFLECTION.md
└── README.md
```

---

# ⚙️ Configuration

Settings are stored in:

```text
scripts/config.json
```

| Setting                         | Default | Description                             |
| ------------------------------- | ------: | --------------------------------------- |
| `thresholds.warning`            |    `75` | Usage percentage that triggers WARNING  |
| `thresholds.critical`           |    `90` | Usage percentage that triggers CRITICAL |
| `performance.top_process_limit` |     `5` | Number of processes displayed           |
| `performance.sort_by`           |   `cpu` | Sort by CPU or memory                   |

### Environment variables

| Environment Variable        | Overrides                       |
| --------------------------- | ------------------------------- |
| `HEALTH_WARNING_THRESHOLD`  | `thresholds.warning`            |
| `HEALTH_CRITICAL_THRESHOLD` | `thresholds.critical`           |
| `HEALTH_TOP_PROCESS_LIMIT`  | `performance.top_process_limit` |
| `HEALTH_SORT_BY`            | `performance.sort_by`           |

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/NtandoBadla/python-utilities-pack.git
```

Enter the project:

```bash
cd python-utilities-pack
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

---

# ▶️ Running the CLI Tools

From the project root:

### Week 1

```bash
python scripts/system_information.py
python scripts/password_checker.py
python scripts/IT_manager.py
```

### Week 2

```bash
python scripts/file_organizer.py --path "<folder-path>"
python scripts/log_analyzer.py --file "<log-file-path>"
python scripts/system_health_checker.py --all
```

### Week 3

```bash
python scripts/performance_monitor.py --sort-by cpu --limit 5
```

Run system health tests:

```bash
cd scripts
python -m unittest test_system_health_checker -v
```

### Week 4

From the `scripts/` directory:

```bash
cd scripts
python main.py health --report html
python main.py performance --limit 5
python main.py validate-csv --file Spreadsheets/sample_employees.csv --output ../output/cleaned.csv
python main.py ip
python main.py repo-status --owner NtandoBadla --repo python-utilities-pack
python main.py full-scan --report html
```

---

# 🌐 Running the Web Platform

The platform requires two processes:

```text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
Python Utilities
```

## 1. Start the backend

From the project root:

```powershell
python -m uvicorn backend.app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 2. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm run dev
```

Vite will provide the local frontend address in the terminal.

The frontend communicates with the FastAPI backend through REST API requests.

---

# 🧪 Testing

The project includes unit tests for important Python functionality.

### System Health Tests

```bash
cd scripts
python -m unittest test_system_health_checker -v
```

### CSV Validator Tests

```bash
python -m unittest test_data_validator -v
```

Testing covers validation logic, health status logic, and other core functionality.

---

# 🐳 Running with Docker

Build the image:

```bash
docker build -t it-toolkit .
```

Run the container:

```bash
docker run --rm it-toolkit
```

Override a health threshold:

```bash
docker run --rm \
    -e HEALTH_WARNING_THRESHOLD=80 \
    it-toolkit
```

See [`CLOUD_DEPLOYMENT.md`](CLOUD_DEPLOYMENT.md) for additional deployment concepts.

---

# 🧠 Python Concepts Practised

<div align="center">

![Variables](https://img.shields.io/badge/-Variables-2E9EF7?style=flat-square)
![Conditionals](https://img.shields.io/badge/-Conditionals-2E9EF7?style=flat-square)
![Loops](https://img.shields.io/badge/-Loops-2E9EF7?style=flat-square)
![Functions](https://img.shields.io/badge/-Functions-2E9EF7?style=flat-square)
![Regex](https://img.shields.io/badge/-Regex-2E9EF7?style=flat-square)
![argparse](https://img.shields.io/badge/-argparse-2E9EF7?style=flat-square)
![Logging](https://img.shields.io/badge/-Logging-2E9EF7?style=flat-square)
![Exception Handling](https://img.shields.io/badge/-Exception%20Handling-2E9EF7?style=flat-square)
![Unit Testing](https://img.shields.io/badge/-Unit%20Testing-2E9EF7?style=flat-square)
![Decorators](https://img.shields.io/badge/-Decorators-2E9EF7?style=flat-square)
![JSON Config](https://img.shields.io/badge/-JSON%20Config-2E9EF7?style=flat-square)
![REST API](https://img.shields.io/badge/-REST%20API-2E9EF7?style=flat-square)
![FastAPI](https://img.shields.io/badge/-FastAPI-2E9EF7?style=flat-square)
![React](https://img.shields.io/badge/-React-2E9EF7?style=flat-square)
![Docker](https://img.shields.io/badge/-Docker-2E9EF7?style=flat-square)
![Git & GitHub](https://img.shields.io/badge/-Git%20%26%20GitHub-2E9EF7?style=flat-square)

</div>

The project practises:

* Variables and data types
* Strings and operators
* Conditional logic
* `for` / `while` loops
* Lists, tuples, dictionaries, and sets
* Functions and modules
* Decorators
* Regular expressions
* Command-line arguments with `argparse`
* File and CSV processing
* JSON configuration
* Environment variables
* Structured logging
* Exception handling
* Unit testing with `unittest`
* REST API development
* FastAPI routing
* File uploads and downloads
* Frontend/backend integration
* React application development
* Git branching and commits
* GitHub workflows
* Docker/containerization concepts

---

# 💼 IT Department Applications

| Tool                      | Real-world use                                                |
| ------------------------- | ------------------------------------------------------------- |
| System Information Tool   | Quickly identify system specifications during support tickets |
| Password Strength Checker | Verify basic password policy compliance                       |
| IT User & Device Manager  | Maintain basic employee and device records                    |
| File Organizer            | Automate cleanup of shared drives or downloads folders        |
| Regex Log Analyzer        | Quickly investigate application and system logs               |
| System Health Checker     | Detect CPU, memory, and disk resource problems                |
| Performance Monitor       | Identify processes consuming excessive resources              |
| CSV Validator             | Validate employee/device records before importing them        |
| Report Generator          | Produce structured system health reports                      |
| Public IP Tool            | Support troubleshooting and network-related investigations    |
| GitHub API Client         | Retrieve repository information programmatically              |
| Web Dashboard             | Provide a centralized interface for IT operations             |
| FastAPI Backend           | Expose automation functionality to other applications         |

---

# 🚀 Future Improvements

The current platform provides the core automation and web dashboard functionality. Potential next improvements include:

* [ ] Persistent database for activity and audit history
* [ ] User authentication and role-based access
* [ ] Scheduled health checks using Windows Task Scheduler
* [ ] Automated email/Slack alerts for CRITICAL conditions
* [ ] Centralized monitoring of multiple computers
* [ ] PDF report generation
* [ ] Historical system-health charts
* [ ] Real-time process monitoring
* [ ] GitHub Actions CI pipeline
* [ ] Automated frontend/backend deployment
* [ ] Improved activity and audit logging
* [ ] Production deployment configuration

---

# 📚 Learning Progression

The project demonstrates a progression from basic scripting to application development:

```text
Python Fundamentals
        ↓
Automation Scripts
        ↓
Git & GitHub Workflow
        ↓
Troubleshooting
        ↓
Logging & Exception Handling
        ↓
Unit Testing
        ↓
Configuration Management
        ↓
API Integration
        ↓
Capstone CLI
        ↓
FastAPI Backend
        ↓
React Web Dashboard
        ↓
IT Operations Automation Platform
```

This progression demonstrates how individual scripts can be transformed into a reusable software platform.

---

# 📄 Project Documentation

Additional project documentation:

* [`WEEK3_REPORT.md`](WEEK3_REPORT.md) — Troubleshooting and configuration-management report
* [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) — Capstone demonstration walkthrough
* [`REFLECTION.md`](REFLECTION.md) — Individual project reflection
* [`CLOUD_DEPLOYMENT.md`](CLOUD_DEPLOYMENT.md) — Cloud and container deployment concepts

---

# 👨‍💻 Author

<div align="center">

**Ntando Badla**

Python • IT Automation • Software Development

[![GitHub](https://img.shields.io/badge/GitHub-NtandoBadla-181717?logo=github\&logoColor=white)](https://github.com/NtandoBadla)

![Profile Views](https://komarev.com/ghpvc/?username=NtandoBadla\&color=2E9EF7\&style=flat-square\&label=Repo+Views)

</div>

---

<div align="center">

### 🐍 Built with Python • ⚡ Powered by FastAPI • ⚛️ React Dashboard

</div>

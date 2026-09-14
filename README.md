<div align="center">

# 🐍 Python Utilities Pack

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=2E9EF7&center=true&vCenter=true&width=600&lines=IT+Automation+with+Python;File+Organizer+%7C+Log+Analyzer+%7C+Health+Checker;Configurable+%7C+Tested+%7C+Cloud-Ready)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Ready-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

A growing collection of practical Python utilities built to support everyday **IT department** tasks — from system diagnostics to log analysis and file automation.

Each week builds on the last: Week 1 covered Python fundamentals, Week 2 added automation and a proper Git/GitHub workflow, and Week 3 focused on making the toolkit **robust, configurable, and cloud-ready** — logging, testing, exception handling, externalized configuration, and container packaging.

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Week 1 — Python Fundamentals](#-week-1--python-fundamentals)
- [Week 2 — Automation & Git Workflow](#-week-2--automation--git-workflow)
- [Week 3 — Troubleshooting, Configuration & Cloud](#-week-3--troubleshooting-configuration--cloud)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Running the Scripts](#️-running-the-scripts)
- [Running with Docker](#-running-with-docker)
- [Python Concepts Practised](#-python-concepts-practised)
- [IT Department Applications](#-it-department-applications)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 📌 Project Overview

The **Python Utilities Pack** is a set of command-line tools written to solve practical problems an IT department deals with day to day — checking system health, cleaning up messy folders, parsing log files, and keeping basic records of users and devices.

The project is organised by week, tracking progress from Python fundamentals through automation scripting, Git/GitHub collaboration, and finally professional practices like configuration management and cloud-readiness.

---

## 🗂️ Week 1 — Python Fundamentals

| Tool | File | Purpose |
|---|---|---|
| System Information Tool | `scripts/system_information.py` | Displays computer name, OS, processor, architecture, and current user |
| Password Strength Checker | `scripts/password_checker.py` | Categorises a password as WEAK, MEDIUM, or STRONG against basic security requirements |
| IT User & Device Manager | `scripts/IT_manager.py` | Command-line tool for managing basic employee and device records |

**Example — System Information Tool:**

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

## ⚙️ Week 2 — Automation & Git Workflow

Week 2 shifted focus to **automation scripts**, **command-line arguments**, and a proper **Git/GitHub collaboration workflow** — feature branches, pull requests, and code review — rather than working directly on `main`.

| Tool | File | Purpose |
|---|---|---|
| File Organizer | `scripts/file_organizer.py` | Scans a directory and automatically sorts files into subfolders by type |
| Regex Log Analyzer | `scripts/log_analyzer.py` | Parses log files with regular expressions to extract errors, timestamps, and IP addresses |
| System Health Checker | `scripts/system_health_checker.py` | Reports CPU, memory, and disk usage, flagged as HEALTHY / WARNING / CRITICAL |

**Example — System Health Checker:**

```bash
python scripts/system_health_checker.py --all
```

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

## 🛠️ Week 3 — Troubleshooting, Configuration & Cloud

Week 3 focused on making the toolkit production-minded: diagnosable when something goes wrong, configurable without editing code, and portable across machines and environments.

### 1. Troubleshooting Methodology

Applied a consistent method to real and deliberately-broken bugs: reproduce → read the error → isolate → hypothesise → test → fix → prevent. See [`WEEK3_REPORT.md`](WEEK3_REPORT.md) for a full write-up, including a real issue this process uncovered (elevated CPU usage traced to OneDrive struggling to sync on a near-full disk).

### 2. Logging, Exception Handling & Testing

**File:** `scripts/system_health_checker.py`, `scripts/test_system_health_checker.py`

- Every run now logs to `logs/system_health_checker.log` with timestamps, in addition to console output.
- Each metric (hostname, CPU, memory, disk) is collected independently with its own error handling — one failure no longer crashes the whole script.
- 10 unit tests cover the status-threshold logic and formatting.

```bash
cd scripts
python -m unittest test_system_health_checker -v
```

### 3. Performance Monitoring

**File:** `scripts/performance_monitor.py`

- `@timed` — a reusable decorator that logs how long any function takes to run.
- `top_processes()` — lists the processes consuming the most CPU or memory right now.

```bash
python scripts/performance_monitor.py --sort-by cpu --limit 5
```

```text
===== TOP 5 PROCESSES BY CPU % =====
PID     Name                          CPU %
--------------------------------------------------
8000    python.exe                    61.60
9456    OneDrive.exe                  34.50
4596    OneDrive.Sync.Service.exe     27.60
```

### 4. Configuration Management

**File:** `scripts/config_manager.py`, `scripts/config.json`

Thresholds and paths were externalized from hardcoded values into `config.json`, with validation and environment-variable overrides for cloud/VM deployment.

```json
{
    "thresholds": { "warning": 75, "critical": 90 },
    "performance": { "top_process_limit": 5, "sort_by": "cpu" }
}
```

Override without touching a file — e.g. for a deployed environment:

```bash
export HEALTH_WARNING_THRESHOLD=80
python scripts/system_health_checker.py --all
```

### 5. Cloud & Container Readiness

**Files:** `requirements.txt`, `Dockerfile`, `CLOUD_DEPLOYMENT.md`

The toolkit is now packaged so it runs identically on a laptop, a VM, or a container platform. See [`CLOUD_DEPLOYMENT.md`](CLOUD_DEPLOYMENT.md) for VM vs. container concepts and scalability notes.

---

**Weekly deliverable:** [`WEEK3_REPORT.md`](WEEK3_REPORT.md) — full troubleshooting and configuration-management report.

---

## 📁 Project Structure

```text
python-utilities-pack/
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
│   └── config.json
│
├── requirements.txt
├── Dockerfile
├── .gitignore
├── CLOUD_DEPLOYMENT.md
├── WEEK3_REPORT.md
└── README.md
```

---

## ⚙️ Configuration

Settings live in `scripts/config.json`, auto-created with defaults on first run:

| Setting | Default | Description |
|---|---|---|
| `thresholds.warning` | 75 | % usage that triggers a WARNING status |
| `thresholds.critical` | 90 | % usage that triggers a CRITICAL status |
| `performance.top_process_limit` | 5 | Number of processes shown by the performance monitor |
| `performance.sort_by` | `cpu` | Sort top processes by `cpu` or `memory` |

Any setting can be overridden with an environment variable (useful for cloud/VM deployment without editing files):

| Environment Variable | Overrides |
|---|---|
| `HEALTH_WARNING_THRESHOLD` | `thresholds.warning` |
| `HEALTH_CRITICAL_THRESHOLD` | `thresholds.critical` |
| `HEALTH_TOP_PROCESS_LIMIT` | `performance.top_process_limit` |
| `HEALTH_SORT_BY` | `performance.sort_by` |

---

## ▶️ Running the Scripts

Install dependencies:

```bash
pip install -r requirements.txt
```

From the project directory:

```bash
# Week 1
python scripts/system_information.py
python scripts/password_checker.py
python scripts/IT_manager.py

# Week 2
python scripts/file_organizer.py --path "<folder-path>"
python scripts/log_analyzer.py --file "<log-file-path>"
python scripts/system_health_checker.py --all

# Week 3
python scripts/performance_monitor.py --sort-by cpu --limit 5
cd scripts && python -m unittest test_system_health_checker -v
```

---

## 🐳 Running with Docker

```bash
# Build the image
docker build -t it-toolkit .

# Run with default thresholds
docker run --rm it-toolkit

# Override a threshold at run time — no rebuild needed
docker run --rm -e HEALTH_WARNING_THRESHOLD=80 it-toolkit
```

---

## 🧠 Python Concepts Practised

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
![Docker](https://img.shields.io/badge/-Docker-2E9EF7?style=flat-square)
![Git & GitHub](https://img.shields.io/badge/-Git%20%26%20GitHub-2E9EF7?style=flat-square)

</div>

* Variables, data types, strings, operators, conditional logic
* `for` / `while` loops, lists, tuples, dictionaries
* Functions, modules, and decorators (`@timed`)
* Regular expressions (`re`) and `argparse`
* Structured logging (`logging`) and exception handling (`try`/`except`)
* Unit testing (`unittest`)
* JSON-based configuration with validation and environment-variable overrides
* Containerization concepts (`Dockerfile`)
* Git branching, commits, and pull request workflows

---

## 💼 IT Department Applications

| Tool | Real-world use |
|---|---|
| System Information Tool | Quickly identify basic computer/system specs during support tickets |
| Password Strength Checker | Enforce/verify password policy compliance |
| IT User & Device Manager | Maintain basic employee and equipment records |
| File Organizer | Automate cleanup of shared drives or downloads folders |
| Regex Log Analyzer | Rapidly triage system/application logs for errors and anomalies |
| System Health Checker | Monitor CPU, memory and disk health for early warning of resource issues |
| Performance Monitor | Identify exactly which processes are consuming system resources |
| Configuration Management | Tune alert thresholds per-deployment without editing code |

---

## 🚀 Future Improvements

- [ ] Add persistent data storage (JSON/CSV/SQLite)
- [ ] Add scheduled/automated health check runs (cron / Task Scheduler)
- [ ] Send alerts (email/Slack webhook) on CRITICAL status
- [ ] Centralize reports from multiple machines
- [ ] Export reports (CSV/PDF) from log analyzer and health checker
- [ ] Add a simple GUI or web dashboard
- [ ] CI pipeline (GitHub Actions) to lint and test on every PR

---

## 👨‍💻 Author

<div align="center">

**Ntando Badla**
Python & IT Automation — Week 3

![Profile Views](https://komarev.com/ghpvc/?username=NtandoBadla&color=2E9EF7&style=flat-square&label=Repo+Views)

</div>
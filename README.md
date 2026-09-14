<div align="center">

# 🐍 Python Utilities Pack

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=2E9EF7&center=true&vCenter=true&width=600&lines=IT+Automation+with+Python;File+Organizer+%7C+Log+Analyzer+%7C+Health+Checker;Built+during+a+Python+IT+Automation+Bootcamp)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Made with](https://img.shields.io/badge/Made%20with-%E2%98%95%20%26%20Python-orange)

</div>

---

A growing collection of practical Python utilities built to support everyday **IT department** tasks — from system diagnostics to log analysis and file automation.

Each week builds on the last, moving from core Python fundamentals toward real command-line automation tools, proper Git workflows, and professional documentation.

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Week 1 — Python Fundamentals](#-week-1--python-fundamentals)
  - [System Information Tool](#1-system-information-tool)
  - [Password Strength Checker](#2-password-strength-checker)
  - [IT User & Device Manager](#3-it-user--device-manager)
- [Week 2 — Automation & Git Workflow](#-week-2--automation--git-workflow)
  - [File Organizer](#1-file-organizer)
  - [Regex Log Analyzer](#2-regex-log-analyzer)
  - [Command-Line System Health Checker](#3-command-line-system-health-checker)
- [Project Structure](#-project-structure)
- [Running the Scripts](#️-running-the-scripts)
- [Python Concepts Practised](#-python-concepts-practised)
- [IT Department Applications](#-it-department-applications)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 📌 Project Overview

The **Python Utilities Pack** is a set of command-line tools written to solve practical problems an IT department deals with day to day — checking system health, cleaning up messy folders, parsing log files, and keeping basic records of users and devices.

The project is organised by week, tracking progress from Python fundamentals through to automation scripting and collaborative Git workflows (branches, pull requests, and code review).

---

## 🗂️ Week 1 — Python Fundamentals

### 1. System Information Tool

**File:** `scripts/system_information.py`

Displays information about the computer running the program.

Information includes:

* Computer name
* Operating system
* OS version
* Processor
* System architecture
* Number of CPU cores
* Python version
* Current user

**Example:**

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

### 2. Password Strength Checker

**File:** `scripts/password_checker.py`

Checks a password against basic security requirements:

* Minimum 8 characters
* Uppercase letters
* Lowercase letters
* Numbers
* Special characters

Categorises passwords as **WEAK**, **MEDIUM**, or **STRONG**, and identifies any missing requirements.

---

### 3. IT User & Device Manager

**File:** `scripts/IT_manager.py`

A command-line tool for managing basic employee and IT device records.

```text
=============================================
          IT USER & DEVICE MANAGER
=============================================
1. Add employee
2. View employees
3. Search employee
4. Add device
5. View devices
6. Exit
=============================================
```

---

## ⚙️ Week 2 — Automation & Git Workflow

Week 2 shifted focus to **automation scripts**, **command-line arguments**, and a proper **Git/GitHub collaboration workflow** — feature branches, pull requests, and code review — rather than working directly on `main`.

### 1. File Organizer

**File:** `scripts/file_organizer.py`

Scans a target directory and automatically sorts files into subfolders based on file type (e.g. Documents, Images, Scripts, Archives), reducing manual folder cleanup.

**Example:**

```bash
python scripts/file_organizer.py --path "C:\Users\user\Downloads"
```

```text
=============================================
          FILE ORGANIZER
=============================================
Scanning: C:\Users\user\Downloads
Moved 12 files → Documents/
Moved 5 files  → Images/
Moved 3 files  → Archives/
Organization complete.
=============================================
```

---

### 2. Regex Log Analyzer

**File:** `scripts/log_analyzer.py`

Parses log files using regular expressions to extract useful information such as error counts, timestamps, and IP addresses — helpful for quickly triaging system or application logs.

**Example:**

```bash
python scripts/log_analyzer.py --file "logs/system.log"
```

```text
=============================================
          LOG ANALYSIS REPORT
=============================================
Total lines scanned : 4,210
ERROR entries        : 37
WARNING entries       : 112
Most frequent IP      : 192.168.1.14
=============================================
```

---

### 3. Command-Line System Health Checker

**File:** `scripts/system_health_checker.py`

Checks real-time system health — CPU, memory, and disk usage — and flags each as **HEALTHY**, **WARNING**, or **CRITICAL** based on usage thresholds. Supports command-line flags for flexible reporting.

**Example:**

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

**Available flags:**

| Flag | Description |
|------|-------------|
| `--system` | Display system information only |
| `--resources` | Display CPU, memory and disk usage only |
| `--all` | Display full health report (default if no flag given) |

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
│   └── system_health_checker.py
│
└── README.md
```

---

## ▶️ Running the Scripts

Make sure Python 3.10+ is installed, and install dependencies where needed:

```bash
pip install psutil
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
```

---

## 🧠 Python Concepts Practised

<div align="center">

![Variables](https://img.shields.io/badge/-Variables-2E9EF7?style=flat-square)
![Data Types](https://img.shields.io/badge/-Data%20Types-2E9EF7?style=flat-square)
![Conditionals](https://img.shields.io/badge/-Conditionals-2E9EF7?style=flat-square)
![Loops](https://img.shields.io/badge/-Loops-2E9EF7?style=flat-square)
![Functions](https://img.shields.io/badge/-Functions-2E9EF7?style=flat-square)
![Dictionaries](https://img.shields.io/badge/-Dictionaries-2E9EF7?style=flat-square)
![Error Handling](https://img.shields.io/badge/-Error%20Handling-2E9EF7?style=flat-square)
![Regex](https://img.shields.io/badge/-Regex-2E9EF7?style=flat-square)
![argparse](https://img.shields.io/badge/-argparse-2E9EF7?style=flat-square)
![File I/O](https://img.shields.io/badge/-File%20I%2FO-2E9EF7?style=flat-square)
![Git & GitHub](https://img.shields.io/badge/-Git%20%26%20GitHub-2E9EF7?style=flat-square)
![Automation](https://img.shields.io/badge/-Automation-2E9EF7?style=flat-square)

</div>

* Variables, data types, strings, operators
* Conditional logic and logical expressions
* `for` and `while` loops
* Lists, tuples, dictionaries
* Functions and modules
* User input and basic validation
* Error handling (`try` / `except`)
* Regular expressions (`re`)
* Command-line arguments (`argparse`)
* Working with the file system (`os`, `shutil`)
* System introspection (`platform`, `socket`, `psutil`)
* Git branching, commits, and pull request workflows

---

## 💼 IT Department Applications

| Tool | Real-world use |
|------|----------------|
| System Information Tool | Quickly identify basic computer/system specs during support tickets |
| Password Strength Checker | Enforce/verify password policy compliance |
| IT User & Device Manager | Maintain basic employee and equipment records |
| File Organizer | Automate cleanup of shared drives or downloads folders |
| Regex Log Analyzer | Rapidly triage system/application logs for errors and anomalies |
| System Health Checker | Monitor CPU, memory and disk health for early warning of resource issues |

---

## 🚀 Future Improvements

- [ ] Add persistent data storage (JSON/CSV/SQLite)
- [ ] Add automated unit tests (`pytest`)
- [ ] Add stronger input validation across all tools
- [ ] Add password input masking
- [ ] Add scheduled/automated health check runs
- [ ] Export reports (CSV/PDF) from log analyzer and health checker
- [ ] Add a simple GUI or web dashboard
- [ ] CI pipeline (GitHub Actions) to lint and test on every PR

---

## 👨‍💻 Author

<div align="center">

**Ntando Badla**
Python & IT Automation — Week 2

![Profile Views](https://komarev.com/ghpvc/?username=NtandoBadla&color=2E9EF7&style=flat-square&label=Repo+Views)

</div>

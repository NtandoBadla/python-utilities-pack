# 🐍 Python Utilities Pack

A collection of three practical Python utilities developed as part of **Week 1: Python Fundamentals**.

The project demonstrates how Python can be used to automate simple tasks that could support an IT department.

---

## 📌 Project Overview

The Python Utilities Pack contains three command-line tools:

1. **System Information Tool** — Collects useful information about a computer.
2. **Password Strength Checker** — Checks whether a password meets basic security requirements.
3. **IT User & Device Manager** — Manages employee and device records.

The project focuses on applying Python fundamentals to practical IT-related problems.

---

## 🛠️ Utilities

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

Checks a password against basic security requirements.

The tool checks for:

* Minimum 8 characters
* Uppercase letters
* Lowercase letters
* Numbers
* Special characters

It categorises passwords as:

* **WEAK**
* **MEDIUM**
* **STRONG**

The tool also identifies requirements that are missing.

---

### 3. IT User & Device Manager

**File:** `scripts/IT_manager.py`

A command-line tool for managing basic employee and IT device records.

The system allows users to:

* Add employees
* View employees
* Search for employees
* Add devices
* View devices
* Exit the application

Example:

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

## 🧠 Python Concepts Practised

This project applies the following Python fundamentals:

* Variables
* Data types
* Strings
* Operators
* Conditional statements
* Logical expressions
* `for` loops
* `while` loops
* Lists
* Tuples
* Dictionaries
* Functions
* Modules
* User input
* Basic validation
* Error handling
* Reusable code

---

## 📁 Project Structure

```text
python-utilities-pack/
│
├── scripts/
│   ├── system_information.py
│   ├── password_checker.py
│   └── IT_manager.py
│
└── README.md
```

---

## ▶️ Running the Scripts

Make sure Python is installed on your computer.

From the project directory, run:

### System Information

```bash
python scripts/system_information.py
```

### Password Checker

```bash
python scripts/password_checker.py
```

### IT User & Device Manager

```bash
python scripts/IT_manager.py
```

---

## 💼 IT Department Applications

These utilities demonstrate how simple Python programs can assist with everyday IT tasks.

### System Information Tool

Can help IT support staff quickly identify basic computer and system information.

### Password Strength Checker

Can help users identify whether passwords meet basic security requirements.

### IT User & Device Manager

Can help maintain basic records of employees and their assigned IT equipment.

---

## 📚 Learning Outcome

The project demonstrates the progression from basic Python syntax to building small, functional IT automation tools.

The goal was not only to learn Python concepts, but to apply those concepts to practical problems that could occur in an IT environment.

---

## 🚀 Future Improvements

Possible improvements include:

* Add persistent data storage
* Add stronger input validation
* Add exception handling
* Add automated tests
* Add device assignment validation
* Add employee deletion and editing
* Add password input masking
* Export employee and device records
* Add a graphical user interface

---

## 👨‍💻 Author

**Ntando Badla**

Python Fundamentals — Week 1

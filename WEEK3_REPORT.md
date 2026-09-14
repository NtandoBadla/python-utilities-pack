\# Week 3 Report: Troubleshooting \& Configuration Management



\*\*Project:\*\* Python Utilities Pack — IT Operations Automation Toolkit

\*\*Author:\*\* Ntando Badla

\*\*Week:\*\* 3 — Troubleshooting, Configuration Management and Cloud



\---



\## 1. Summary



This week focused on making the toolkit built in Weeks 1–2 more robust,

diagnosable, configurable, and portable. Work was driven by real

troubleshooting methodology rather than guesswork, and one of the

investigations below surfaced a genuine, previously-unnoticed

performance issue on the development machine itself.



\---



\## 2. Technical Problem Investigated



\*\*Symptom:\*\* `system\_health\_checker.py` repeatedly reported CPU usage

at or near 100%, memory usage in the high 80s–90s%, and disk usage

above 95% — across almost every run this week, not just a one-off

spike.



\### Troubleshooting process followed



1\. \*\*Reproduce\*\* — confirmed the high readings were consistent across

&#x20;  multiple separate runs, not a single anomaly.

2\. \*\*Read the data carefully\*\* — the health checker reports \*aggregate\*

&#x20;  system usage, but gives no visibility into \*which\* processes are

&#x20;  responsible. This was itself a gap worth fixing.

3\. \*\*Isolate\*\* — built `performance\_monitor.py` specifically to list

&#x20;  the top CPU/memory-consuming processes, turning an unknown into a

&#x20;  measurable one.

4\. \*\*Form a hypothesis\*\* — disk usage was already at 95%+; a

&#x20;  near-full disk was suspected as a plausible root cause for

&#x20;  secondary symptoms (sync tools retrying, indexing struggling, etc.)

5\. \*\*Test the hypothesis\*\* — ran `performance\_monitor.py --sort-by

&#x20;  cpu`.



\### Result



```

===== TOP 5 PROCESSES BY CPU % =====

PID     Name                          CPU %

\--------------------------------------------------

8000    python.exe                    61.60

9456    OneDrive.exe                  34.50

4596    OneDrive.Sync.Service.exe     27.60

16088   xpdAgent.exe                  23.30

17628   xpdAgent.exe                  18.50

```



\### Root cause



`python.exe` at the top is expected — the monitoring script itself was

running. The significant finding is \*\*OneDrive.exe and

OneDrive.Sync.Service.exe together consuming \~62% CPU\*\*, on a machine

with disk usage already at 95–96%. This strongly suggests OneDrive was

struggling to sync — likely retrying repeatedly — because there was

almost no free disk space left for it to work with.



\### Solution implemented



\- Built `performance\_monitor.py` as a permanent addition to the

&#x20; toolkit, so this kind of process-level visibility isn't a one-off

&#x20; investigation but a repeatable tool.

\- Documented the finding here rather than silently working around it.



\### How this could be prevented in future



\- Free up disk space (recommended action for this machine directly —

&#x20; 95%+ disk usage is close to causing broader OS-level problems, not

&#x20; just sync slowness).

\- Run `performance\_monitor.py` periodically (or on a schedule) as an

&#x20; early-warning tool, rather than only investigating after symptoms

&#x20; appear.

\- The health checker's CRITICAL threshold for disk (90%, configurable)

&#x20; already exists specifically to catch this earlier — this incident is

&#x20; a real example of that threshold doing its job.



\---



\## 3. Debugging Improvements Made to the Toolkit



| Improvement | File | Why it matters |

|---|---|---|

| Structured logging | `system\_health\_checker.py`, `performance\_monitor.py` | Every run now writes to a log file with timestamps, not just console output — essential for diagnosing issues after the fact |

| Per-metric exception handling | `system\_health\_checker.py` | A failure reading one metric (e.g. a missing drive) no longer crashes the whole script — it logs the error and reports "Unavailable" for just that metric |

| Unit tests | `test\_system\_health\_checker.py` | 10 tests covering threshold logic and formatting, run automatically rather than relying on manual spot-checks |

| Timing decorator (`@timed`) | `performance\_monitor.py` | Reusable tool to measure how long any function takes, for catching slow operations before they become a problem |



\---



\## 4. Configuration Management



Previously, thresholds (WARNING/CRITICAL) and the disk path to check

were hardcoded directly in `system\_health\_checker.py`. This week that

was externalized:



\- \*\*`config.json`\*\* — holds thresholds, performance settings, and

&#x20; paths. Auto-created with sensible defaults if missing.

\- \*\*`config\_manager.py`\*\* — loads and validates the config (e.g.

&#x20; rejects a WARNING threshold that's higher than CRITICAL), and falls

&#x20; back safely to defaults if the file is missing or broken, rather

&#x20; than crashing.

\- \*\*Environment variable overrides\*\* — settings like

&#x20; `HEALTH\_WARNING\_THRESHOLD` can now be set via environment variables,

&#x20; which take priority over `config.json`. This matters specifically

&#x20; for cloud/VM deployment, where settings are typically injected by

&#x20; the platform rather than hand-edited in a file.



\*\*Why this matters:\*\* the same script now behaves consistently and

predictably across different machines and environments — its behavior

is driven by configuration, not by editing Python code.



\---



\## 5. Cloud/VM Readiness



\- \*\*`requirements.txt`\*\* — pins dependencies so any environment

&#x20; installs the exact same versions.

\- \*\*`Dockerfile`\*\* — packages the toolkit so it runs identically

&#x20; regardless of host OS or local Python setup.

\- \*\*`CLOUD\_DEPLOYMENT.md`\*\* — documents VM vs. container concepts and

&#x20; scalability considerations for running this toolkit against many

&#x20; machines in future, not just one.



\---



\## 6. Reflection



The most valuable part of this week wasn't fixing a deliberately broken

script — it was that the tooling built earlier in the week (the

performance monitor) immediately surfaced a real, previously invisible

issue on the actual development machine. That's the point of building

diagnostic tooling: it should find problems you didn't know to look

for, not just confirm ones you already suspected.


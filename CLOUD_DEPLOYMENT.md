\# Cloud \& VM Deployment Notes



Notes on preparing the IT Operations Automation Toolkit for a cloud or

virtual machine environment (Week 3, Friday deliverable).



\## 1. Why this matters



Scripts that only work "on my machine" are fragile — different

hardware, OS, file paths, and installed packages can all break them

silently. Making a script cloud/VM-ready means removing assumptions

about the specific machine it happens to be running on.



\## 2. Changes made to support this



| Concern | Before | After |

|---|---|---|

| Dependencies | Installed manually, version unspecified | Pinned in `requirements.txt` |

| Thresholds/paths | Hardcoded in the script | Loaded from `config.json`, overridable by environment variables |

| Disk path | Hardcoded `C:\\\\` (Windows-only) | Resolved per-OS (`C:\\\\` on Windows, `/` on Linux/macOS) |

| Portability | Tied to local Python install | Packaged in a `Dockerfile` — runs identically anywhere Docker runs |



\## 3. Why environment variables (not just config.json)



On a real cloud platform (AWS, Azure, a Docker host, etc.) you

generally can't — or shouldn't — hand-edit a config file baked into a

deployed image. Instead, the platform injects settings as environment

variables at run time. Supporting both means:



\- \*\*Locally:\*\* edit `config.json` directly, simple and visual.

\- \*\*In the cloud:\*\* set `HEALTH\_WARNING\_THRESHOLD=80` (etc.) in the

&#x20; platform's environment settings — no rebuild, no redeploy.



\## 4. Running it in a container (conceptual)



```bash

\# Build the image

docker build -t it-toolkit .



\# Run with default thresholds

docker run --rm it-toolkit



\# Override a threshold at run time, no code/image changes needed

docker run --rm -e HEALTH\_WARNING\_THRESHOLD=80 it-toolkit

```



\## 5. Virtual machines vs. containers (concept summary)



\- \*\*A VM\*\* virtualizes an entire machine (its own OS kernel) — heavier,

&#x20; but fully isolated. Good for running full server environments.

\- \*\*A container\*\* (like Docker) shares the host OS kernel and only

&#x20; packages the application + its dependencies — much lighter and

&#x20; faster to start, ideal for a small automation tool like this one.



\## 6. Scalability considerations



If this toolkit were deployed to check the health of many machines

(not just one), the current design would need to evolve:



\- Run as a \*\*scheduled job\*\* (cron on Linux, Task Scheduler on

&#x20; Windows, or a cloud scheduler) rather than manually invoked.

\- Send results to a \*\*central location\*\* (a log aggregator, a

&#x20; database, or an API) instead of only printing locally — one

&#x20; machine's report is useless if nobody centrally reviews it.

\- Add \*\*alerting\*\* (e.g. email/Slack webhook) when CRITICAL is

&#x20; detected, instead of relying on someone reading console output.



These are noted as future improvements, not implemented yet.


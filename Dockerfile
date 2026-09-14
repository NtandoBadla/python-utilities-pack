# IT Automation Toolkit — container image
#
# Building this image packages the toolkit with its exact Python
# version and dependencies, so it behaves identically on a laptop, a
# VM, or a cloud container service (e.g. AWS ECS, Azure Container
# Instances) — the core goal of "configuration management and the
# cloud".

FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer
# separately from the source code (faster rebuilds when only code
# changes).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

# Example thresholds can be overridden at run time without rebuilding
# the image, e.g.:
#   docker run -e HEALTH_WARNING_THRESHOLD=80 it-toolkit
ENV HEALTH_WARNING_THRESHOLD=75
ENV HEALTH_CRITICAL_THRESHOLD=90

ENTRYPOINT ["python", "scripts/system_health_checker.py"]
CMD ["--all"]
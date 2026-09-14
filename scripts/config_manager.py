"""
config_manager.py

Week 3 Thursday deliverable: configuration management.

Separates settings (thresholds, paths, limits) from code, so the
toolkit's behaviour can be changed by editing config.json instead of
editing Python files. This keeps behaviour consistent across machines
and makes the toolkit safer to hand to someone else.

Usage in another script:
    from config_manager import load_config

    config = load_config()
    warning_threshold = config["thresholds"]["warning"]
"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config.json")

# Environment variables that can override config.json values.
# This matters for cloud/VM deployment: cloud platforms (AWS, Azure,
# Docker, etc.) typically configure apps via environment variables
# rather than by hand-editing files on the instance.
ENV_OVERRIDES = {
    "HEALTH_WARNING_THRESHOLD": ("thresholds", "warning", int),
    "HEALTH_CRITICAL_THRESHOLD": ("thresholds", "critical", int),
    "HEALTH_TOP_PROCESS_LIMIT": ("performance", "top_process_limit", int),
    "HEALTH_SORT_BY": ("performance", "sort_by", str),
    "HEALTH_LOG_LEVEL": ("logging", "level", str),
}

DEFAULT_CONFIG = {
    "thresholds": {
        "warning": 75,
        "critical": 90
    },
    "performance": {
        "top_process_limit": 5,
        "sort_by": "cpu"
    },
    "paths": {
        "log_directory": "logs",
        "disk_to_check_windows": "C:\\",
        "disk_to_check_unix": "/"
    },
    "logging": {
        "level": "INFO"
    }
}


def create_default_config(path=CONFIG_PATH):
    """Write the default configuration file if one doesn't already exist."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)
    logger.info(f"Created default configuration file at '{path}'.")


def validate_config(config):
    """
    Check that required keys exist and values are sane.
    Raises ValueError with a clear message if something is wrong,
    rather than letting a bad config cause confusing failures later.
    """
    try:
        warning = config["thresholds"]["warning"]
        critical = config["thresholds"]["critical"]
    except KeyError as error:
        raise ValueError(f"Missing required threshold setting: {error}")

    if not (0 <= warning <= 100):
        raise ValueError(f"'warning' threshold must be between 0 and 100, got {warning}")

    if not (0 <= critical <= 100):
        raise ValueError(f"'critical' threshold must be between 0 and 100, got {critical}")

    if warning >= critical:
        raise ValueError(
            f"'warning' threshold ({warning}) must be lower than 'critical' ({critical})"
        )

    limit = config.get("performance", {}).get("top_process_limit", 5)
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError(f"'top_process_limit' must be a positive integer, got {limit}")

    sort_by = config.get("performance", {}).get("sort_by", "cpu")
    if sort_by not in ("cpu", "memory"):
        raise ValueError(f"'sort_by' must be 'cpu' or 'memory', got '{sort_by}'")

    return True


def apply_env_overrides(config):
    """
    Override config values with environment variables, if set.

    This lets the same config.json ship as a sensible default while
    still allowing a cloud/VM deployment to tune behaviour (e.g. a
    stricter WARNING threshold on a production server) purely through
    environment variables — no file edits, no redeploying code.
    """
    for env_var, (section, key, cast) in ENV_OVERRIDES.items():
        raw_value = os.environ.get(env_var)
        if raw_value is None:
            continue

        try:
            value = cast(raw_value)
        except ValueError:
            logger.warning(
                f"Environment variable '{env_var}' has invalid value "
                f"'{raw_value}' — ignoring override."
            )
            continue

        config.setdefault(section, {})[key] = value
        logger.info(f"Config override from environment: {section}.{key} = {value}")

    return config


def load_config(path=CONFIG_PATH):
    """
    Load configuration from a JSON file.

    - If the file doesn't exist, a default one is created automatically.
    - If the file is invalid JSON or fails validation, falls back to
      in-memory defaults so the toolkit can still run, and logs a
      warning explaining why.
    """
    if not path.exists():
        logger.info(f"No config file found at '{path}' — creating default.")
        create_default_config(path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as error:
        logger.warning(
            f"Config file at '{path}' contains invalid JSON ({error}). "
            "Falling back to default settings."
        )
        return DEFAULT_CONFIG

    try:
        validate_config(config)
    except ValueError as error:
        logger.warning(
            f"Config file at '{path}' failed validation ({error}). "
            "Falling back to default settings."
        )
        config = DEFAULT_CONFIG.copy()

    config = apply_env_overrides(config)

    try:
        validate_config(config)
    except ValueError as error:
        logger.warning(
            f"Environment overrides produced an invalid config ({error}). "
            "Ignoring overrides and using file/default settings."
        )
        return DEFAULT_CONFIG

    logger.info(f"Configuration loaded successfully from '{path}'.")
    return config


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    cfg = load_config()
    print("\nCurrent configuration:")
    print(json.dumps(cfg, indent=4))
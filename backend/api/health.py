import sys
from pathlib import Path

from fastapi import APIRouter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from system_health_checker import (  # noqa: E402
    get_system_health,
    determine_status,
)

router = APIRouter(
    prefix="/api/health",
    tags=["System Health"],
)


@router.get("/")
def system_health():
    health = get_system_health()

    return {
        "hostname": health["hostname"],
        "operating_system": health["operating_system"],
        "os_version": health["os_version"],
        "cpu": {
            "usage": health["cpu_usage"],
            "status": determine_status(health["cpu_usage"]),
        },
        "memory": {
            "usage": health["memory_usage"],
            "status": determine_status(health["memory_usage"]),
        },
        "disk": {
            "usage": health["disk_usage"],
            "status": determine_status(health["disk_usage"]),
        },
    }
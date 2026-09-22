import platform
import socket

import psutil
from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["System Health"])


def determine_status(usage: float) -> str:
    if usage >= 90:
        return "CRITICAL"
    elif usage >= 75:
        return "WARNING"
    return "HEALTHY"


@router.get("/")
def get_system_health():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:\\").percent

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "cpu": {
            "usage": cpu,
            "status": determine_status(cpu)
        },
        "memory": {
            "usage": memory,
            "status": determine_status(memory)
        },
        "disk": {
            "usage": disk,
            "status": determine_status(disk)
        }
    }
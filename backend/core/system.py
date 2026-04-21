import psutil
import platform
from datetime import datetime

try:
    import GPUtil

    GPU_AVAILABLE = True
except Exception:
    GPU_AVAILABLE = False


def get_cpu() -> dict:
    freq = psutil.cpu_freq()
    return {
        "usage_percent": psutil.cpu_percent(interval=0.5),
        "core_count": psutil.cpu_count(logical=False),
        "thread_count": psutil.cpu_count(logical=True),
        "frequency_mhz": round(freq.current, 1) if freq else None,
    }


def get_ram() -> dict:
    ram = psutil.virtual_memory()
    return {
        "total_gb": round(ram.total / 1e9, 1),
        "used_gb": round(ram.used / 1e9, 1),
        "available_gb": round(ram.available / 1e9, 1),
        "usage_percent": ram.percent,
    }


def get_gpu() -> list[dict]:
    try:
        import pynvml

        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        gpus = []
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            name = pynvml.nvmlDeviceGetName(handle)
            gpus.append(
                {
                    "id": i,
                    "name": name if isinstance(name, str) else name.decode(),
                    "load_percent": util.gpu,
                    "memory_used_mb": round(mem.used / 1e6, 1),
                    "memory_total_mb": round(mem.total / 1e6, 1),
                    "memory_percent": round(mem.used / mem.total * 100, 1),
                    "temperature_c": temp,
                }
            )
        pynvml.nvmlShutdown()
        return gpus
    except Exception as e:
        return []


def get_processes(limit: int = 10) -> list[dict]:
    processes = []
    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_info", "status"]
    ):
        try:
            info = proc.info
            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"],
                    "cpu_percent": info["cpu_percent"],
                    "memory_mb": round(info["memory_info"].rss / 1e6, 1),
                    "status": info["status"],
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by memory usage
    processes.sort(key=lambda x: x["memory_mb"], reverse=True)
    return processes[:limit]


def get_system_info() -> dict:
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)

    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "hostname": platform.node(),
        "uptime": f"{hours}h {minutes}m",
        "boot_time": boot_time.isoformat(),
    }


def get_full_status() -> dict:
    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "gpu": get_gpu(),
        "top_processes": get_processes(),
        "system": get_system_info(),
    }

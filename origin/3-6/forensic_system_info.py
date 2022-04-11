from dataclasses import dataclass, field, asdict
import platform, socket, psutil
import pprint


@dataclass
class Ram:
    total: str = ""
    free: str = ""


@dataclass
class Disk:
    total: str = ""
    free: str = ""


@dataclass
class SystemInfo:
    system: str = ""
    version: float = ""
    architecture: str = ""
    hostname: str = ""
    processor: str = ""
    cpu_core: str = ""
    ram: Ram = field(default_factory=Ram)
    disk: Disk = field(default_factory=Disk)


def get_sytem_info():
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage(path='/')
    ram_totle = str(round(ram.total / (1024.0 ** 3))) + " GB"
    ram_free = str(round(ram.available / (1024.0 ** 3))) + " GB"
    disk_total = str(round(disk.total / (1024.0 ** 3))) + " GB"
    disk_free = str(round(disk.free / (1024.0 ** 3))) + " GB"

    system_info = SystemInfo()
    system_info.system = platform.system()
    system_info.version = platform.version()
    system_info.architecture = platform.machine()
    system_info.hostname = socket.gethostname()
    system_info.processor = platform.processor()
    system_info.cpu_core = psutil.cpu_count()
    system_info.ram.total = ram_totle
    system_info.ram.free = ram_free
    system_info.disk.total = disk_total
    system_info.disk.free = disk_free

    return system_info


system_information = get_sytem_info()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(asdict(system_information))

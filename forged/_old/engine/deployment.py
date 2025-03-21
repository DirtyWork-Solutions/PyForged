import platform
import psutil
import socket

import GPUtil
import time

def get_gpu_info():
    """
    Gather information about the system's GPU.

    Returns:
        list: A list of dictionaries containing GPU information.
    """
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "id": gpu.id,
            "name": gpu.name,
            "load": gpu.load,
            "memory_total": gpu.memoryTotal,
            "memory_used": gpu.memoryUsed,
            "memory_free": gpu.memoryFree,
            "driver_version": gpu.driver,
            "temperature": gpu.temperature
        })
    return gpu_info

def get_system_uptime():
    """
    Get the system uptime.

    Returns:
        str: The system uptime in a human-readable format.
    """
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    return uptime_string

def get_detailed_network_info():
    """
    Gather detailed information about the system's network interfaces.

    Returns:
        dict: A dictionary containing detailed network interface information.
    """
    net_io = psutil.net_io_counters(pernic=True)
    detailed_network_info = {interface: net_io[interface]._asdict() for interface in net_io}
    return detailed_network_info

def get_system_info():
    """
    Gather basic information about the system.

    Returns:
        dict: A dictionary containing system information.
    """
    return {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def get_memory_info():
    """
    Gather information about the system's memory.

    Returns:
        dict: A dictionary containing memory information.
    """
    virtual_memory = psutil.virtual_memory()
    return {
        "total": virtual_memory.total,
        "available": virtual_memory.available,
        "percent": virtual_memory.percent,
        "used": virtual_memory.used,
        "free": virtual_memory.free
    }

def get_cpu_info():
    """
    Gather information about the system's CPU.

    Returns:
        dict: A dictionary containing CPU information.
    """
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": psutil.cpu_freq().max,
        "min_frequency": psutil.cpu_freq().min,
        "current_frequency": psutil.cpu_freq().current,
        "cpu_usage": psutil.cpu_percent(interval=1)
    }

def get_disk_info():
    """
    Gather information about the system's disk usage.

    Returns:
        dict: A dictionary containing disk usage information.
    """
    partitions = psutil.disk_partitions()
    disk_usage = {partition.device: psutil.disk_usage(partition.mountpoint)._asdict() for partition in partitions}
    return disk_usage

def get_network_info():
    """
    Gather information about the system's network interfaces.

    Returns:
        dict: A dictionary containing network interface information.
    """
    interfaces = psutil.net_if_addrs()
    network_info = {interface: [addr._asdict() for addr in addrs] for interface, addrs in interfaces.items()}
    return network_info

def get_host_name():
    """
    Get the host name of the system.

    Returns:
        str: The host name of the system.
    """
    return socket.gethostname()

def get_ip_address():
    """
    Get the IP address of the system.

    Returns:
        str: The IP address of the system.
    """
    return socket.gethostbyname(socket.gethostname())

def generate_system_report(return_type: str = 'dict'):
    """
    Generate a comprehensive report of the system's information.

    Returns:
        str: A formatted string containing the system report.
    """
    report = {
        "System Information": get_system_info(),
        "Memory Information": get_memory_info(),
        "CPU Information": get_cpu_info(),
        "Disk Information": get_disk_info(),
        "Network Information": get_network_info(),
        "Detailed Network Information": get_detailed_network_info(),
        "GPU Information": get_gpu_info(),
        "System Uptime": get_system_uptime(),
        "Host Name": get_host_name(),
        "IP Address": get_ip_address()
    }

    if return_type.lower() == 'dict' or return_type == dict:
        return report

    else:
        report_lines = []
        for section, data in report.items():
            report_lines.append(f"{section}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    report_lines.append(f"  {key}: {value}")
            elif isinstance(data, list):
                for item in data:
                    report_lines.append(f"  {item}")
            else:
                report_lines.append(f"  {data}")
            report_lines.append("")  # Add a blank line for separation

        return "\n".join(report_lines)

# Example usage
if __name__ == "__main__":
    print(generate_system_report())
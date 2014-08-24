import psutil
import socket
from uuid import getnode as get_mac

def basic_info():
    return dict(
        cpu_count = psutil.cpu_count(),
        phy_mem = psutil.virtual_memory().total,
    )
def run_info():
    return dict(
        cpu_usage = psutil.cpu_percent(),
        boot_time = psutil.boot_time(),
        swap_usage = psutil.swap_memory().used,
        mem_usage = psutil.virtual_memory().used
    )

fqdn = socket.getfqdn()
mac = format(get_mac(), '02x')
ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

id_name = '%s/%s/%s' % (fqdn, ip, mac)
print id_name

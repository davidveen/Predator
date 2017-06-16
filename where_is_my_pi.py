import re
import socket
import subprocess

from multiprocessing import cpu_count
from multiprocessing.dummy import Pool


_PREDATOR = "b8-27-eb-af-78-05"


class PiNotFound(Exception):
    pass


def get_ip():
    return socket.gethostbyname(socket.gethostname())

def get_subnet():
    return get_ip().rpartition(".")[0]

def ping(ip_address):
    subprocess.call(["ping", ip_address, "-n", "1", "-w", "1"])

def arp_scan():
    subnet = get_subnet()
    lb = 1
    ub = 255

    addresses = [
        "{s}.{i}".format(s=subnet, i=i)
        for i in range(lb, ub)
    ]

    pool = Pool(cpu_count())

    results = pool.map(ping, addresses)

    pool.close()
    pool.join()

def predator_ip():
    """
    Find and return the Predator's current IP address on the local network.
    """
    def get_line():
        arp_output = subprocess.check_output(["arp", "-a"]).split("\n")
        return [
            x for x in arp_output
            if _PREDATOR in x.lower()
        ][0]

    try:
        line = get_line()
    except IndexError:
        arp_scan()

        try:
            line = get_line()
        except IndexError as e:
            raise PiNotFound(e)

    pattern = "\d+\.\d+\.\d+\.\d+"
    ip = re.search(pattern, line).group(0)

    return ip

print(predator_ip())

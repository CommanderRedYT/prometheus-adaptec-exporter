import subprocess
import re
import time
from prometheus_client import start_http_server, Gauge

def get_temperature() -> tuple[int, int] | None:
    try:
        output = subprocess.check_output(["arcconf", "getconfig", "1", "AD"]).decode("utf-8")
        match = re.search(r"Temperature\s+:\s+(\d+)\s+C/\s+(\d+)\s+F", output)
        if match:
            return match.group(1), match.group(2)
    except subprocess.CalledProcessError:
        pass
    return None

def run_exporter():
    gauge = Gauge("adaptec_temperature", "Temperature of Adaptec RAID controller", ["unit"])
    start_http_server(9110)
    while True:
        temperature = get_temperature()

        if temperature is None:
            continue

        celsius, fahrenheit = temperature

        gauge.labels("celsius").set(int(celsius))
        gauge.labels("fahrenheit").set(int(fahrenheit))
        time.sleep(10)

if __name__ == "__main__":
    run_exporter()

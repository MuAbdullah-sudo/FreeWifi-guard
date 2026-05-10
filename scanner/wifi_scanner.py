import subprocess
import re


def scan_wifi():

    networks = []

    try:

        command = "netsh wlan show networks mode=bssid"

        result = subprocess.check_output(
            command,
            shell=True
        ).decode("utf-8", errors="ignore")

        lines = result.split("\n")

        current_network = {}

        for line in lines:

            line = line.strip()

            # SSID
            if line.startswith("SSID") and "BSSID" not in line:

                match = re.search(r":(.*)", line)

                if match:

                    if current_network:
                        networks.append(current_network)

                    current_network = {
                        "ssid": match.group(1).strip()
                    }

            # BSSID
            elif line.startswith("BSSID"):

                match = re.search(r":(.*)", line)

                if match:
                    current_network["bssid"] = match.group(1).strip()

            # Signal
            elif "Signal" in line:

                match = re.search(r":(.*)", line)

                if match:
                    current_network["signal"] = match.group(1).strip()

            # Authentication
            elif "Authentication" in line:

                match = re.search(r":(.*)", line)

                if match:
                    current_network["security"] = match.group(1).strip()

        if current_network:
            networks.append(current_network)

    except Exception as error:

        print("WiFi Scan Error:", error)

    return networks
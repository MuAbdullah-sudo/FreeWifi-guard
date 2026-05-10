from scapy.all import sniff, ARP, DNS, IP
from collections import defaultdict
import threading
import time

# Store alerts
packet_alerts = []

# DNS request tracker
dns_tracker = defaultdict(int)

# ARP tracker
arp_tracker = defaultdict(int)


def add_alert(alert_type, message, level):

    alert = {
        "type": alert_type,
        "message": message,
        "level": level,
        "time": time.strftime("%H:%M:%S")
    }

    packet_alerts.insert(0, alert)

    # Keep only latest alerts
    if len(packet_alerts) > 30:

        packet_alerts.pop()


def process_packet(packet):

    try:

        #
        # DNS TRAFFIC ANALYSIS
        #

        if packet.haslayer(DNS):

            if packet.haslayer(IP):

                source_ip = packet[IP].src

                dns_tracker[source_ip] += 1

                # Detect excessive DNS requests
                if dns_tracker[source_ip] > 20:

                    add_alert(
                        "DNS FLOOD",
                        f"Suspicious DNS activity from {source_ip}",
                        "danger"
                    )

                else:

                    add_alert(
                        "DNS Request",
                        f"DNS traffic detected from {source_ip}",
                        "info"
                    )

        #
        # ARP SPOOF DETECTION
        #

        if packet.haslayer(ARP):

            mac = packet[ARP].hwsrc

            arp_tracker[mac] += 1

            # Detect suspicious ARP activity
            if arp_tracker[mac] > 15:

                add_alert(
                    "ARP Spoofing",
                    f"Potential ARP spoofing detected from {mac}",
                    "danger"
                )

            else:

                add_alert(
                    "ARP Packet",
                    f"ARP activity detected from {mac}",
                    "warning"
                )

    except Exception as error:

        print("PACKET ERROR:", error)


def start_sniffing():

    sniff(
        prn=process_packet,
        store=False
    )


def run_sniffer():

    thread = threading.Thread(
        target=start_sniffing
    )

    thread.daemon = True

    thread.start()


def get_packet_alerts():

    return packet_alerts
from flask import Flask, render_template, jsonify

from scanner.wifi_scanner import scan_wifi

from scanner.detector import detect_evil_twins

from scanner.analyzer import (
    create_database,
    save_scan,
    get_scan_history
)

# Scapy Packet Sniffer
from scanner.packet_sniffer import (
    run_sniffer,
    get_packet_alerts
)

app = Flask(__name__)

# Initialize Database
create_database()

# Start Packet Sniffer
run_sniffer()


#
# HOME PAGE
#

@app.route("/")
def home():

    return render_template("index.html")


#
# SCAN NETWORKS
#

@app.route("/scan")
def scan():

    try:

        # Scan nearby Wi-Fi
        networks = scan_wifi()

        # Detect Evil Twins
        analyzed_networks = (
            detect_evil_twins(networks)
        )

        # Save scan results
        save_scan(analyzed_networks)

        return jsonify(analyzed_networks)

    except Exception as error:

        print("SCAN ERROR:", error)

        return jsonify({
            "error": str(error)
        }), 500


#
# SCAN HISTORY
#

@app.route("/history")
def history():

    history_data = get_scan_history()

    return jsonify(history_data)


#
# LIVE PACKET ALERTS
#

@app.route("/alerts")
def alerts():

    try:

        alerts_data = get_packet_alerts()

        return jsonify(alerts_data)

    except Exception as error:

        print("ALERT ERROR:", error)

        return jsonify({
            "error": str(error)
        }), 500


#
# RUN APP
#

if __name__ == "__main__":

    app.run(
        debug=True
    )
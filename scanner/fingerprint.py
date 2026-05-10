import json
import os

FINGERPRINT_FILE = "database/fingerprints.json"


#
# LOAD FINGERPRINT DATABASE
#

def load_fingerprints():

    if not os.path.exists(FINGERPRINT_FILE):

        return {}

    with open(FINGERPRINT_FILE, "r") as file:

        try:

            return json.load(file)

        except:

            return {}


#
# SAVE FINGERPRINT DATABASE
#

def save_fingerprints(data):

    with open(FINGERPRINT_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


#
# CREATE NETWORK FINGERPRINT
#

def create_fingerprint(network):

    return {

        "bssid":
            network.get("bssid"),

        "security":
            network.get("security"),

        "signal":
            network.get("signal")
    }


#
# ANALYZE NETWORK BEHAVIOR
#

def analyze_fingerprint(network):

    fingerprints =load_fingerprints()

    ssid = network.get("ssid")

    if not ssid:

        return network

    current = create_fingerprint(network)

    #
    # FIRST TIME NETWORK
    #

    if ssid not in fingerprints:

        fingerprints[ssid] =  current

        save_fingerprints(
            fingerprints
        )

        network["risk"] ="SAFE"

        network["threat_score"] = 10

        return network

    #
    # COMPARE FINGERPRINT
    #

    stored =fingerprints[ssid]

    risk_score = 0

    #
    # DIFFERENT BSSID
    #

    if current["bssid"] != stored["bssid"]:

        risk_score += 50

    #
    # SECURITY CHANGED
    #

    if current["security"] != stored["security"]:

        risk_score += 30

    #
    # SIGNAL ANOMALY
    #

    try:

        current_signal = int(str(current["signal"]).replace("%", ""))

        stored_signal =int(str(stored["signal"]).replace("%", ""))

        signal_diff =abs(current_signal - stored_signal)

        if signal_diff > 35:

            risk_score += 20

    except:

        pass

    #
    # FINAL CLASSIFICATION
    #

    if risk_score >= 70:

        network["risk"] ="DANGEROUS"

    elif risk_score >= 40:

        network["risk"] = "SUSPICIOUS"

    else:

        network["risk"] ="SAFE"

    network["threat_score"] =risk_score

    return network
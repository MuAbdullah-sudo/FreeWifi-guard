from scanner.fingerprint import (
    analyze_fingerprint
)


def detect_evil_twins(networks):

    ssid_count = {}

    analyzed_networks = []

    #
    # COUNT SSIDs
    #

    for network in networks:

        ssid =network.get(
                "ssid",
                ""
            )

        if ssid in ssid_count:

            ssid_count[ssid] += 1

        else:

            ssid_count[ssid] = 1

    #
    # ANALYZE NETWORKS
    #

    for network in networks:

        ssid =network.get(
                "ssid",
                ""
            )

        security =network.get(
                "security",
                ""
            )

        #
        # DEFAULT RISK
        #

        risk = "SAFE"

        threat_score = 0

        #
        # DUPLICATE SSID DETECTION
        #

        if ssid_count[ssid] > 1:

            risk = "SUSPICIOUS"

            threat_score += 40

        #
        # OPEN NETWORK DETECTION
        #

        if "Open" in security:

            risk = "DANGEROUS"

            threat_score += 50

        #
        # APPLY INITIAL VALUES
        #

        network["risk"] = risk

        network["threat_score"] = threat_score

        #
        # RUN SIGNAL FINGERPRINT ANALYSIS
        #

        network =analyze_fingerprint(
                network
            )

        #
        # THREAT LABEL
        #

        final_score =network.get(
                "threat_score",
                0
            )

        if final_score >= 70:

            network["threat_label"] = \
                "HIGH RISK"

        elif final_score >= 40:

            network["threat_label"] = \
                "MEDIUM RISK"

        else:

            network["threat_label"] = \
                "LOW RISK"

        analyzed_networks.append(
            network
        )

    return analyzed_networks
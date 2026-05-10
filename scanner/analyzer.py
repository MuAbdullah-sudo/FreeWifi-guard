import sqlite3


DATABASE_NAME = "database/wifi_guard.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ssid TEXT,
            bssid TEXT,
            signal TEXT,
            security TEXT,
            risk TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_scan(networks):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    for network in networks:

        cursor.execute("""
            INSERT INTO scans (
                ssid,
                bssid,
                signal,
                security,
                risk
            )
            VALUES (?, ?, ?, ?, ?)
        """, (

            network.get("ssid"),
            network.get("bssid"),
            network.get("signal"),
            network.get("security"),
            network.get("risk")

        ))

    connection.commit()
    connection.close()


def get_scan_history():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT ssid, bssid, signal, security, risk
        FROM scans
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append({
            "ssid": row[0],
            "bssid": row[1],
            "signal": row[2],
            "security": row[3],
            "risk": row[4]
        })

    return history
import csv
import re

INPUT_FILE = "data/parsed-incident-logs.csv"


def detect_incident(row):
    message = row["Message"].lower()
    level = row["Level"].upper()
    service = row["Service"]

    if "http 5" in message:
        return "HTTP Failure", "HIGH"

    if "login failed" in message:
        return "Authentication Failure", "MEDIUM"

    if "payment timeout" in message:
        return "Payment Timeout", "HIGH"

    if "slow request" in message:
        duration = row.get("DurationMs", "")

        if duration and int(duration) > 4000:
            return "Critical Slow Request", "HIGH"

        return "Slow Request", "MEDIUM"

    if "database connection failed" in message:
        return "Database Failure", "HIGH"

    if "connection pool exhausted" in message:
        return "Database Resource Exhaustion", "HIGH"

    if level == "ERROR":
        return f"{service} Error", "MEDIUM"

    return "Normal", "LOW"


def detect_incidents():
    incidents = []

    with open(INPUT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            incident_type, severity = detect_incident(row)

            if incident_type != "Normal":
                row["IncidentType"] = incident_type
                row["Severity"] = severity
                incidents.append(row)

    print("\n=== INCIDENT DETECTION RESULTS ===\n")

    for incident in incidents:
        print(
            f"[{incident['Severity']}] "
            f"{incident['IncidentType']} | "
            f"{incident['Service']} | "
            f"{incident['TimeGenerated']}"
        )

    print(f"\nTotal incidents detected: {len(incidents)}")


if __name__ == "__main__":
    detect_incidents()
    
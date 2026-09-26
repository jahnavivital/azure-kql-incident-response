import csv
from collections import Counter


INPUT_FILE = "data/parsed-incident-logs.csv"


def classify_incident(row):
    message = row["Message"].lower()
    level = row["Level"].upper()

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
        return f"{row['Service']} Error", "MEDIUM"

    return "Normal", "LOW"


def generate_summary():
    incident_types = Counter()
    severities = Counter()
    services = Counter()

    with open(INPUT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            incident_type, severity = classify_incident(row)

            if incident_type != "Normal":
                incident_types[incident_type] += 1
                severities[severity] += 1
                services[row["Service"]] += 1

    print("\n=== INCIDENT SUMMARY ===\n")

    print("By Incident Type:")
    for incident, count in incident_types.items():
        print(f"{incident}: {count}")

    print("\nBy Severity:")
    for severity, count in severities.items():
        print(f"{severity}: {count}")

    print("\nBy Service:")
    for service, count in services.items():
        print(f"{service}: {count}")

    print(f"\nTotal Incidents: {sum(incident_types.values())}")


if __name__ == "__main__":
    generate_summary()
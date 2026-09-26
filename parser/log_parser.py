import csv
import re


INPUT_FILE = "data/incident-logs.csv"
OUTPUT_FILE = "data/parsed-incident-logs.csv"


def parse_message(message):
    result = {}

    user = re.search(r"user=(\w+)", message)
    ip = re.search(r"ip=([\d.]+)", message)
    duration = re.search(r"duration=(\d+)ms", message)
    server = re.search(r"server=([\w-]+)", message)
    endpoint = re.search(r"endpoint=([^\s]+)", message)

    result["User"] = user.group(1) if user else ""
    result["IP"] = ip.group(1) if ip else ""
    result["DurationMs"] = duration.group(1) if duration else ""
    result["Server"] = server.group(1) if server else ""
    result["Endpoint"] = endpoint.group(1) if endpoint else ""

    return result


def parse_logs():
    with open(INPUT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        rows = []

        for row in reader:
            extracted = parse_message(row["Message"])
            row.update(extracted)
            rows.append(row)

    fieldnames = [
        "TimeGenerated",
        "Level",
        "Service",
        "Message",
        "User",
        "IP",
        "DurationMs",
        "Server",
        "Endpoint"
    ]

    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

    print(f"Parsing completed successfully.")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    parse_logs()
import subprocess

print("=" * 60)
print(" AZURE KQL INCIDENT RESPONSE - DEMO")
print("=" * 60)

print("\n[1] Parsing incident logs...")
subprocess.run(["python3", "parser/log_parser.py"])

print("\n[2] Detecting incidents...")
subprocess.run(["python3", "detection/incident_detector.py"])

print("\n[3] Generating incident summary...")
subprocess.run(["python3", "reports/incident_summary.py"])

print("\n" + "=" * 60)
print(" DEMO COMPLETED SUCCESSFULLY")
print("=" * 60)
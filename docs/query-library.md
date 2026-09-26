# KQL Query Library Documentation

## Overview

This document describes the reusable KQL queries developed for the
Azure Log Analytics KQL Query Library for Incident Response project.

The queries are designed to identify common incident patterns and
support faster incident diagnosis.

---

## 1. Application Errors

### File

`queries/application-errors.kql`

### Purpose

Identifies application exceptions and displays the number of errors
over time.

### Azure Table

`AppExceptions`

### Query

```kql
AppExceptions
| where TimeGenerated > ago(1h)
| summarize ErrorCount = count()
    by bin(TimeGenerated, 5m), ProblemId
| order by TimeGenerated asc
---

## 2. HTTP 5xx Errors

### File

`queries/http-5xx-errors.kql`

### Purpose

Detects HTTP server-side errors such as HTTP 500 and HTTP 503.

### Azure Table

`AppRequests`

### Query

```kql
AppRequests
| where TimeGenerated > ago(1h)
| where ResultCode startswith "5"
| summarize ErrorCount = count()
    by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Use Case

Helps identify server failures and service availability problems.

---

## 3. Failed Logins

### File

`queries/failed-logins.kql`

### Purpose

Identifies unsuccessful authentication attempts.

### Azure Table

`SigninLogs`

### Query

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != "0"
| summarize FailedAttempts = count()
    by UserPrincipalName, IPAddress
| order by FailedAttempts desc
```

### Use Case

Helps identify repeated authentication failures.

---

## 4. Slow Requests

### File

`queries/slow-requests.kql`

### Purpose

Identifies requests that take more than one second to complete.

### Azure Table

`AppRequests`

### Query

```kql
AppRequests
| where TimeGenerated > ago(1h)
| where DurationMs > 1000
| summarize SlowRequests = count(),
            AverageDuration = avg(DurationMs)
    by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

### Use Case

Useful for detecting application performance degradation.

---

## 5. Service Failures

### File

`queries/service-failures.kql`

### Purpose

Identifies failed Azure operations.

### Azure Table

`AzureActivity`

### Query

```kql
AzureActivity
| where TimeGenerated > ago(1h)
| where ActivityStatusValue == "Failed"
| summarize FailedOperations = count()
    by ResourceGroup, ResourceProviderValue
| order by FailedOperations desc
```

### Use Case

Helps identify Azure resource and service failures.

---

# Query Optimization

## Optimized Query

### File

`optimization/optimized-queries.kql`

The optimized query reduces unnecessary data processing by filtering
early, limiting the time range, and selecting only required columns.

### Optimized KQL

```kql
AppRequests
| where TimeGenerated > ago(1h)
| where ResultCode startswith "5"
| project TimeGenerated, Name, ResultCode, DurationMs
| summarize
    ErrorCount = count(),
    AverageDuration = avg(DurationMs)
    by bin(TimeGenerated, 5m), ResultCode
| order by TimeGenerated asc
```

### Benefits

- Reduces unnecessary data processing.
- Filters data before aggregation.
- Uses only required columns.
- Improves query efficiency on large datasets.

---

# Log Parsing

## File

`parser/log_parser.py`

The parser extracts useful information from unstructured log messages.

### Extracted Fields

- User
- IP address
- Duration
- Server
- Endpoint

### Input

`data/incident-logs.csv`

### Output

`data/parsed-incident-logs.csv`

---

# Incident Detection

## File

`detection/incident_detector.py`

The incident detector identifies common incident patterns from parsed
logs and assigns severity levels.

### Supported Incident Types

- Payment Timeout
- Database Failure
- Authentication Failure
- HTTP Failure
- Slow Request
- Critical Slow Request
- Database Resource Exhaustion

### Detection Result

The current sample dataset contains:

**10 incidents**

---

# Incident Summary

## File

`reports/incident_summary.py`

The incident summary groups incidents by type, severity, and service.

### Summary

| Metric | Count |
|---|---:|
| Total Incidents | 10 |
| High Severity | 7 |
| Medium Severity | 3 |

---

# Dashboard Data

## File

`dashboard/incident-dashboard.json`

The dashboard data contains:

- Total incidents
- Severity distribution
- Incident-type distribution
- Service-wise incident counts

This data can be used as the basis for an incident monitoring dashboard.

---

# Incident Response Workflow

```text
Azure Applications / Services
            ↓
      Azure Monitor
            ↓
   Log Analytics Workspace
            ↓
      KQL Query Library
            ↓
      Log Parsing
            ↓
    Incident Detection
            ↓
     Incident Summary
            ↓
        Dashboard
            ↓
    Incident Response
```

---

# Project Benefits

1. Provides reusable KQL queries for common incidents.
2. Reduces repetitive manual log analysis.
3. Supports faster incident diagnosis.
4. Handles common unstructured log patterns through parsing.
5. Provides automated incident classification.
6. Assigns severity levels to detected incidents.
7. Demonstrates query optimization for large datasets.
8. Provides structured incident statistics.
9. Provides dashboard-ready data.
10. Supports a complete incident-response workflow.

---

# Expected Outcome

The project provides a centralized KQL query library combined with
log parsing, automated incident detection, query optimization,
incident summarization, and dashboard-ready data.

The solution helps incident-response teams analyze Azure logs more
efficiently and reduce the effort required to diagnose common
incidents.
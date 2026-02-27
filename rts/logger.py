"""
Custom Lightweight Logging Utility
-----------------------------------

This module provides a unified logging mechanism designed for Django-based
applications. It supports both request-aware logging (inside views/middleware)
and system-level logging (background tasks, utilities, services).

Key Features
------------
1. Unified logging interface:
       record(request, "message")
       record("message")

2. Automatic caller tracing:
   - Captures filename
   - Captures line number
   - Captures timestamp

3. Request metadata capture (if available):
   - IP address (supports X-Forwarded-For)
   - HTTP method
   - URL path
   - Authenticated user (if authentication is enabled)
   - Basic headers (User-Agent, Referer)

4. Dual log output:
   - `records.log` → human-readable flat logs
   - `detail_records.log` → structured JSON logs

5. Integrity verification:
   - Each JSON log entry includes a SHA-256 hash
   - Ensures tamper-evidence of log entries

Design Philosophy
-----------------
This logger is intentionally defensive and does not assume that
authentication or request attributes always exist. It safely handles:

- Projects without authentication
- Anonymous users
- System-level executions
- Missing request metadata

The `record()` function dynamically detects whether it was called
with a Django request object or just a message string.

Example Usage
-------------
Inside a Django view:
    record(request, "User accessed dashboard")

Inside background jobs or utilities:
    record("Daily cron job started")

Security Note
-------------
The hash stored in detailed logs allows post-event verification
to detect modification of log entries.

Limitations
-----------
This is a file-based logger and does not include:
- Log rotation
- Concurrency control
- Log levels (INFO, WARNING, ERROR)
- Centralized logging integration

For production-grade scalability, consider migrating to Python's
built-in `logging` module with structured formatters and rotating handlers.
"""



import inspect
import os
import json
import hashlib
from datetime import datetime


def get_actor(request):
    """
    Safely extracts the acting user from the request.

    Returns:
    - username or user_id if authentication is enabled and user is logged in
    - "anonymous" if authentication/session is not present or user is unauthenticated

    This function is intentionally defensive to avoid runtime errors
    when authentication is not yet implemented in the project.
    """
    try:
        user = getattr(request, "user", None)

        if user and hasattr(user, "is_authenticated") and user.is_authenticated:
            return getattr(user, "username", None) or getattr(user, "id", "authenticated")
    except Exception:
        pass

    return "anonymous"





def record(request_or_message, message=None):
    """
    Unified logging function.

    Usage:
        record(request, "Message with request context")
        record("Message without request context")
    """

    # ----------------------------
    # Detect call signature
    # ----------------------------
    if message is None:
        request = None
        message = request_or_message
    else:
        request = request_or_message

    # ----------------------------
    # Caller info
    # ----------------------------
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    filepath = caller_frame.f_globals.get("__file__", "unknown")
    file_name = os.path.basename(filepath)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ----------------------------
    # Request metadata (if available)
    # ----------------------------
    if request:
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "unknown")

        path = getattr(request, "path", "N/A")
        method = getattr(request, "method", "N/A")
        actor = get_actor(request)

        headers = {
            "User-Agent": request.META.get("HTTP_USER_AGENT", "")[:200],
            "Referer": request.META.get("HTTP_REFERER", ""),
        }

    else:
        ip = "N/A"
        method = "N/A"
        path = "N/A"
        actor = "system"
        headers = {}

    # ----------------------------
    # Simple Log (records.log)
    # ----------------------------
    record_data = (
        f"[{timestamp} --- {ip}] "
        f"{file_name} [{line_number}] "
        f"[{method}] {path} --> {message}"
    )

    with open("records.log", "a", encoding="utf-8") as f:
        f.write(record_data + "\n")

    # ----------------------------
    # Detailed JSON Log
    # ----------------------------
    full_data = {
        "time": timestamp,
        "ip": ip,
        "file": file_name,
        "line": line_number,
        "method": method,
        "path": path,
        "user": actor,
        "headers": headers,
        "message": message,
    }

    hash_value = hashlib.sha256(
        json.dumps(full_data, sort_keys=True).encode()
    ).hexdigest()

    full_data["hash"] = hash_value

    with open("detail_records.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(full_data) + "\n")



# """
# logger.py

# This module provides a lightweight, file-based request and audit logging utility.

# It is designed to:
# - Record request-level activity without using middleware
# - Work safely even when authentication/session is not implemented
# - Capture minimal but important request metadata (IP, path, method, source code location)
# - Maintain a tamper-evident audit trail using cryptographic hashing
# - Avoid database usage for high-volume logging data

# Two log files are written:
# 1. records.log
#    - Human-readable, quick-view log entries for developers/admins

# 2. detail_records.log
#    - Structured JSON audit records with SHA-256 hash
#    - Intended for audits, verification, and forensic analysis

# Log rotation / compression is intentionally NOT handled here.
# That responsibility should be managed externally (cron job / scheduled task).

# This module can be safely used now and will automatically support
# authenticated users once session/authentication is integrated.
# """
   
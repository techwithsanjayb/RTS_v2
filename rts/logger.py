"""
logger.py

This module provides a lightweight, file-based request and audit logging utility.

It is designed to:
- Record request-level activity without using middleware
- Work safely even when authentication/session is not implemented
- Capture minimal but important request metadata (IP, path, method, source code location)
- Maintain a tamper-evident audit trail using cryptographic hashing
- Avoid database usage for high-volume logging data

Two log files are written:
1. records.log
   - Human-readable, quick-view log entries for developers/admins

2. detail_records.log
   - Structured JSON audit records with SHA-256 hash
   - Intended for audits, verification, and forensic analysis

Log rotation / compression is intentionally NOT handled here.
That responsibility should be managed externally (cron job / scheduled task).

This module can be safely used now and will automatically support
authenticated users once session/authentication is integrated.
"""

import inspect
import os
import json
import hashlib
from datetime import datetime
##############################################################
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


##############################################################

def record(request,message):

    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    filepath = caller_frame.f_globals.get("__file__", "unknown")
    file_name = os.path.basename(filepath)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if request:
        # IP safely extract
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "unknown")

        path = request.path
        method = request.method
        actor = get_actor(request)
    else:
        ip = "anonymous"
        method = "N/A"
        path = "N/A"
        actor = "anonymous"
            
    record_data = (
        f"[{timestamp} --- {ip}]"
        f" {file_name} [{line_number}]"
        f"---[{method}]---{path} --> {message} ]"
    )

    with open("records.log", "a", encoding="utf-8") as f:
        f.write(record_data + "\n")

    # -------- FULL REQUEST RECORD (records.log) ----------

    full_data = {
        "time": timestamp,
        "ip": ip,
        "file": file_name,
        "line": line_number,
        "method": method,
        "path": path,
        "user": actor,
        "headers": {
            "User-Agent": request.META.get("HTTP_USER_AGENT", "")[:200],
            "Referer": request.META.get("HTTP_REFERER", ""),
        },
        "message": message,
    }

    # -------- TAMPER-PROOF HASH ----------
    hash_value = hashlib.sha256(
        json.dumps(full_data, sort_keys=True).encode()
    ).hexdigest()

    full_data["hash"] = hash_value

    with open("detail_records.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(full_data) + "\n")
        
        
def audit(message):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    filepath = caller_frame.f_globals.get("__file__", "unknown")
    file_name = os.path.basename(filepath)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    full_data = {
        "time": timestamp,
        "file": file_name,
        "line": line_number,
        "message": message,
    }
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(full_data) + "\n")
    
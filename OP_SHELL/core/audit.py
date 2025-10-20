# op_shell/audit.py
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def log_event(
    user: str,
    intent_text: str,
    matched_rule: str,
    command: str,
    action: str,  # "dry_run", "execute_attempt", "execute_success", "execute_failure"
    details: dict = None
):
    event = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": user,
        "intent": intent_text,
        "matched_rule": matched_rule,
        "command": command,
        "action": action,
        "details": details or {}
    }

    log_file = LOG_DIR / "op-shell.log"
    with open(log_file, "a") as f:
        f.write(json.dumps(event) + "\n")
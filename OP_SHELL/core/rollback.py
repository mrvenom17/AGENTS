# op_shell/rollback.py
import os
import hashlib
from pathlib import Path
from datetime import datetime

SNAPSHOT_DIR = Path("snapshots")

def hash_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def record_pre_state(command: str, params: dict) -> dict:
    # Example: if command involves /etc/nginx/nginx.conf, hash it
    state = {}
    if "nginx" in command and "/etc/nginx" in command:
        state["/etc/nginx/nginx.conf"] = hash_file("/etc/nginx/nginx.conf")
    # Extend as needed per rule
    return state
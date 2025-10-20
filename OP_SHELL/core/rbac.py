# op_shell/rbac.py
import os
import yaml
from pathlib import Path

def get_current_user() -> str:
    return os.getenv("USER") or os.getenv("USERNAME") or "unknown"

def load_policy(config_path: str = "config/policies.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)

def is_intent_allowed(intent_description: str, user: str, policy: dict) -> bool:
    user_role = policy["user_roles"].get(user)
    if not user_role:
        return False
    allowed = policy["roles"].get(user_role, {}).get("allowed_intents", [])
    return intent_description in allowed
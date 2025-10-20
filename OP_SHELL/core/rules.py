import os
import yaml
from pathlib import Path
from typing import List
from model.models import IntentRule

def load_rules_from_dir(rules_dir: str = "rules") -> List[IntentRule]:
    rules = []
    rules_path = Path(rules_dir)
    if not rules_path.exists():
        raise FileNotFoundError(f"Rules directory not found: {rules_path}")
    
    for rule_file in rules_path.glob("*.yaml"):
        with open(rule_file) as f:
            data = yaml.safe_load(f)
            for rule_dict in data.get("rules", []):
                rules.append(IntentRule(**rule_dict))
    return rules
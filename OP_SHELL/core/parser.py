
import re
from typing import Optional, Tuple
from jinja2 import Template
from model.models import IntentRule

def match_intent(intent_text: str, rules: list[IntentRule]) -> Optional[Tuple[IntentRule, dict]]:
    for rule in rules:
        match = re.fullmatch(rule.pattern, intent_text.strip(), re.IGNORECASE)
        if match:
            return rule, match.groupdict()
    return None

def render_command(rule: IntentRule, params: dict) -> str:
    template = Template(rule.template.command)
    return template.render(**params)
"""
Filtro de seguridad determinista. Se aplica ANTES de rankear suplementos.

No hace cross-check automático contra una base de fármacos (fuera de alcance): si
el usuario reporta medicación, se emite un aviso global de "consulta a un
profesional" y se aplican las reglas conservadoras de data/rules/safety_rules.json.
"""
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from agent.questions import has_meaningful_text

DISCLAIMER = (
    "Esta información es orientativa y no sustituye el consejo médico. Estas "
    "recomendaciones no constituyen un diagnóstico ni un tratamiento. Consulta "
    "con un profesional de la salud antes de iniciar cualquier suplementación."
)
DISCLAIMER_VERSION = 1


def _rules_path() -> Path:
    candidates = [os.environ.get("DATA_DIR"), "/data", Path(__file__).resolve().parents[2] / "data"]
    for base in candidates:
        if base and (Path(base) / "rules" / "safety_rules.json").exists():
            return Path(base) / "rules" / "safety_rules.json"
    raise FileNotFoundError("No se encontró safety_rules.json (configura DATA_DIR)")


with open(_rules_path()) as f:
    RULES: list[dict] = json.load(f)


@dataclass
class SafetyResult:
    blocked: dict[str, str] = field(default_factory=dict)        # slug -> motivo del bloqueo
    warnings: dict[str, list[str]] = field(default_factory=dict)  # slug -> avisos
    advisory: bool = False
    advisory_message: str = ""

    def risk_flags(self) -> list[dict]:
        flags = [
            {"type": "hard_block", "supplement": slug, "message": msg}
            for slug, msg in self.blocked.items()
        ]
        flags += [
            {"type": "soft_warning", "supplement": slug, "message": msg}
            for slug, msgs in self.warnings.items()
            for msg in msgs
        ]
        if self.advisory:
            flags.append({"type": "advisory", "supplement": None, "message": self.advisory_message})
        return flags


def evaluate(responses: dict) -> SafetyResult:
    medication = responses.get("medication", "")
    other = responses.get("other_treatments", "")
    text = f"{medication} {other}".lower()
    result = SafetyResult()

    for rule in RULES:
        ct = rule["condition_type"]
        if ct == "general_medication":
            continue  # se trata como aviso global más abajo

        keywords = rule.get("medication_keywords") or rule.get("symptom_keywords") or []
        if not any(k.lower() in text for k in keywords):
            continue

        for slug in rule.get("affected_supplement_slugs", []):
            if rule["action"] == "hard_block":
                result.blocked[slug] = rule["message"]
            else:
                result.warnings.setdefault(slug, []).append(rule["message"])

    if has_meaningful_text(medication):
        general = next((r for r in RULES if r["condition_type"] == "general_medication"), None)
        result.advisory = True
        result.advisory_message = general["message"] if general else DISCLAIMER

    return result

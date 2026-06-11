"""
Seed the supplements table from data/catalog.json.
Run inside the backend container: python seed.py
"""
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))

from models.db import SessionLocal, Supplement
from seed_evidence import seed_evidence


def main() -> None:
    catalog_path = os.path.join(os.path.dirname(__file__), "..", "data", "supplements", "catalog.json")
    with open(catalog_path) as f:
        catalog = json.load(f)

    db = SessionLocal()
    inserted = 0
    skipped = 0

    try:
        for item in catalog:
            existing = db.query(Supplement).filter(Supplement.slug == item["slug"]).first()
            if existing:
                skipped += 1
                continue
            db.add(Supplement(
                id=uuid.uuid4(),
                slug=item["slug"],
                name=item["name"],
                category=item.get("category", ""),
                evidence_level=item.get("evidence_level", "C"),
                mechanisms=item.get("mechanisms", []),
                standard_dose=item.get("standard_dose", ""),
                contraindications=item.get("contraindications", []),
                known_interactions=item.get("known_interactions", []),
                need_weights=item.get("need_weights", {}),
            ))
            inserted += 1

        db.commit()
        print(f"Seed complete: {inserted} inserted, {skipped} already existed.")
        seed_evidence(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()

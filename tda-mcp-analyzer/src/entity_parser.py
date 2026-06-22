"""Parse LLM markdown output into individual entities for Terre d'Arran."""

import re
from dataclasses import dataclass

_ENTITY_MARKER = re.compile(r"<!--\s*ENTITY:\s*([^>]+?)\s*-->")

CATEGORY_TO_PATH: dict[str, str] = {
    "Regles/Personnage/Profils": "01-Regles/Personnage/Profils",
    "Regles/Personnage/Competences": "01-Regles/Personnage/Competences",
    "Regles/Personnage/Traits": "01-Regles/Personnage/Traits",
    "Regles/Mecanique": "01-Regles/Mecanique",
    "Lieux/Villes": "02-Lieux/Villes",
    "Lieux/Donjons": "02-Lieux/Donjons",
    "Lieux/Regions": "02-Lieux/Regions",
    "Lieux/Points-d-interet": "02-Lieux/Points-d-interet",
    "Factions": "03-Factions",
    "PNJ": "04-PNJ",
    "Bestiaire": "05-Bestiaire",
    "Equipement/Armes": "06-Equipement/Armes",
    "Equipement/Armures": "06-Equipement/Armures",
    "Equipement/Objets": "06-Equipement/Objets",
    "Magie/Sorts": "07-Magie/Sorts",
    "Magie/Rituels": "07-Magie/Rituels",
    "Magie/Domaines": "07-Magie/Domaines",
    "Tables": "08-Tables",
    "INDEX": "INDEX",
}


@dataclass
class Entity:
    category: str
    name: str
    content: str
    vault_path: str
    chunk_id: str = ""
    source_book: str = ""


def parse_entities(markdown: str, chunk_id: str = "") -> list[Entity]:
    """Split markdown on ENTITY markers and return Entity objects."""
    parts = _ENTITY_MARKER.split(markdown)

    entities: list[Entity] = []
    i = 1
    while i < len(parts) - 1:
        raw_path = parts[i].strip()
        content = parts[i + 1].strip()
        i += 2

        if not content:
            continue

        category, name = _split_path(raw_path)
        vault_path = _resolve_vault_path(category)
        book_id = chunk_id.split("_")[0] if chunk_id else ""

        entities.append(Entity(
            category=category,
            name=name,
            content=content,
            vault_path=vault_path,
            chunk_id=chunk_id,
            source_book=book_id,
        ))

    return entities


def _split_path(raw: str) -> tuple[str, str]:
    parts = raw.rsplit("/", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return raw, raw


def _resolve_vault_path(category: str) -> str:
    if category in CATEGORY_TO_PATH:
        return CATEGORY_TO_PATH[category]

    for prefix, vault_dir in CATEGORY_TO_PATH.items():
        if category.startswith(prefix):
            suffix = category[len(prefix):]
            return vault_dir + suffix

    return category

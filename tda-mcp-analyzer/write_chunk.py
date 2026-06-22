#!/usr/bin/env python3
"""Helper pour agents : écrit les entités d'un chunk dans le vault.

Usage:
    echo '<markdown>' | python write_chunk.py <chunk_id>
    python write_chunk.py <chunk_id> --file <markdown_file>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from src import entity_parser, obsidian_writer, progress_tracker

VAULT_PATH = "../obsidian"

parser = argparse.ArgumentParser()
parser.add_argument("chunk_id")
parser.add_argument("--file", help="Fichier markdown à lire (sinon stdin)")
args = parser.parse_args()

if args.file:
    markdown = Path(args.file).read_text(encoding="utf-8")
else:
    markdown = sys.stdin.read()

book_id = args.chunk_id.split("_p")[0] if "_p" in args.chunk_id else args.chunk_id.split("_")[0]

entities = entity_parser.parse_entities(markdown, args.chunk_id)
result = obsidian_writer.write_entities(entities, VAULT_PATH)

progress = progress_tracker.load(VAULT_PATH)
progress_tracker.mark_chunk_done(progress, book_id, len(result["files_created"]), result["conflicts_detected"])
progress_tracker.update_entity_counts(progress, VAULT_PATH)
progress_tracker.save(progress)

print(json.dumps(result, ensure_ascii=False, indent=2))

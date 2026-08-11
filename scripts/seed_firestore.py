#!/usr/bin/env python3
"""Seed script for Firestore players collection."""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-0fa1cb8107fc"
COLLECTION_NAME = "players"

INITIAL_PLAYERS = [
    {
        "player_id": "bukayo-saka",
        "name": "Bukayo Saka",
        "team": "Arsenal",
        "position": "RW",
        "rating": 87,
        "preferred_foot": "Left",
        "pace": 86,
        "shooting": 83,
        "passing": 82,
        "dribbling": 88,
        "defending": 55,
        "physical": 74,
    },
    {
        "player_id": "martin-odegaard",
        "name": "Martin Ødegaard",
        "team": "Arsenal",
        "position": "CAM",
        "rating": 89,
        "preferred_foot": "Left",
        "pace": 77,
        "shooting": 81,
        "passing": 90,
        "dribbling": 89,
        "defending": 62,
        "physical": 68,
    },
    {
        "player_id": "declan-rice",
        "name": "Declan Rice",
        "team": "Arsenal",
        "position": "CDM",
        "rating": 87,
        "preferred_foot": "Right",
        "pace": 76,
        "shooting": 72,
        "passing": 83,
        "dribbling": 81,
        "defending": 86,
        "physical": 86,
    },
    {
        "player_id": "william-saliba",
        "name": "William Saliba",
        "team": "Arsenal",
        "position": "CB",
        "rating": 87,
        "preferred_foot": "Right",
        "pace": 82,
        "shooting": 40,
        "passing": 72,
        "dribbling": 74,
        "defending": 88,
        "physical": 84,
    },
    {
        "player_id": "kai-havertz",
        "name": "Kai Havertz",
        "team": "Arsenal",
        "position": "ST",
        "rating": 84,
        "preferred_foot": "Left",
        "pace": 80,
        "shooting": 81,
        "passing": 79,
        "dribbling": 82,
        "defending": 50,
        "physical": 78,
    },
]


def seed_firestore():
    print(f"Connecting to Firestore for project: {PROJECT_ID}...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    for player in INITIAL_PLAYERS:
        doc_ref = collection_ref.document(player["player_id"])
        doc_ref.set(player)
        print(f"Seeded player: {player['name']} ({player['position']}) -> {doc_ref.path}")

    print("Firestore seeding complete!")


if __name__ == "__main__":
    seed_firestore()

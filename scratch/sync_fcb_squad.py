"""Script to sync the entire FC Barcelona squad in Firestore with current 2025/2026 roster."""

import sys
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-0fa1cb8107fc"
COLLECTION_NAME = "players"

def sync_fcb_squad():
    db = firestore.Client(project=PROJECT_ID)
    coll = db.collection(COLLECTION_NAME)

    # 1. Fetch all current FC Barcelona players in Firestore and delete them to do a clean sync
    print("Fetching existing FC Barcelona documents...")
    existing = list(coll.where("team", "==", "FC Barcelona").stream())
    for doc in existing:
        print(f"Deleting outdated record: {doc.id}")
        doc.reference.delete()

    # 2. Complete Official FC Barcelona Roster (2025/2026 Season)
    fcb_squad = [
        # Goalkeepers
        {
            "player_id": "marc-andre-ter-stegen",
            "name": "Marc-André ter Stegen",
            "team": "FC Barcelona",
            "position": "GK",
            "rating": 89,
            "preferred_foot": "Right",
            "pace": 85, "shooting": 85, "passing": 88, "dribbling": 65, "defending": 88, "physical": 85
        },
        {
            "player_id": "wojciech-szczesny",
            "name": "Wojciech Szczęsny",
            "team": "FC Barcelona",
            "position": "GK",
            "rating": 84,
            "preferred_foot": "Right",
            "pace": 81, "shooting": 82, "passing": 82, "dribbling": 60, "defending": 84, "physical": 81
        },
        {
            "player_id": "inaki-pena",
            "name": "Iñaki Peña",
            "team": "FC Barcelona",
            "position": "GK",
            "rating": 76,
            "preferred_foot": "Right",
            "pace": 74, "shooting": 72, "passing": 76, "dribbling": 62, "defending": 75, "physical": 73
        },
        # Defenders
        {
            "player_id": "jules-kounde",
            "name": "Jules Koundé",
            "team": "FC Barcelona",
            "position": "RB",
            "rating": 86,
            "preferred_foot": "Right",
            "pace": 84, "shooting": 50, "passing": 76, "dribbling": 78, "defending": 86, "physical": 82
        },
        {
            "player_id": "pau-cubarsi",
            "name": "Pau Cubarsí",
            "team": "FC Barcelona",
            "position": "CB",
            "rating": 83,
            "preferred_foot": "Right",
            "pace": 75, "shooting": 42, "passing": 83, "dribbling": 77, "defending": 84, "physical": 79
        },
        {
            "player_id": "inigo-martinez",
            "name": "Íñigo Martínez",
            "team": "FC Barcelona",
            "position": "CB",
            "rating": 82,
            "preferred_foot": "Left",
            "pace": 71, "shooting": 45, "passing": 73, "dribbling": 72, "defending": 83, "physical": 81
        },
        {
            "player_id": "andreas-christensen",
            "name": "Andreas Christensen",
            "team": "FC Barcelona",
            "position": "CB",
            "rating": 82,
            "preferred_foot": "Right",
            "pace": 68, "shooting": 50, "passing": 73, "dribbling": 72, "defending": 83, "physical": 76
        },
        {
            "player_id": "eric-garcia",
            "name": "Eric García",
            "team": "FC Barcelona",
            "position": "CB",
            "rating": 78,
            "preferred_foot": "Right",
            "pace": 70, "shooting": 45, "passing": 75, "dribbling": 73, "defending": 78, "physical": 71
        },
        {
            "player_id": "alejandro-balde",
            "name": "Alejandro Balde",
            "team": "FC Barcelona",
            "position": "LB",
            "rating": 83,
            "preferred_foot": "Left",
            "pace": 91, "shooting": 58, "passing": 75, "dribbling": 82, "defending": 77, "physical": 74
        },
        {
            "player_id": "hector-fort",
            "name": "Héctor Fort",
            "team": "FC Barcelona",
            "position": "RB",
            "rating": 73,
            "preferred_foot": "Right",
            "pace": 81, "shooting": 52, "passing": 70, "dribbling": 73, "defending": 71, "physical": 69
        },
        {
            "player_id": "gerard-martin",
            "name": "Gerard Martín",
            "team": "FC Barcelona",
            "position": "LB",
            "rating": 72,
            "preferred_foot": "Left",
            "pace": 78, "shooting": 48, "passing": 68, "dribbling": 71, "defending": 71, "physical": 70
        },
        # Midfielders
        {
            "player_id": "pedri",
            "name": "Pedri",
            "team": "FC Barcelona",
            "position": "CM",
            "rating": 88,
            "preferred_foot": "Right",
            "pace": 79, "shooting": 75, "passing": 89, "dribbling": 90, "defending": 68, "physical": 71
        },
        {
            "player_id": "frenkie-de-jong",
            "name": "Frenkie de Jong",
            "team": "FC Barcelona",
            "position": "CM",
            "rating": 87,
            "preferred_foot": "Right",
            "pace": 80, "shooting": 71, "passing": 87, "dribbling": 89, "defending": 78, "physical": 78
        },
        {
            "player_id": "dani-olmo",
            "name": "Dani Olmo",
            "team": "FC Barcelona",
            "position": "CAM",
            "rating": 86,
            "preferred_foot": "Right",
            "pace": 78, "shooting": 83, "passing": 86, "dribbling": 87, "defending": 50, "physical": 68
        },
        {
            "player_id": "gavi",
            "name": "Gavi",
            "team": "FC Barcelona",
            "position": "CM",
            "rating": 85,
            "preferred_foot": "Right",
            "pace": 78, "shooting": 72, "passing": 81, "dribbling": 85, "defending": 77, "physical": 82
        },
        {
            "player_id": "fermin-lopez",
            "name": "Fermín López",
            "team": "FC Barcelona",
            "position": "CAM",
            "rating": 82,
            "preferred_foot": "Right",
            "pace": 81, "shooting": 80, "passing": 78, "dribbling": 81, "defending": 62, "physical": 73
        },
        {
            "player_id": "marc-casado",
            "name": "Marc Casadó",
            "team": "FC Barcelona",
            "position": "CDM",
            "rating": 80,
            "preferred_foot": "Right",
            "pace": 76, "shooting": 65, "passing": 81, "dribbling": 79, "defending": 79, "physical": 77
        },
        {
            "player_id": "marc-bernal",
            "name": "Marc Bernal",
            "team": "FC Barcelona",
            "position": "CDM",
            "rating": 78,
            "preferred_foot": "Left",
            "pace": 73, "shooting": 66, "passing": 80, "dribbling": 77, "defending": 78, "physical": 79
        },
        {
            "player_id": "pablo-torre",
            "name": "Pablo Torre",
            "team": "FC Barcelona",
            "position": "CAM",
            "rating": 76,
            "preferred_foot": "Right",
            "pace": 75, "shooting": 74, "passing": 78, "dribbling": 79, "defending": 48, "physical": 62
        },
        # Forwards
        {
            "player_id": "lamine-yamal",
            "name": "Lamine Yamal",
            "team": "FC Barcelona",
            "position": "RW",
            "rating": 89,
            "preferred_foot": "Left",
            "pace": 93, "shooting": 83, "passing": 86, "dribbling": 92, "defending": 45, "physical": 71
        },
        {
            "player_id": "raphinha",
            "name": "Raphinha",
            "team": "FC Barcelona",
            "position": "LW",
            "rating": 87,
            "preferred_foot": "Left",
            "pace": 90, "shooting": 85, "passing": 84, "dribbling": 87, "defending": 54, "physical": 76
        },
        {
            "player_id": "ferran-torres",
            "name": "Ferran Torres",
            "team": "FC Barcelona",
            "position": "ST",
            "rating": 81,
            "preferred_foot": "Right",
            "pace": 83, "shooting": 80, "passing": 76, "dribbling": 80, "defending": 45, "physical": 73
        },
        {
            "player_id": "pau-victor",
            "name": "Pau Víctor",
            "team": "FC Barcelona",
            "position": "ST",
            "rating": 75,
            "preferred_foot": "Right",
            "pace": 81, "shooting": 76, "passing": 70, "dribbling": 75, "defending": 38, "physical": 71
        },
        {
            "player_id": "ansu-fati",
            "name": "Ansu Fati",
            "team": "FC Barcelona",
            "position": "LW",
            "rating": 77,
            "preferred_foot": "Right",
            "pace": 81, "shooting": 76, "passing": 72, "dribbling": 79, "defending": 32, "physical": 60
        },
    ]

    print(f"Syncing {len(fcb_squad)} official FC Barcelona players to Firestore...")
    for player in fcb_squad:
        pid = player["player_id"]
        coll.document(pid).set(player)
        print(f"✓ Saved {player['name']} ({player['position']}, Rating: {player['rating']})")

    print("\nFC Barcelona Squad Sync Complete!")

if __name__ == "__main__":
    sync_fcb_squad()

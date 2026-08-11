"""Firestore tools for managing soccer player database."""

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# HARDCODED project ID string as required for Agent Platform deployment safety
PROJECT_ID = "qwiklabs-gcp-04-0fa1cb8107fc"
COLLECTION_NAME = "players"


def get_firestore_client() -> firestore.Client:
    """Returns a Firestore client initialized with hardcoded project ID."""
    return firestore.Client(project=PROJECT_ID)


def search_players(team: str = "", position: str = "", min_rating: int = 0) -> str:
    """Searches players in the Firestore database based on team, position, or rating criteria.

    Args:
        team: Optional team name to filter by (e.g. 'Arsenal').
        position: Optional position abbreviation (e.g. 'RW', 'CAM', 'CB', 'ST', 'CDM').
        min_rating: Optional minimum overall rating (e.g. 80).

    Returns:
        Formatted string list of matching players and their key attributes.
    """
    db = get_firestore_client()
    query = db.collection(COLLECTION_NAME)

    if team:
        query = query.where(filter=FieldFilter("team", "==", team))
    if position:
        query = query.where(filter=FieldFilter("position", "==", position))
    if min_rating > 0:
        query = query.where(filter=FieldFilter("rating", ">=", min_rating))

    docs = list(query.stream())
    if not docs:
        return f"No players found matching criteria (team='{team}', position='{position}', min_rating={min_rating})."

    results = []
    for doc in docs:
        data = doc.to_dict()
        results.append(
            f"- [{data.get('player_id', doc.id)}] {data.get('name')} | Team: {data.get('team')} | "
            f"Pos: {data.get('position')} | Rating: {data.get('rating')} | Preferred Foot: {data.get('preferred_foot')} | "
            f"Pace: {data.get('pace')} | Shooting: {data.get('shooting')} | Passing: {data.get('passing')} | "
            f"Dribbling: {data.get('dribbling')} | Defending: {data.get('defending')} | Physical: {data.get('physical')}"
        )

    return f"Found {len(results)} player(s):\n" + "\n".join(results)


def get_player_details(player_id: str) -> str:
    """Retrieves full details for a specific player by player_id.

    Args:
        player_id: The unique ID string of the player (e.g. 'bukayo-saka').

    Returns:
        Formatted player attribute details string or error message if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(player_id.lower().strip())
    doc = doc_ref.get()

    if not doc.exists:
        return f"Player with ID '{player_id}' not found in Firestore."

    data = doc.to_dict()
    return (
        f"Player Details for {data.get('name')}:\n"
        f"• ID: {data.get('player_id')}\n"
        f"• Team: {data.get('team')}\n"
        f"• Position: {data.get('position')}\n"
        f"• Rating: {data.get('rating')}\n"
        f"• Preferred Foot: {data.get('preferred_foot')}\n"
        f"• Stats: Pace {data.get('pace')}, Shooting {data.get('shooting')}, "
        f"Passing {data.get('passing')}, Dribbling {data.get('dribbling')}, "
        f"Defending {data.get('defending')}, Physical {data.get('physical')}"
    )


def add_or_update_player(
    player_id: str,
    name: str,
    team: str,
    position: str,
    rating: int,
    preferred_foot: str = "Right",
    pace: int = 75,
    shooting: int = 75,
    passing: int = 75,
    dribbling: int = 75,
    defending: int = 75,
    physical: int = 75,
) -> str:
    """Adds a new player card or updates an existing player's attributes in Firestore.

    Args:
        player_id: Unique slug identifier for the player (e.g. 'martin-odegaard').
        name: Full display name of the player.
        team: Club or national team name.
        position: Primary position abbreviation (e.g. 'RW', 'CAM', 'ST', 'CB', 'CDM').
        rating: Overall FIFA/EA Sports style rating (e.g. 88).
        preferred_foot: 'Left' or 'Right'.
        pace: Pace attribute (1-99).
        shooting: Shooting attribute (1-99).
        passing: Passing attribute (1-99).
        dribbling: Dribbling attribute (1-99).
        defending: Defending attribute (1-99).
        physical: Physical attribute (1-99).

    Returns:
        Confirmation message of creation or update in Firestore.
    """
    db = get_firestore_client()
    clean_id = player_id.lower().strip().replace(" ", "-")

    player_data = {
        "player_id": clean_id,
        "name": name,
        "team": team,
        "position": position,
        "rating": rating,
        "preferred_foot": preferred_foot,
        "pace": pace,
        "shooting": shooting,
        "passing": passing,
        "dribbling": dribbling,
        "defending": defending,
        "physical": physical,
    }

    doc_ref = db.collection(COLLECTION_NAME).document(clean_id)
    doc_ref.set(player_data, merge=True)

    return f"Successfully saved player '{name}' (ID: {clean_id}, Team: {team}, Rating: {rating}) to Firestore!"

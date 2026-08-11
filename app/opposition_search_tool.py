"""Web search tool specifically for opposition team news, injuries, suspensions, and expected lineups."""

from ddgs import DDGS


def fetch_opposition_news_and_injuries(team_name: str) -> str:
    """Searches live news sources for an opposition team's latest squad news, injuries, suspensions, press conferences, and projected starting lineups.

    Args:
        team_name: The name of the opposition team (e.g., 'Real Madrid', 'Atletico Madrid', 'Bayern Munich', 'PSG').

    Returns:
        Formatted summary of recent web articles, injury updates, suspension notices, and lineup predictions for the target team.
    """
    queries = [
        f"{team_name} predicted lineup expected starting XI injuries news",
        f"{team_name} injury report suspended players squad news",
    ]

    all_snippets = []
    seen_urls = set()

    for q in queries:
        try:
            results = list(DDGS().text(q, max_results=4))
            for r in results:
                url = r.get("href", "")
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_snippets.append(
                        f"• **{r.get('title', 'Article')}**\n"
                        f"  Summary: {r.get('body', 'No snippet')}\n"
                        f"  Source: {url}"
                    )
        except Exception as e:
            all_snippets.append(f"Search warning for query '{q}': {e}")

    if not all_snippets:
        return f"No live opposition news found for '{team_name}'."

    return (
        f"Live News & Injury Search Results for {team_name}:\n\n"
        + "\n\n".join(all_snippets)
    )

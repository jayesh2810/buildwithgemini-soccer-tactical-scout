"""Web search tool for fetching live squad information, transfer news, and player rosters."""

from ddgs import DDGS


def search_web_for_squad_info(query: str) -> str:
    """Searches the internet for real-time soccer team squads, transfer news, player stats, or roster updates.

    Args:
        query: The search query string (e.g., 'FC Barcelona squad roster', 'Arsenal latest transfer news').

    Returns:
        A formatted string summary of top web search results with title, snippet body, and source URLs.
    """
    try:
        results = list(DDGS().text(query, max_results=5))
        if not results:
            return f"No live search results found for query: '{query}'."

        formatted_snippets = []
        for idx, r in enumerate(results, 1):
            title = r.get("title", "No Title")
            snippet = r.get("body", "No Snippet")
            url = r.get("href", "")
            formatted_snippets.append(
                f"{idx}. **{title}**\n   Snippet: {snippet}\n   URL: {url}"
            )

        return (
            f"Web Search Results for '{query}':\n\n"
            + "\n\n".join(formatted_snippets)
        )
    except Exception as e:
        return f"Error executing web search for query '{query}': {e}"

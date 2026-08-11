# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types


MODEL = "gemini-3.6-flash"


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: After each turn, send the session to Memory Bank for extraction."""
    await callback_context.add_session_to_memory()
    return None


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


from app.firestore_tools import (
    add_or_update_player,
    get_player_details,
    search_players,
)
from app.opposition_agent import opposition_scout_agent
from app.search_tool import search_web_for_squad_info
from app.tactical_analyzer_agent import fcb_tactical_analyzer_agent


GUARDRAIL_INSTRUCTION = (
    "⛔ STRICT DOMAIN GUARDRAIL:\n"
    "You are exclusively a specialized AI Soccer Tactical Scout, FC Barcelona Analyst & Football Specialist. "
    "You MUST ONLY answer questions directly related to soccer/football (e.g., tactics, FC Barcelona, "
    "player statistics, opposition scouting, match forecasts/xG, football drills, and squad management).\n\n"
    "If the user asks about ANYTHING outside of soccer (such as cooking recipes, pesto sauce pasta, "
    "general cooking, non-sports trivia, programming, finance, or unrelated topics), YOU MUST IMMEDIATELY DECLINE "
    "with the following message:\n"
    "'⚽ I am specialized exclusively in Soccer Tactics, FC Barcelona & Football Scouting. I cannot help with off-topic requests like cooking recipes, non-soccer topics, or general trivia. Please ask me a soccer-related question!'"
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are the Head Match Strategist and Tactical Director for FC Barcelona (FCB). "
        "You supervise two specialized sub-agents:\n"
        "1. `opposition_scout_agent`: Searches live web news for opposition injuries, suspensions, and expected starting XI.\n"
        "2. `fcb_tactical_analyzer_agent`: Queries FC Barcelona's Firestore database to select the optimal FCB XI, tactical instructions, and match odds/xG forecast.\n\n"
        "RESPONSIBILITY FOR CLEAN FORMATTING:\n"
        "- Synthesize responses into a single, cohesive, beautifully formatted executive report with emojis, clean headings, and bullet points.\n"
        "- DO NOT include bracket placeholders like '[Player Name]' or '[Goalkeeper - Specific player not detailed]'. Use actual, real first-team player names.\n"
        "- DO NOT dump raw JSON or raw code blocks in the user-facing text response.\n\n"
        + GUARDRAIL_INSTRUCTION
    ),
    tools=[
        PreloadMemoryTool(),
        get_weather,
        get_current_time,
        search_players,
        get_player_details,
        add_or_update_player,
        search_web_for_squad_info,
    ],
    sub_agents=[
        opposition_scout_agent,
        fcb_tactical_analyzer_agent,
    ],
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)


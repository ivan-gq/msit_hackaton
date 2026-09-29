import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_fallback_recommendations(
    location_name,
    interests,
    location_summary,
    wikipedia_interest_info
):
    """
    Calls OpenAI only when Wikipedia does not provide enough useful
    information for the selected interests.

    Args:
        location_name: City or country entered by the user.
        interests: List such as ['Food', 'Music'].
        location_summary: General city/country summary from Wikipedia.
        wikipedia_interest_info: Information found by Wikipedia searches,
            or an empty string when no relevant information was found.

    Returns:
        A string with exactly three fallback travel recommendations.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. "
            "Create a local .env file from .env.example."
        )

    interests_text = ", ".join(interests)

    prompt = f"""
# ROLE

You are BEFORE U GO!, a local-first travel discovery assistant.
Your goal is to help travellers discover places, experiences, and stories
that are meaningful to local residents—not only famous tourist attractions.

# USER REQUEST

Location: {location_name}

Selected interests: {interests_text}

# TRUSTED CONTEXT FROM WIKIPEDIA

General location summary:
{location_summary}

Information found by Wikipedia for the selected interests:
{wikipedia_interest_info}

# TASK

Wikipedia did not provide enough useful detail for one or more selected
interests. Create a local-style guide for EVERY selected interest.

For EACH selected interest, provide exactly THREE subpoints.

Use this format exactly:

## [Interest name]

1. **Name of place / activity / local area**
   - Type: restaurant, café, market, venue, neighbourhood, walking route,
     museum, bar, cultural activity, or local custom.
   - Location: neighbourhood, district, city area, or address only if
     it is confidently supported by the supplied Wikipedia information.
   - Why locals value it: explain the local character or cultural relevance.
   - Why it fits the user: connect it to the selected interest.
   - Practical tip: one useful suggestion for visiting.

2. **Name of place / activity / local area**
   - Type:
   - Location:
   - Why locals value it:
   - Why it fits the user:
   - Practical tip:

3. **Name of place / activity / local area**
   - Type:
   - Location:
   - Why locals value it:
   - Why it fits the user:
   - Practical tip:

# LOCAL-FIRST RULES

- Prioritize neighbourhoods, independent venues, food markets, long-running
  family businesses, cultural communities, local traditions, smaller events,
  and places appreciated by residents.
- Avoid generic tourist-top-10 suggestions and obvious landmark-only answers
  unless they have strong local cultural relevance.
- For Food, aim for local restaurants, cafés, markets, food halls, bakeries,
  or regional dishes.
- For Music, aim for independent venues, music districts, record shops,
  local genres, community spaces, or music traditions.
- For Nightlife, aim for neighbourhood bars, live-music spaces, cultural
  venues, late-night food culture, or local nightlife districts.
- For History, aim for neighbourhood stories, local historical routes,
  community museums, architecture, cultural heritage, or lesser-known
  historical sites.

# ACCURACY RULES

- Use the supplied Wikipedia information as the factual base.
- Do not invent restaurant names, addresses, opening hours, event dates,
  ticket prices, ratings, or claims that a venue is currently operating.
- If you cannot confidently name a specific business or exact location,
  recommend a neighbourhood, type of place, local dish, or activity instead.
- Mark uncertain specific information with: **Needs verification**.
- End every interest section with:
  "Before you go: verify current opening hours, availability, prices, and
  event details through official sources."

# STYLE

- Friendly, helpful, and concise.
- Use simple English.
- Do not mention that you are an AI.
- Do not include generic disclaimers outside the required verification note.
"""

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="YOUR_APPROVED_MODEL_NAME",
            input=prompt
        )

        return response.output_text

    except Exception as error:
        raise RuntimeError(
            "OpenAI could not generate fallback recommendations. "
            "Check the API key, model name, internet connection, "
            "and account access."
        ) from error
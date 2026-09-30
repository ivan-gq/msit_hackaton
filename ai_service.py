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
You are BEFORE U GO!, a local-first travel discovery assistant.

Your goal is to help travellers discover authentic places and experiences
valued by local residents, not only famous tourist attractions.

Location: {location_name}
Selected interest: {interests_text}

Wikipedia city summary:
{location_summary}

Wikipedia information related to the selected interest:
{wikipedia_interest_info}

Use the Wikipedia information as background context. Then use web search to
verify current places and location details before answering.

Create exactly THREE local-first recommendations for the selected interest.

For each recommendation, use this exact format:

Interest:

1. Place or activity name
   - Type: restaurant, café, market, venue, bar, neighbourhood,
     historical site, or local activity
   - Exact location: street address or clear neighbourhood/district
   - Why locals value it: one short sentence
   - Practical tip: one short sentence
   - Google Maps: https://www.google.com/maps/search/?api=1&query=URL_ENCODED_PLACE_NAME_AND_CITY
   - Sources: include the web source URLs used to verify the place

2. Place or activity name
   - Type:
   - Exact location:
   - Why locals value it:
   - Practical tip:
   - Google Maps:
   - Sources:

3. Place or activity name
   - Type:
   - Exact location:
   - Why locals value it:
   - Practical tip:
   - Google Maps:
   - Sources:

Rules:
- Prioritize independent places, neighbourhood favourites, local markets,
  bakeries, cafés, cultural venues, community spaces, and lesser-known
  historical experiences.
- Avoid generic tourist top-10 attractions unless they have clear local value.
- Use web search to verify that named businesses and addresses are current.
- Do not invent names, addresses, reviews, opening hours, ratings, or links.
- If you cannot verify an exact place or address, recommend a neighbourhood
  or activity instead and write: Needs verification.
- Create a valid Google Maps search URL by using the exact place name and
  city in the query parameter.
- Keep each recommendation under 80 words.
- Use simple, friendly English.
- Do not mention that you are an AI.
"""

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
            tools=[
                {
                    "type": "web_search"
                }
            ]
        )

        return response.output_text

    except Exception as error:
        raise RuntimeError(
            "OpenAI could not generate fallback recommendations. "
            "Check the API key, model name, internet connection, "
            "and account access."
        ) from error
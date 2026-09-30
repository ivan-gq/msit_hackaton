# BEFORE U GO!

> **Know the place before you go.**

BEFORE U GO! is a Python console-based travel discovery app that helps users learn more about a city before visiting it. The app first searches Wikipedia for a factual city summary and information related to the user’s chosen interest. If Wikipedia does not provide useful information, the app uses the OpenAI API to create a local-first travel guide.

The project focuses on discovering local character—not only the famous tourist attractions found in ordinary top-10 lists.

---

## Project idea

Travellers often find plenty of general information about famous landmarks, but it can be difficult to discover local food, music, history, nightlife, neighbourhoods, traditions, and lesser-known experiences.

BEFORE U GO! provides a simple workflow:

1. The user enters a city.
2. The app validates and normalizes the city name.
3. The user chooses an interest.
4. The app retrieves a general city summary from Wikipedia.
5. The app searches Wikipedia for information related to the selected interest.
6. If useful Wikipedia information is found, it is displayed.
7. If Wikipedia does not provide enough relevant information, OpenAI generates a local-first guide.
8. The user can explore another city or exit the application.

---

## Main features

- Console-based user interface.
- City-name validation using geocoding.
- Support for common city aliases and abbreviations such as `ldn` for London and `ber` for Berlin.
- Fuzzy matching for spelling mistakes in city names.
- Wikipedia city-summary retrieval.
- Wikipedia section search for selected categories.
- Interest categories including:
  - Music.
  - Food.
  - History.
- OpenAI fallback recommendations when Wikipedia has insufficient information.
- Local-first recommendations focused on neighbourhoods, independent places, markets, cultural spaces, local traditions, and lesser-known experiences.
- Console formatting with loading indicators and a typewriter-style presentation.
- Environment-variable protection for the OpenAI API key.

---

## How the information flow works

```text
User enters a city
        |
        v
City normalization and validation
        |
        v
Wikipedia city summary
        |
        v
Wikipedia search for the selected interest
        |
        +------------------------------+
        |                              |
Useful information found              No useful information found
        |                              |
        v                              v
Display Wikipedia information          Send context to OpenAI
                                       |
                                       v
                              Generate local-first guide
                                       |
                                       v
                              Display recommendations
```

Wikipedia is used as the first information source. OpenAI is used as a fallback and refinement service when the selected interest is not sufficiently covered by Wikipedia.

---

## Example user journey

```text
Welcome to BEFORE U GO!

Type the city you want to visit: ber

City: Berlin
Country: Germany

Summary:
Berlin is the capital and largest city of Germany...

Let's go deeper:
1. Music
2. Food
3. History
```

If Wikipedia has a relevant section, the app displays that information. If it does not, the app asks OpenAI to generate three concise, local-first recommendations for the selected interest.

---

## Technologies used

- **Python** — Main programming language.
- **Wikipedia-API** — Retrieves Wikipedia summaries and section content.
- **OpenAI Python SDK** — Generates fallback and refined travel recommendations.
- **python-dotenv** — Loads the OpenAI API key from a local `.env` file.
- **RapidFuzz** — Handles fuzzy matching and spelling correction for city names.
- **GeoPy** — Uses OpenStreetMap Nominatim to validate and geocode places.
- **Unidecode** — Converts accented place names into readable Latin characters where needed.
- **PyFiglet** — Creates the console title banner.
- **Rich** — Displays console status messages and loading indicators.
- **Git/GitHub** — Version control and team collaboration.

---

## Project structure

```text
msit_hackaton/
|
|-- main.py                 # Main console application and user flow
|-- ai_service.py           # OpenAI fallback and refinement service
|-- wiki_summary.py         # Wikipedia summary and category search
|-- cities_data.py          # City data used by the application
|-- requirements.txt        # Python dependencies
|-- .env.example            # Safe environment-variable template
|-- .gitignore              # Files excluded from Git
|-- README.md               # Project documentation
|-- .env                    # Local secret file; never commit this
`-- venv/                   # Local virtual environment; never commit this
```

---

## Requirements

- Python 3.10 or newer.
- Internet connection.
- An authorized OpenAI API key for the AI fallback feature.
- Git, if you want to clone or contribute to the project.

The OpenStreetMap Nominatim service also requires the application to identify itself with a descriptive user agent. The project configures a user agent for this purpose.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ivan-gq/msit_hackaton.git
cd msit_hackaton
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
```

Activate it in Git Bash:

```bash
source venv/Scripts/activate
```

Activate it in PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## API key setup

The OpenAI API key must never be written directly into Python code or committed to GitHub.

### 1. Copy the environment template

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

#### Git Bash

```bash
cp .env.example .env
```

### 2. Open `.env`

Replace the placeholder with an authorized key:

```text
OPENAI_API_KEY=your-authorized-openai-api-key
```

The `.env` file is intentionally ignored by Git. It should remain only on the local computer that is authorized to run the OpenAI feature.

---

## Running the app

With the virtual environment activated, run:

```bash
python main.py
```

Then:

1. Enter a city or supported city alias.
2. Select an interest.
3. Read the Wikipedia summary and category information.
4. If Wikipedia lacks useful information, read the OpenAI-generated local guide.
5. Enter another city or quit the program.

---

## OpenAI fallback behaviour

The OpenAI service is implemented in `ai_service.py` through:

```python
generate_fallback_recommendations(
    location_name,
    interests,
    location_summary,
    wikipedia_interest_info
)
```

The function receives:

- The validated city name.
- The selected interest.
- The Wikipedia city summary.
- Any Wikipedia information found for that interest.

The prompt asks OpenAI to produce concise local-first suggestions. It prioritizes neighbourhoods, independent places, markets, cultural spaces, local traditions, and lesser-known experiences rather than generic tourist lists.

Any current details such as opening hours, prices, event schedules, or business availability should be verified through official sources before travel.

---

## Security notes

The following files must not be committed:

```text
.env
venv/
__pycache__/
*.pyc
.idea/
```

The repository includes `.env.example`, which is safe to share because it contains only a placeholder:

```text
OPENAI_API_KEY=put-your-authorized-api-key-here
```

If a real API key is ever committed to GitHub, revoke or rotate it immediately.

---

## Testing

A small local API test can be created as `test_ai_service.py`:

```python
from ai_service import generate_fallback_recommendations


result = generate_fallback_recommendations(
    location_name="Berlin",
    interests=["Food"],
    location_summary=(
        "Berlin is the capital and largest city of Germany. "
        "It is known for its history, cultural diversity, and creative life."
    ),
    wikipedia_interest_info=""
)

print(result)
```

Run it with:

```bash
python test_ai_service.py
```

The test should be used carefully because an OpenAI API request may consume account usage.

---

## Known limitations

- The MVP depends on an internet connection.
- Wikipedia may not contain a dedicated section for every category.
- OpenAI-generated recommendations require verification before travel.
- The app does not currently provide bookings, payments, accounts, or saved itineraries.
- The app does not guarantee live opening hours, prices, event schedules, or availability.
- City names with multiple possible meanings may require a more specific input.
- Nominatim requests should not be sent in bulk or repeatedly because public geocoding services have usage limits.

---

## Future improvements

- Add a web or mobile interface.
- Add Google Maps or another verified places service.
- Add current events and festival information.
- Add direct links to official venue and tourism pages.
- Add support for more languages.
- Add user profiles and saved travel plans.
- Add filters for budget, family-friendly activities, accessibility, and trip duration.
- Add a source and verification date for each recommendation.
- Add community-submitted local tips with moderation.
- Add itinerary generation for one-day, weekend, and week-long trips.

---

## Team

This project was created as part of the Masterschool GenAI Engineering hackathon.

Contributors:

- Ivan GQ
- Binu Dio
- Syed Nafifur Rahman

---

## Project message

> BEFORE U GO! helps travellers know the place before they go—starting with reliable city context from Wikipedia and adding personalized local discovery with OpenAI when more information is needed.

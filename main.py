import os
from cities_data import CITY_ALIASES, KNOWN_CITIES
from rapidfuzz import process, fuzz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from ai_service import generate_fallback_recommendations
import wikipediaapi
from unidecode import unidecode
import pyfiglet
from rich.console import Console
import sys
import time

console = Console(force_terminal=True, force_interactive=True)
os.environ["PYTHONUNBUFFERED"] = "1"

CATEGORY_KEYWORDS = {
    "Music": ["music", "concert", "opera", "nightlife", "festival", "performing arts", "entertainment"],
    "Food": ["food", "cuisine", "culinary", "gastronomy", "dining", "restaurant"],
    "History": ["history", "heritage", "etymology"],
}

wiki = wikipediaapi.Wikipedia(
    user_agent='MSIT_HACKATON_app',
    language='en'
)

def clear_terminal():
    # 'cls' for Windows (nt), 'clear' for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')


def get_category_info(city, category, max_chars=10000):
    """Returns the text of the sections whose heading contains a keyword of the category.
    Returns an empty string if nothing matched."""
    page = wiki.page(city)
    if not page.exists():
        return ""

    keywords = CATEGORY_KEYWORDS[category]
    found = []

    def search(sections):
        for section in sections:
            if any(keyword in section.title.lower() for keyword in keywords):
                found.append(section.full_text())
            else:
                search(section.sections)

    search(page.sections)
    return "\n\n".join(found)[:max_chars]


def normalize_input(user_input: str) -> str:
    """
    Pre-processes input using explicit aliases first, then rapidfuzz
    for matching against KNOWN_CITIES.
    """
    cleaned = user_input.strip()
    if not cleaned:
        return user_input

    # Step 1: Exact alias check (e.g., "ldn" -> "London")
    lowercased = cleaned.lower()
    if lowercased in CITY_ALIASES:
        return CITY_ALIASES[lowercased]

    # Step 2: High-speed fuzzy match using RapidFuzz
    # score_cutoff=75.0 requires a minimum 75% similarity (0–100 scale)
    match = process.extractOne(
        query=cleaned.title(),
        choices=KNOWN_CITIES,
        scorer=fuzz.WRatio,
        score_cutoff=75.0
    )

    if match:
        # match is a tuple: (matched_string, score, index)
        matched_city = match[0]
        return matched_city

    # Fallback to title-cased raw input if no match met the threshold
    return cleaned.title()


def validate_place(user_input: str) -> dict:
    """Returns dictonary: 'is_valid': Bool, query: city name and geocoded_address (if its a place)
    """
    if not user_input or len(user_input.strip()) < 2:
        return {"is_valid": False, "query": user_input, "geocoded_address": None}

    # Clean and normalize the input first
    normalized_city = normalize_input(user_input)

    # Pass the clean string to geopy
    geolocator = Nominatim(user_agent="city_normalizer_app")
    try:
        location = geolocator.geocode(normalized_city, addressdetails=True, timeout=5)
        if not location:
            return {"is_valid": False, "normalized_query": normalized_city, "geocoded_address": None}


        raw_address = location.raw.get("address", {})
        valid_place_types = {
            "city", "town", "village", "municipality"
        }

        is_place = any(place_type in raw_address for place_type in valid_place_types)

        return {
            "is_valid": is_place,
            "original_input": user_input,
            "normalized_query": normalized_city,
            "geocoded_address": location.address if is_place else None
        }

    except (GeocoderTimedOut, GeocoderServiceError):
        return {"is_valid": False, "query": normalized_city, "geocoded_address": None}


def get_wiki_summary(topic):
    # Initialize the API with a required User-Agent (you can leave this example text as is)
    wiki = wikipediaapi.Wikipedia(
        user_agent='MSIT_HACKATON_app',
        language='en'
    )


    # Fetch the page
    page = wiki.page(topic)

    # Check if the page actually exists
    if page.exists():
        # Get the summary, split it by periods, take the first 3, and stick them back together
        sentences = page.summary.split('. ')
        short_summary = '. '.join(sentences[:3]) + '.'
        return short_summary
    else:
        return "Sorry, I couldn't find a Wikipedia page for that."


def typewriter(text: str, delay: float = 0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Forces character to print immediately
        time.sleep(delay)
    print()  # Add a newline at the end


def print_menu():
    clear_terminal()
    print("Welcome to")
    ascii_banner = pyfiglet.figlet_format("Welcome to . . .", font="standard")
    print(ascii_banner)
    time.sleep(0.5)
    ascii_banner = pyfiglet.figlet_format("BEFORE YOU GO", font="slant")
    print(ascii_banner)
    print("---------------------------------------------------------------------------")
    typewriter("We help you get all the insider information on the place you want to go.")


def main():
    menu_input = 0
    print_menu()
    while True:
        raw_input = input("Type the city you want to visit: ('q' to exit) ").strip()
        #Let the user quit
        if raw_input == "q":
            clear_terminal()
            ascii_banner = pyfiglet.figlet_format("Bye bye ! ! !", font="slant")
            print(ascii_banner)
            typewriter("Thanks for using BEFORE YOU GO!")
            time.sleep(2)
            clear_terminal()
            break

        valid_place = validate_place(raw_input)
        #Check if place is valid and
        if valid_place["is_valid"]:

            city_info = valid_place["geocoded_address"].split(",")
            #use these variables for city
            uni_city = unidecode(city_info[0])
            # use these variables for country
            uni_country = unidecode(city_info[-1])

            print(f"\nCity: {uni_city}\nCountry: {uni_country}\n")

            with console.status("[bold green]Asking wikipedia...[/bold green]", spinner="dots"):
                print(f"Summery:\n{get_wiki_summary(uni_city)}")
            typewriter("\n\nLets go deeper, type number of menu item:")
            while True:
                menu_input = input("1. Music // 2. Food // 3. History (type 'q' to enter city again): ")
                if menu_input == "q":
                    print_menu()
                    break
                else:
                    try:
                        menu_item = int(menu_input)
                        if menu_item not in [1,2,3]:
                            print("Not a valid input")
                        elif menu_item == 1:
                            with console.status("[bold green]Asking wikipedia...[/bold green]", spinner="dots"):
                                result = get_category_info(uni_city, "Music", max_chars=3000)
                            if result != "":
                                print(result)
                            else:
                                print("Nothing on wikipedia, asking AI")
                                with console.status("[bold green]Asking ChatGPT...[/bold green]", spinner="dots"):
                                    result = generate_fallback_recommendations(
                                        location_name = uni_city,
                                        interests = ["Music"],
                                        location_summary = (),
                                        wikipedia_interest_info=""
                                    )
                                print(result)
                        elif menu_item == 2:
                            with console.status("[bold green]Asking wikipedia...[/bold green]", spinner="dots"):
                                result = get_category_info(uni_city, "Food", max_chars=3000)
                            if result != "":
                                print(result)
                            else:
                                print("Nothing on wikipedia, asking AI")
                                with console.status("[bold green]Asking ChatGPT...[/bold green]", spinner="dots"):
                                    result = generate_fallback_recommendations(
                                        location_name = uni_city,
                                        interests = ["Food"],
                                        location_summary = (),
                                        wikipedia_interest_info=""
                                    )
                                print(result)
                        elif menu_item == 3:
                            with console.status("[bold green]Asking wikipedia...[/bold green]", spinner="dots"):
                                result = get_category_info(uni_city, "History", max_chars=3000)
                            if result != "":
                                print(result)
                            else:
                                print("Nothing on wikipedia, asking AI")
                                with console.status("[bold green]Asking ChatGPT...[/bold green]", spinner="dots"):
                                    result = generate_fallback_recommendations(
                                        location_name = uni_city,
                                        interests = ["History"],
                                        location_summary = (),
                                        wikipedia_interest_info=""
                                    )
                                print(result)
                    except ValueError:
                        print("Must be number")
        else:
            print("No such city, please re enter the city")


if __name__ == "__main__":
    main()
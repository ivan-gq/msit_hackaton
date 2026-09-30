import os
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

# 1. Known Aliases / Slang / Abbreviations
CITY_ALIASES = {
    # UK / Ireland
    "ldn": "London", "mcr": "Manchester", "brum": "Birmingham", "dub": "Dublin",
    
    # Germany / Central Europe
    "hh": "Hamburg", "ber": "Berlin", "muc": "Munich", "fra": "Frankfurt",
    "cgn": "Cologne", "dus": "Düsseldorf", "vie": "Vienna", "zrh": "Zurich",
    
    # Rest of Europe
    "par": "Paris", "bcn": "Barcelona", "mad": "Madrid", "ams": "Amsterdam",
    "rom": "Rome", "lis": "Lisbon", "cph": "Copenhagen", "sto": "Stockholm",
    
    # Americas
    "nyc": "New York", "ny": "New York", "la": "Los Angeles", "lax": "Los Angeles",
    "chi": "Chicago", "sf": "San Francisco", "sfo": "San Francisco", "sea": "Seattle",
    "bos": "Boston", "dc": "Washington", "atx": "Austin", "mia": "Miami",
    "vegas": "Las Vegas", "pto": "Porto", "yvr": "Vancouver", "yyz": "Toronto",
    
    # Asia / Oceania
    "tky": "Tokyo", "hk": "Hong Kong", "sg": "Singapore", "kl": "Kuala Lumpur",
    "syd": "Sydney", "mel": "Melbourne", "dxb": "Dubai"
}

# 2. Canonical Target Cities for Fuzzy Correction
KNOWN_CITIES = [
    # United Kingdom & Ireland
    "London", "Manchester", "Birmingham", "Liverpool", "Edinburgh", "Glasgow", 
    "Leeds", "Bristol", "Belfast", "Dublin", "Cork", "Newcastle", "Sheffield",
    "Nottingham", "Cardiff", "Oxford", "Cambridge", "Southampton", "Brighton",

    # Germany & Central Europe
    "Hamburg", "Berlin", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", 
    "Dortmund", "Essen", "Leipzig", "Bremen", "Dresden", "Hannover", "Nuremberg", 
    "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster", "Vienna", 
    "Zurich", "Geneva", "Basel", "Bern", "Prague", "Warsaw", "Krakow", "Budapest",

    # Western & Southern Europe
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Bordeaux", "Lille", "Rennes", "Brussels", "Antwerp", "Amsterdam", "Rotterdam", 
    "The Hague", "Utrecht", "Madrid", "Barcelona", "Valencia", "Seville", "Malaga", 
    "Zaragoza", "Lisbon", "Porto", "Rome", "Milan", "Naples", "Turin", "Palermo", 
    "Genoa", "Bologna", "Florence", "Athens", "Thessaloniki",

    # Northern & Eastern Europe
    "Copenhagen", "Stockholm", "Gothenburg", "Oslo", "Bergen", "Helsinki", 
    "Reykjavik", "Tallinn", "Riga", "Vilnius", "Bucharest", "Sofia", "Belgrade", 
    "Zagreb", "Ljubljana", "Bratislava", "Kyiv", "Kharkiv", "Odesa", "Istanbul",

    # North America
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", 
    "Fort Worth", "Columbus", "Charlotte", "Indianapolis", "San Francisco", 
    "Seattle", "Denver", "Washington", "Boston", "Nashville", "El Paso", 
    "Detroit", "Las Vegas", "Portland", "Memphis", "Louisville", "Baltimore", 
    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Mesa", 
    "Atlanta", "Kansas City", "Colorado Springs", "Miami", "Raleigh", "Omaha", 
    "Long Beach", "Virginia Beach", "Oakland", "Minneapolis", "Tampa", "Tulsa", 
    "Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", 
    "Winnipeg", "Quebec City", "Mexico City", "Guadalajara", "Monterrey",

    # South America
    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", 
    "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre", 
    "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Santiago", "Lima", 
    "Bogotá", "Medellín", "Cali", "Caracas", "Quito", "Guayaquil", "Montevideo",

    # Asia & Middle East
    "Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Kobe", "Kyoto", "Fukuoka", 
    "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Chongqing", 
    "Hangzhou", "Wuhan", "Xi'an", "Hong Kong", "Taipei", "Seoul", "Busan", 
    "Incheon", "Singapore", "Bangkok", "Kuala Lumpur", "Jakarta", "Manila", 
    "Hanoi", "Ho Chi Minh City", "Mumbai", "Delhi", "Bangalore", "Hyderabad", 
    "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Dubai", "Abu Dhabi", 
    "Riyadh", "Jeddah", "Doha", "Tel Aviv", "Jerusalem", "Amman", "Beirut",

    # Africa & Oceania
    "Cairo", "Alexandria", "Giza", "Johannesburg", "Cape Town", "Durban", 
    "Pretoria", "Nairobi", "Lagos", "Accra", "Casablanca", "Tunis", "Algiers", 
    "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Auckland", "Wellington"
]

def clear_terminal():
    # 'cls' for Windows (nt), 'clear' for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')


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

    
def typewriter(text: str, delay: float = 0.015):
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
            ascii_banner = pyfiglet.figlet_format("Bye bye!!!", font="slant")
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
                menu_input = input("1. Music // 2. Food // 3. History (type 'q' to enter city again) :")
                if menu_input == "q":
                    print_menu()
                    break
                else:
                    try:
                        menu_item = int(menu_input)
                        if menu_item not in [1,2,3]:
                            print("Not a valid input")
                        elif menu_item == 1:
                            with console.status("[bold green]Asking ChatGPT...[/bold green]", spinner="dots"):
                                result = generate_fallback_recommendations(
                                    location_name = uni_city,
                                    interests = ["Music"],
                                    location_summary = (
                                        "Berlin is the capital and largest city of Germany. "
                                        "It is known for its history, cultural diversity, and creative life."
                                    ),
                                    wikipedia_interest_info=""
                                )
                            print(result)
                        elif menu_item == 2:
                            with console.status("[bold green]Asking ChatGPT...[/bold green]", spinner="dots"):
                                result = generate_fallback_recommendations(
                                    location_name = uni_city,
                                    interests = ["Food"],
                                    location_summary = (
                                        "Berlin is the capital and largest city of Germany. "
                                        "It is known for its history, cultural diversity, and creative life."
                                    ),
                                    wikipedia_interest_info=""
                                )
                            print(result)
                        elif menu_item == 3:
                            with console.status("[bold green]Asking ChatGPT...[/bold green]", spinner="dots"):
                                result = generate_fallback_recommendations(
                                    location_name = uni_city,
                                    interests = ["History"],
                                    location_summary = (
                                        "Berlin is the capital and largest city of Germany. "
                                        "It is known for its history, cultural diversity, and creative life."
                                    ),
                                    wikipedia_interest_info=""
                                )
                            print(result)
                    except ValueError:
                        print("Must be number")
        else:
            print("No such city, please re enter the city")


if __name__ == "__main__":
    main()
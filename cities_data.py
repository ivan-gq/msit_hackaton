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
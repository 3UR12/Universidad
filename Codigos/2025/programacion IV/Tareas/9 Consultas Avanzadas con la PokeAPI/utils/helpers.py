from utils.peticiones_http import get_json

def get_all_pokemon(limit=1300):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    data = get_json(url)
    return data["results"] if data else []

def get_pokemon_details(name_or_url):
    url = name_or_url if name_or_url.startswith("http") else f"https://pokeapi.co/api/v2/pokemon/{name_or_url}"
    return get_json(url)

def get_species_details(name):
    return get_json(f"https://pokeapi.co/api/v2/pokemon-species/{name}")

def get_evolution_chain(url):
    return get_json(url)

def get_type_pokemon(type_name):
    data = get_json(f"https://pokeapi.co/api/v2/type/{type_name}")
    return [p["pokemon"]["name"] for p in data["pokemon"]] if data else []

def get_region_pokemon(region_name):
    region_data = get_json(f"https://pokeapi.co/api/v2/region/{region_name}")
    locations = [loc["name"] for loc in region_data["locations"]] if region_data else []
    species = set()
    for loc in locations:
        area_data = get_json(f"https://pokeapi.co/api/v2/location/{loc}")
        for area in area_data.get("areas", []):
            encounters = get_json(area["url"])
            for enc in encounters.get("pokemon_encounters", []):
                species.add(enc["pokemon"]["name"])
    return list(species)

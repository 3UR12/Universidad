from utils.helpers import *
from utils.peticiones_http import get_json
from collections import Counter
from tqdm import tqdm

def get_fire_pokemon_kanto():
    fire_pokemon = set(get_type_pokemon("fire"))
    kanto_pokemon = set(get_region_pokemon("kanto"))
    return len(fire_pokemon & kanto_pokemon)

def get_water_pokemon_tall():
    water_pokemon = get_type_pokemon("water")
    result = []
    for name in tqdm(water_pokemon, desc="Filtrando altura"):
        data = get_pokemon_details(name)
        if data and data["height"] > 10:
            result.append(data["name"])
    return result

def get_evolution_chain(pokemon_name):
    species = get_species_details(pokemon_name)
    evo_url = species.get("evolution_chain", {}).get("url") if species else None
    if not evo_url:
        return []

    return parse_evolution_chain(evo_url)

def parse_evolution_chain(url):
    data = get_json(url)
    result = []

    def traverse(node):
        result.append(node["species"]["name"])
        for evo in node.get("evolves_to", []):
            traverse(evo)

    if data and "chain" in data:
        traverse(data["chain"])
    return result

def get_electric_without_evolution():
    electric_pokemon = get_type_pokemon("electric")
    result = []
    for name in tqdm(electric_pokemon, desc="Buscando sin evolución"):
        species = get_species_details(name)
        if not species:
            continue

        evo_url = species.get("evolution_chain", {}).get("url")
        if not evo_url:
            result.append(name)
            continue

        chain = parse_evolution_chain(evo_url)
        if chain == [name]:  # Solo él en la cadena
            result.append(name)
    return result

def get_highest_attack_johto():
    johto_pokemon = get_region_pokemon("johto")
    max_attack = ("", 0)
    for name in tqdm(johto_pokemon, desc="Evaluando ataque"):
        data = get_pokemon_details(name)
        if data:
            for stat in data["stats"]:
                if stat["stat"]["name"] == "attack" and stat["base_stat"] > max_attack[1]:
                    max_attack = (name, stat["base_stat"])
    return max_attack

def get_fastest_non_legendary():
    all_pokemon = get_all_pokemon()
    max_speed = ("", 0)
    for p in tqdm(all_pokemon, desc="Evaluando velocidad"):
        name = p["name"]
        species = get_species_details(name)
        if species and not species["is_legendary"]:
            data = get_pokemon_details(name)
            for stat in data["stats"]:
                if stat["stat"]["name"] == "speed" and stat["base_stat"] > max_speed[1]:
                    max_speed = (name, stat["base_stat"])
    return max_speed

def get_common_grass_habitat():
    grass_pokemon = get_type_pokemon("grass")
    habitats = []
    for name in tqdm(grass_pokemon, desc="Recolectando hábitats"):
        species = get_species_details(name)
        if species and species["habitat"]:
            habitats.append(species["habitat"]["name"])
    return Counter(habitats).most_common(1)[0]

def get_lightest_pokemon():
    all_pokemon = get_all_pokemon()
    min_weight = ("", float("inf"))
    for p in tqdm(all_pokemon, desc="Buscando peso mínimo"):
        data = get_pokemon_details(p["name"])
        if data and data["weight"] < min_weight[1]:
            min_weight = (p["name"], data["weight"])
    return min_weight

import requests

BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon_info(name):
    url = f"{BASE_URL}/pokemon/{name.lower()}"
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to retrieve data: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error: {e}")
        return None


def display_pokemon_info(pokemon):
    print("\n--- Pokémon Info ---")
    print(f"Name: {pokemon['name'].capitalize()}")
    print(f"ID: {pokemon['id']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    
    # Extra: types
    types = [t['type']['name'] for t in pokemon['types']]
    print(f"Types: {', '.join(types)}")


def main():
    pokemon_name = input("Enter Pokémon name: ")
    pokemon_info = get_pokemon_info(pokemon_name)

    if pokemon_info:
        display_pokemon_info(pokemon_info)
    else:
        print("No data found.")


if __name__ == "__main__":
    main()
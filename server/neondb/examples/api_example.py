import sys
sys.path.append('C:/Users/User/Documents/NTU_WORK/Techfest2025/server')

from neondb.api import create_sample_heroes, get_heroes, get_hero

if __name__ == "__main__":
    # Create the heroes table in the database
    # create_sample_heroes()

    # Get all heroes from the database
    heroes = get_heroes()
    print("All heroes:")
    for hero in heroes:
        print(hero)

    # Get a hero by ID from the database
    hero = get_hero(1)
    print("Hero with ID 1:")
    print(hero)

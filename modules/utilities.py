import sqlite3
import json

DATABASE_PATH = 'databases/ptcgp.db'

valid_types = [
    'grass',
    'fire',
    'water',
    'lightning',
    'fighting',
    'psychic',
    'colorless',
    'darkness',
    'metal',
    'dragon'
]



def move_list_copies(move_name):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # getting the number of copies from the move database
        cursor.execute(f'select * from move where move_name = \"{move_name}\"')
        copies = cursor.fetchall()
        num_counts = len(copies)

        # there are no copies of the move
        if num_counts == 0:
            print(f'No copies of {move_name} found in move database')
            return
        
        # printing all copies of the current move
        for move in copies:
            move_id, move_name, description, base_damage, cost, effects = move

            print(f'[MOVE_ID # {move_id}] {move_name}\n\tDescription: {description}\n\tBase Damage: {base_damage}\n\tCost: {cost}\n\tEffects: {effects}\n')
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def ability_list_copies(ability_name):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # getting the number of copies from the ability database
        cursor.execute(f'select * from ability where ability_name = \"{ability_name}\"')
        copies = cursor.fetchall()
        num_counts = len(copies)

        # there are no copies of the ability
        if num_counts == 0:
            print(f'No copies of {ability_name} found in ability database')
            return
        
        # printing all copies of the current ability
        for ability in copies:
            ability_id, ability_name, description, activable, active_req, repeatable, effects = ability

            print(f'[ABILITY_ID # {ability_id}] {ability_name}\n\tDescription: {description}\n\tActivable: {activable}\n\tActive Req: {active_req}\n\tRepeatable: {repeatable}\n\tEffects: {effects}\n')
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def pokemon_card_list_copies(pokemon_name, display_id_names = False):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # getting the number of copies from the pokemon_name database
        cursor.execute(f'select * from pokemon_card where pokemon_name = \"{pokemon_name}\"')
        copies = cursor.fetchall()
        num_counts = len(copies)

        # there are no copies of the pokemon
        if num_counts == 0:
            print(f'No copies of {pokemon_name} found in pokemon_name database')
            return
        
        # printing all copies of the current pokemon
        for pokemon in copies:
            pokemon_id, card_id, pokemon_name, pokemon_type, is_ex, base_hp, stage, evolution_name, move_1_id, move_2_id, ability_id, weakness, retreat_cost = pokemon

            # we can display the move/ability names instead of the IDs
            if display_id_names:
                move_1_name, move_2_name, ability_name = 'None'

                # getting move 1 name
                if move_1_id != -1:
                    cursor.execute(f'select move_name from move where move_id = {move_1_id}')
                    move_1_name = cursor.fetchall()[0][0]
                
                # getting move 2 name
                if move_2_id != -1:
                    cursor.execute(f'select move_name from move where move_id = {move_2_id}')
                    move_2_name = cursor.fetchall()[0][0]

                # getting ability name
                if ability_id != -1:
                    cursor.execute(f'select ability_name from ability where ability_id = {ability_id}')
                    ability_name = cursor.fetchall()[0][0]

                # printing our information
                print(f'[POKEMON_ID # {pokemon_id}] {pokemon_name}\n\tCard ID: {card_id}\n\tPokemon Type: {pokemon_type}\n\tIs EX: {is_ex}\n\tBase HP: {base_hp}\n\tStage: {stage}\n\tEvolution Name: {evolution_name}\n\Move 1: {move_1_name   }\n\tMove 2: {move_2_name}\n\tAbility: {ability_name}\n\tWeakness: {weakness}\n\tRetreat Cost: {retreat_cost}\n')
                return

            print(f'[POKEMON_ID # {pokemon_id}] {pokemon_name}\n\tCard ID: {card_id}\n\tPokemon Type: {pokemon_type}\n\tIs EX: {is_ex}\n\tBase HP: {base_hp}\n\tStage: {stage}\n\tEvolution Name: {evolution_name}\n\tMove 1 ID: {move_1_id}\n\tMove 2 ID: {move_2_id}\n\tAbility ID: {ability_id}\n\tWeakness: {weakness}\n\tRetreat Cost: {retreat_cost}\n')
    except Exception  as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
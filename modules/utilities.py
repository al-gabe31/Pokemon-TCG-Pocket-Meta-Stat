import sqlite3

DATABASE_PATH = 'databases/ptcgp.db'



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
            move_id, move_name, description, attack_type, base_damage, cost, effects = move

            print(f'[MOVE_ID # {move_id}] {move_name}\n\tDescription: {description}\n\tAttack Type: {attack_type}\n\tBase Damage: {base_damage}\n\tCost: {cost}\n\tEffects: {effects}\n')
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
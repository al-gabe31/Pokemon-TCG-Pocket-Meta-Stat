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
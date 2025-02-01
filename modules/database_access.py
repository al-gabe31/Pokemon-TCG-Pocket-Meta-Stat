from utilities import *



MOVE_DEFAULT_DESCRIPTION = ''
MOVE_DEFAULT_ATTACK_TYPE = ''
MOVE_DEFAULT_BASE_DAMAGE = -10
MOVE_DEFAULT_COST = '{}'
MOVE_DEFAULT_EFFECTS = '{"null": "null"}'

def get_move(move_name, description = MOVE_DEFAULT_DESCRIPTION, attack_type = MOVE_DEFAULT_ATTACK_TYPE, base_damage = MOVE_DEFAULT_BASE_DAMAGE, cost = MOVE_DEFAULT_COST, effects = MOVE_DEFAULT_EFFECTS, debug = False):
    # if move_name = '', then that means we expect it to return -1 (not looking for a particular move)
    if move_name == '':
        return -1
    
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        additional_where = ''

        # additing additional where clauses if parameters were provided
        if description != MOVE_DEFAULT_DESCRIPTION:
            additional_where += f'description = \'{description}\' and '
        if attack_type != MOVE_DEFAULT_ATTACK_TYPE:
            additional_where += f'attack_type = \'{attack_type}\' and '
        if base_damage != MOVE_DEFAULT_BASE_DAMAGE:
            additional_where += f'base_damage = {base_damage} and '
        if cost != MOVE_DEFAULT_COST:
            additional_where += f'cost = \'{cost}\' and '
        if effects != MOVE_DEFAULT_EFFECTS:
            additional_where == f'effects = \'{effects}\' and '

        query = f'''
            select *
            from move
            where {additional_where} move_name = '{move_name}'
        '''

        cursor.execute(query)
        result = cursor.fetchall()

        # no copies of the move found
        if len(result) == 0:
            print(f'No copies of the move \'{move_name}\' was found with the given parameters.')
        
        # multiple copies of the move found
        elif len(result) > 1:
            print(f'{len(result)} copies of the move \'{move_name}\' was found. Please be more specific.')

            if debug:
                move_list_copies(move_name)
        
        # found 1 copy of a move
        else:
            return result[0][0] # returning the move's id
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return -1 # move not found

def get_ability(ability_name, debug = False):
    # if ability_name = '', then that means we expect it to return -1 (not looking for a particular ability)
    if ability_name == '':
        return -1
    
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        query = f'''
            select *
            from ability
            where ability_name = '{ability_name}'
        '''

        cursor.execute(query)
        result = cursor.fetchall()

        # no copies of the ability found
        if len(result) == 0:
            print(f'No copies of the ability \'{ability_name}\' was found with the given parameters.')

        # multiple copies of the ability found
        elif len(result) > 1:
            print(f'{len(result)} copies of the ability \'{ability_name}\' was found. Please be more specific.')

            if debug:
                ability_list_copies(ability_name)

        # found 1 copy of the ability
        else:
            return result[0][0] # returning the ability's id
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return -1 # ability not found
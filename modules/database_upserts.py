import sqlite3

DATABASE_PATH = 'databases/ptcgp.db'



# PLAYER UPSERT
def player_upsert():
    conn = None
    cursor = None

    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('insert into player default values')

    conn.commit()
    conn.close()



# MOVE UPSERT
# PARAMETER DEFAULT VALUES
MOVE_DEFAULT_DESCRIPTION = '' # (okay if it's empty)
MOVE_DEFAULT_ATTACK_TYPE = ''
MOVE_DEFAULT_BASE_DAMAGE = -10
MOVE_DEFAULT_COST = '{}'
MOVE_DEFAULT_EFFECTS = '{"null": "null"}'

def move_upsert(move_name, description = MOVE_DEFAULT_DESCRIPTION, attack_type = MOVE_DEFAULT_ATTACK_TYPE, base_damage = MOVE_DEFAULT_BASE_DAMAGE, cost = MOVE_DEFAULT_COST, effects = MOVE_DEFAULT_EFFECTS, force_insert = False, force_unique = True):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        action_type = '' # we need to know whether we're going to be inserting or updating a record into the table
        cursor.execute(f'select count(*) from move where move_name = \"{move_name}\"')

        if cursor.fetchall()[0][0] > 0 and force_unique == True:
            action_type = 'upsert'
        else:
            action_type = 'insert'

        # action type is insert but not all parameters are populated (except description)
        if action_type == 'insert' and (attack_type == MOVE_DEFAULT_ATTACK_TYPE or base_damage == MOVE_DEFAULT_BASE_DAMAGE or cost == MOVE_DEFAULT_COST or effects == MOVE_DEFAULT_EFFECTS):
            print('All parameters need to be populated in order to insert into move.db')
            return # exits the function
        
        # action type is insert and all parameters are populated
        if action_type == 'insert' and not (attack_type == MOVE_DEFAULT_ATTACK_TYPE or base_damage == MOVE_DEFAULT_BASE_DAMAGE or cost == MOVE_DEFAULT_COST or effects == MOVE_DEFAULT_EFFECTS):
            cursor.execute(f'''
                insert into move (move_name, description, attack_type, base_damage, cost, effects)
                values (\'{move_name}\', \'{description}\', \'{attack_type}\', {base_damage}, \'{cost}\', \'{effects}\')
            ''')

        # action type is upsert and force insert is false
        if action_type == 'upsert' and force_insert == False:
            # first getting current values for each attribute
            cursor.execute(f'select * from move where move_name = \"{move_name}\"')
            result = cursor.fetchall()[0]
            curr_description = result[2]
            curr_attack_type = result[3]
            curr_base_damage = result[4]
            curr_cost = result[5]
            curr_effects = result[6]

            # only update the attributes we specified
            if description != MOVE_DEFAULT_DESCRIPTION:
                curr_description = description
            if attack_type != MOVE_DEFAULT_ATTACK_TYPE:
                curr_attack_type = attack_type
            if base_damage != MOVE_DEFAULT_BASE_DAMAGE:
                curr_base_damage = base_damage
            if cost != MOVE_DEFAULT_COST:
                curr_cost = cost
            if effects != MOVE_DEFAULT_EFFECTS:
                curr_effects = effects

            # ready to update row
            cursor.execute(f'''
                update move
                set
                    description = \'{curr_description}\',
                    attack_type = \'{curr_attack_type}\',
                    base_damage = {curr_base_damage},
                    cost = \'{curr_cost}\',
                    effects = \'{curr_effects}\'
                where move_name = \'{move_name}\'
            ''')

        # action type is upsert and force insert is true
        if action_type == 'upsert' and force_insert == True:
            print(f'Move {move_name} already in move.db')
            return # exits the function

        conn.commit()
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# ABILITY UPSERT
# PARAMETER DEFAULT VALUES
ABILITY_DEFAULT_DESCRIPTION = '' # (okay if it's empty)
ABILITY_DEFAULT_ACTIVABLE = -1
ABILITY_DEFAULT_ACTIVE_REQ = '{"null": "null"}'
ABILITY_DEFAULT_REPEATABLE = -1
ABILITY_DEFAULT_EFFECTS = '{"null": "null"}'

def ability_upsert(ability_name, description = ABILITY_DEFAULT_DESCRIPTION, activable = ABILITY_DEFAULT_ACTIVABLE, active_req = ABILITY_DEFAULT_ACTIVE_REQ, repeatable = ABILITY_DEFAULT_REPEATABLE, effects = ABILITY_DEFAULT_EFFECTS, force_insert = False, force_unique = True):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        action_type = '' # we need to know whether we're going to be inserting or updating a record into the table
        cursor.execute(f'select count(*) from ability where ability_name = \"{ability_name}\"')
        num_records = cursor.fetchall()[0][0]

        if num_records > 0:
            action_type = 'upsert'
        else:
            action_type = 'insert'

        # action type is insert but not all parameters are populated (except description)
        if action_type == 'insert' and (activable == ABILITY_DEFAULT_ACTIVABLE or active_req == ABILITY_DEFAULT_ACTIVE_REQ or repeatable == ABILITY_DEFAULT_REPEATABLE or effects == ABILITY_DEFAULT_EFFECTS):
            print ('All parameters need to be populated in order to insert into ability.db')
            return # exits the function

        # action type is insert and all parameters are populated
        if action_type == 'insert' and not (activable == ABILITY_DEFAULT_ACTIVABLE or active_req == ABILITY_DEFAULT_ACTIVE_REQ or repeatable == ABILITY_DEFAULT_REPEATABLE or effects == ABILITY_DEFAULT_EFFECTS):
            print('F1')
            cursor.execute(f'''
                insert into ability(ability_name, description, activable, active_req, repeatable, effects)
                values (\'{ability_name}\', \'{description}\', {activable}, \'{active_req}\', {repeatable}, \'{effects}\')
            ''')

        # action type is upsert and force insert is false
        if action_type == 'upsert' and force_insert == False:
            # first getting current values for each attribute
            cursor.execute(f'select * from ability where ability_name = \"{ability_name}\"')
            result = cursor.fetchall()[0]
            curr_description = result[2]
            curr_activable = result[3]
            curr_active_req = result[4]
            curr_repeatable = result[5]
            curr_effects = result[6]

            # only update the attributes we specified
            if description != ABILITY_DEFAULT_DESCRIPTION:
                curr_description = description
            if activable != ABILITY_DEFAULT_ACTIVABLE:
                curr_activable = activable
            if active_req != ABILITY_DEFAULT_ACTIVE_REQ:
                curr_active_req = active_req
            if repeatable != ABILITY_DEFAULT_REPEATABLE:
                curr_repeatable = repeatable
            if effects != ABILITY_DEFAULT_EFFECTS:
                curr_effects = effects

            # ready to update row
            cursor.execute(f'''
                update ability
                set
                    description = \'{curr_description}\',
                    activable = {curr_activable},
                    active_req = \'{curr_active_req}\',
                    repeatable = {curr_repeatable},
                    effects = \'{curr_effects}\'
            ''')

        # action type is upsert and force insert is true
        if action_type == 'upsert' and force_insert == True:
            print(f'Ability {ability_name} already in ability.db')
            return # exits the function

        conn.commit()
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# END OF FILE
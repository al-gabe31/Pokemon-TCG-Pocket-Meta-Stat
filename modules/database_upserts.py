from utilities import *



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
MOVE_DEFAULT_BASE_DAMAGE = -10
MOVE_DEFAULT_COST = '{}'
MOVE_DEFAULT_EFFECTS = '{"null": "null"}'

def move_upsert(
        move_name, 
        description = MOVE_DEFAULT_DESCRIPTION, 
        base_damage = MOVE_DEFAULT_BASE_DAMAGE, 
        cost = MOVE_DEFAULT_COST, 
        effects = MOVE_DEFAULT_EFFECTS, 
        force_insert = False, 
        force_unique = True, 
        debug = False
    ):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Enforcing cost integrity
        cost_dict = json.loads(cost)
        passed_cost_test = True

        for move_type in cost_dict:
            if move_type not in valid_types:
                passed_cost_test = False

        if passed_cost_test == False:
            raise ValueError('Invalid cost passed. Make sure all cost types are valid')

        action_type = '' # we need to know whether we're going to be inserting or updating a record into the table
        cursor.execute(f'select count(*) from move where move_name = \"{move_name}\"')
        num_counts = cursor.fetchall()[0][0]

        # deciding on action type (insert, upsert, or error case)
        if force_insert == True and force_unique == True and num_counts > 0:
            # trying to insert a unique but the move already exists
            print(f'Move {move_name} already exists in move table')

            if debug:
                move_list_copies(move_name)
            return # exits the function
        elif force_insert == False and force_unique == True and num_counts > 1:
            # trying to modify a move but there are multiple copies
            print(f'Move {move_name} has {num_counts} copies! Use move_modify function to edit a specific one instead.')
            return # exits the function
        elif force_insert == False and force_unique == True and num_counts == 1:
            # updating the only existing copy of a move
            action_type = 'upsert'
        elif base_damage == MOVE_DEFAULT_BASE_DAMAGE or cost == MOVE_DEFAULT_COST or effects == MOVE_DEFAULT_EFFECTS:
            # trying to insert but not all parameters are provided
            print('All parameters need to be populated in order to insert into move table')
            return # exits the function
        else:
            # inserting new move into the table
            action_type = 'insert'

        if action_type == 'insert':
            cursor.execute(f'''
                insert into move (move_name, description, base_damage, cost, effects)
                values (\'{move_name}\', \'{description}\', {base_damage}, \'{cost}\', \'{effects}\')
            ''')
        elif action_type == 'upsert':
            # first getting current values for each attribute
            cursor.execute(f'select * from move where move_name = \"{move_name}\"')
            result = cursor.fetchall()[0]
            curr_description = result[2]
            curr_base_damage = result[3]
            curr_cost = result[4]
            curr_effects = result[5]

            # only update the attributes we specified
            if description != MOVE_DEFAULT_DESCRIPTION:
                curr_description = description
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
                    base_damage = {curr_base_damage},
                    cost = \'{curr_cost}\',
                    effects = \'{curr_effects}\'
                where move_name = \'{move_name}\'
            ''')

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

def ability_upsert(
        ability_name, 
        description = ABILITY_DEFAULT_DESCRIPTION, 
        activable = ABILITY_DEFAULT_ACTIVABLE, 
        active_req = ABILITY_DEFAULT_ACTIVE_REQ, 
        repeatable = ABILITY_DEFAULT_REPEATABLE, 
        effects = ABILITY_DEFAULT_EFFECTS, 
        force_insert = False, 
        force_unique = True, 
        debug = False
    ):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        action_type = '' # we need to know whether we're going to be inserting or updating a record into the table
        cursor.execute(f'select count(*) from ability where ability_name = \"{ability_name}\"')
        num_counts = cursor.fetchall()[0][0]

        # deciding on action type (insert, upsert, or error case)
        if force_insert == True and force_unique == True and num_counts > 0:
            # trying to insert a unique but the ability already exists
            print(f'Ability {ability_name} already exists in ability table')

            if debug:
                ability_list_copies(ability_name)
            return # exits the function
        elif force_insert == False and force_unique == True and num_counts > 1:
            # trying to modify an ability but there are multiple copies
            print(f'Ability {ability_name} has {num_counts} copies! Use ability_modify function to edit a specific one instead.')
            return # exits the function
        elif force_insert == False and force_unique == True and num_counts == 1:
            # updating the only existing copy of an ability
            action_type = 'upsert'
        elif activable == ABILITY_DEFAULT_ACTIVABLE or active_req == ABILITY_DEFAULT_ACTIVE_REQ or repeatable == ABILITY_DEFAULT_REPEATABLE or effects == ABILITY_DEFAULT_EFFECTS:
            # trying to insert but not all parameters are provided
            print('All parameters need to be populated in order to insert into ability table')
            return # exits the function
        else:
            # inserting new ability into the table
            action_type = 'insert'

        if action_type == 'insert':
            cursor.execute(f'''
                insert into ability(ability_name, description, activable, active_req, repeatable, effects)
                values (\'{ability_name}\', \'{description}\', {activable}, \'{active_req}\', {repeatable}, \'{effects}\')
            ''')
        elif action_type == 'upsert':
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

        conn.commit()
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# POKEMON UPSERT
# PARAMETER DEFAULT VALUES
POKEMON_DEFAULT_TYPE = ''
POKEMON_DEFAULT_IS_EX = -1
POKEMON_DEFAULT_BASE_HP = -10
POKEMON_DEFAULT_STAGE = ''
POKEMON_DEFAULT_EVOLUTION_NAME = 'None'
POKEMON_DEFAULT_MOVE_1_ID = -1
POKEMON_DEFAULT_MOVE_2_ID = -1
POKEMON_DEFAULT_ABILITY_ID = -1
POKEMON_DEFAULT_WEAKNESS = ''
POKEMON_DEFAULT_RETREAT_COST = -1

def pokemon_upsert(
        pokemon_name, 
        pokemon_type = POKEMON_DEFAULT_TYPE, 
        is_ex = POKEMON_DEFAULT_IS_EX, 
        base_hp = POKEMON_DEFAULT_BASE_HP, 
        stage = POKEMON_DEFAULT_STAGE, 
        evolution_name = POKEMON_DEFAULT_EVOLUTION_NAME, 
        move_1_id = POKEMON_DEFAULT_MOVE_1_ID, 
        move_2_id = POKEMON_DEFAULT_MOVE_2_ID, 
        ability_id = POKEMON_DEFAULT_ABILITY_ID, 
        weakness = POKEMON_DEFAULT_WEAKNESS, 
        retreat_cost = POKEMON_DEFAULT_RETREAT_COST,
        force_insert = False,
        force_unique = True,
        debug = False,
        display_id_names = False
    ):
    conn = None
    cursor = None

    # Pokemon stage & evolution have to be consistent
    # ie. basic pokemon cannot have an evolution
    if stage == 'basic' and evolution_name != '':
        print(f'ERROR - Inserting basic pokemon with an evolution')
        return
    if stage != 'basic' and evolution_name == '':
        print(f'ERROR - Inserting non basic pokemon without an evolution')
        return

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        action_type = '' # we need to know whether we're going to be inserting or updating a record into the table
        cursor.execute(f'select count(*) from pokemon_card where pokemon_name = \"{pokemon_name}\"')
        num_counts = cursor.fetchall()[0][0]

        # deciding on action type (insert, upsert, error case)
        if force_insert == True and force_unique == True and num_counts > 0:
            # trying to insert a unique but the pokemon already exists
            print(f'Pokemon {pokemon_name} already exists in pokemon_card table')

            if debug:
                pokemon_card_list_copies(pokemon_name, display_id_names)
            return # exits the function
        elif force_insert == False and force_unique == True and num_counts > 1:
            # trying to modify a pokemon but there are multiple copies
            print(f'Pokemon {pokemon_name} has {num_counts} copies! Use pokemon_card_modify function to edit a specific one instead.')
            return # exits the function
        elif force_insert == False and force_unique == True and num_counts == 1:
            # updating the only existing copy of a pokemon
            action_type = 'upsert'
        elif pokemon_type == POKEMON_DEFAULT_TYPE or is_ex == POKEMON_DEFAULT_IS_EX or base_hp == POKEMON_DEFAULT_BASE_HP or stage == POKEMON_DEFAULT_STAGE or evolution_name == POKEMON_DEFAULT_EVOLUTION_NAME or weakness == POKEMON_DEFAULT_WEAKNESS or retreat_cost == POKEMON_DEFAULT_RETREAT_COST:
            # trying to insert but not all parameters are provided
            print('All parameters need to be populated in order to insert into pokemon_card table')
            return # exits the function
        else:
            # inserting a new pokemon_card into the table
            action_type = 'insert'

        # verifying that evolution_name is in pokemon_card table
        cursor.execute(f'select count(*) from pokemon_card where pokemon_name = \"{evolution_name}\"')
        evolution_matches = cursor.fetchall()[0][0]

        # error only if there were no evolution matches & evolution parameter was provided (ie not equal to default evolution)
        if evolution_matches == 0 and evolution_name != POKEMON_DEFAULT_EVOLUTION_NAME and evolution_name != '':
            print(f'Evolution pokemon {evolution_name} not found')
            return # exits the function

        if action_type == 'insert':
            # we have to insert into card & pokemon_card table
            # inserting into card table
            cursor.execute(f'''
                insert into card(card_name, card_archetype)
                values(\'{pokemon_name}\', 'pokemon')
            ''')

            card_id = cursor.lastrowid

            # verifying that card_id is not None
            if card_id is None:
                raise ValueError('card_id is None')

            # inserting into pokemon_card table
            additional_insert = ''
            additional_values = ''

            # reminder that move_1, move_2, & ability can be null (parameter will be passed as -1)
            # for any that aren't null, include it in the insert statement
            if move_1_id != POKEMON_DEFAULT_MOVE_1_ID:
                additional_insert += ', move_1_id'
                additional_values += f', {move_1_id}'
            if move_2_id != POKEMON_DEFAULT_MOVE_1_ID:
                additional_insert += ', move_2_id'
                additional_values += f', {move_2_id}'
            if ability_id != POKEMON_DEFAULT_ABILITY_ID:
                additional_insert += ', ability_id'
                additional_values += f', {ability_id}'

            cursor.execute(f'''
                insert into pokemon_card(card_id, pokemon_name, pokemon_type, is_ex, base_hp, stage, evolution_name, weakness, retreat_cost{additional_insert})
                values({card_id}, '{pokemon_name}', '{pokemon_type}', {is_ex}, {base_hp}, '{stage}', '{evolution_name}', '{weakness}', {retreat_cost}{additional_values})
            ''')
        elif action_type == 'upsert':
            # first getting current values for each attribute
            cursor.execute(f'select * from pokemon_card where pokemon_name = \"{pokemon_name}\"')
            result = cursor.fetchall()[0]
            curr_pokemon_type = result[3]
            curr_is_ex = result[4]
            curr_base_hp = result[5]
            curr_stage = result[6]
            curr_evolution_name = result[7]
            curr_move_1_id = result[8]
            curr_move_2_id = result[9]
            curr_ability_id = result[10]
            curr_weakness = result[11]
            curr_retreat_cost = result[12]

            # only update the attributes we specified
            if pokemon_type != POKEMON_DEFAULT_TYPE:
                curr_pokemon_type = pokemon_type
            if is_ex != POKEMON_DEFAULT_IS_EX:
                curr_is_ex = is_ex
            if base_hp != POKEMON_DEFAULT_BASE_HP:
                curr_base_hp = base_hp
            if stage != POKEMON_DEFAULT_STAGE:
                curr_stage = stage
            if evolution_name != POKEMON_DEFAULT_EVOLUTION_NAME:
                curr_evolution_name = evolution_name
            if move_1_id != POKEMON_DEFAULT_MOVE_1_ID:
                curr_move_1_id = move_1_id
            if move_2_id != POKEMON_DEFAULT_MOVE_2_ID:
                curr_move_2_id = move_2_id
            if ability_id != POKEMON_DEFAULT_ABILITY_ID:
                curr_ability_id = ability_id
            if weakness != POKEMON_DEFAULT_WEAKNESS:
                curr_weakness = weakness
            if retreat_cost != POKEMON_DEFAULT_RETREAT_COST:
                curr_retreat_cost = retreat_cost

            # performing data validation
            # making sure the new values make sense
            # 1. evolution name has to already exist in the pokemon_card table
            cursor.execute(f'select count(*) from pokemon_card where pokemon_name = \"{evolution_name}\"')
            num_found = cursor.fetchall()[0][0]

            if num_found <= 0: # evolution name not found
                raise ValueError(f'{pokemon_name} can\'t evolution from {evolution_name} because that pokemon doesn\'t exist.')
            
            # ready to update row
            # hoping that the table constraints perform data validation on the rest

            # we have to be mindful that move/ability id can either be an integer or None
            # only include move/ability in the query so long as an update is requested
            additional_id_statement = ''
            if move_1_id is not None and move_1_id != -1:
                additional_id_statement += f', move_1_id = {curr_move_1_id}'
            if move_2_id is not None and move_2_id != -1:
                additional_id_statement += f', move_2_id = {curr_move_2_id}'
            if ability_id is not None and ability_id != -1:
                additional_id_statement += f', ability_id = {curr_ability_id}'

            cursor.execute(f'''
                update pokemon_card
                set
                    pokemon_type = \'{curr_pokemon_type}\',
                    is_ex = {curr_is_ex},
                    base_hp = {curr_base_hp},
                    stage = \'{curr_stage}\',
                    evolution_name = \'{curr_evolution_name}\',
                    weakness = \'{curr_weakness}\',
                    retreat_cost = {curr_retreat_cost}
                    {additional_id_statement}
                where pokemon_name = \'{pokemon_name}\'
            ''')

        conn.commit() # committing transaction
    except Exception as e:
        print(f'SQL ERROR - {e}')
        conn.rollback() # rolling back transaction
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# END OF FILE
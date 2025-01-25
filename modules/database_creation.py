# setup
import sqlite3

DATABASE_PATH = 'databases/ptcgp.db'

# boilerplate code to create the database
def create_db(db_name, query):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        conn.commit()
        print(f'Database {db_name}.db created!')
    except sqlite3.Error as e:
        print(f'ERROR - {e}')


    conn.close()



'''
EXAMPLE USE

# creating the player database
db_name = 'player'
query = \'\'\'
    create table if not exists player (
        player_id   integer primary key autoincrement,
        num_win     integer not null default 0,
        num_lose    integer not null default 0,
        num_draw    integer not null default 0
    )
\'\'\'
create_db(db_name, query)
'''
import sqlite3

def get_move(move_name, column_index = -1):
    conn = None
    cursor = None

    try:
        conn = sqlite3.connect('databases/ptcgp.db')
        cursor = conn.cursor()

        # fetching the move in the database
        cursor.execute(f'select * from move where move_name = \"{move_name}\" collate nocase')
        return cursor.fetchall()[0]
    except Exception as e:
        print(f'SQL ERROR - {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
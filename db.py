import sqlite3


def db_init() -> None:
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS cashed(
                common_name TEXT PRIMARY KEY,
                scientific_name TEXT,
                dna_sequence TEXT
                );
    ''')

    conn.commit()
    conn.close()


def db_insert(data) -> None:
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''INSERT OR REPLACE INTO cashed (common_name, scientific_name, dna_sequence) 
                     VALUES (:common_name, :scientific_name, :dna_sequence);''', data)

    conn.commit()
    conn.close()


def db_find(common) -> str:
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''SELECT scientific_name FROM cashed WHERE common_name = ?;''', (common,))

    result = c.fetchone()
    conn.close()

    return result

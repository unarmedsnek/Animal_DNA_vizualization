""""
This module provides functions to interact with a SQLite database for caching animal data.

Functions:
- db_init() -> None: Initializes the database and creates the necessary table if it does not exist.
- db_insert(data) -> None: Inserts or replaces animal data into the database.
- db_find(common) -> dict[str: str] | None: Retrieves animal data from the database based on the common name.
"""

import sqlite3


def db_init() -> None:
    """ Initializes the SQLite database and creates the 'cashed' table if it does not already exist."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
            CREATE TABLE IF NOT EXISTS cashed(
                common_name TEXT PRIMARY KEY,
                scientific_name TEXT,
                accession TEXT,
                dna_sequence TEXT
                );
    ''')

    conn.commit()
    conn.close()


def db_insert(data) -> None:
    """
    Inserts or replaces animal data into the 'cashed' table in the SQLite database.

    :param:
        data (dict): A dictionary containing the common name, scientific name, accession number, and DNA sequenco of an animal.
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''INSERT OR REPLACE INTO cashed (common_name, scientific_name, accession, dna_sequence) 
                     VALUES (:common_name, :scientific_name, :accession, :dna_sequence);''', data)

    conn.commit()
    conn.close()


def db_find(common) -> dict[str: str] | None:
    """
    Retrieves animal data from the 'cashed' table in the SQLite database based on the common name.
    :param:
    - common: The common name of the animal to search for in the database.

    :return:
    - A dictionary containing the scientific name and DNA sequence of the animal if found, or None if not found in the database.
    """
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''SELECT scientific_name, dna_sequence FROM cashed WHERE common_name = ?;''', (common,))

    result = c.fetchone()
    conn.close()

    return dict(result) if result else None

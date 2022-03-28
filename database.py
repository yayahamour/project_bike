import sqlite3

DB = sqlite3.connect('projet_bike')


def create_table():
    #creation d'une table vide 
    cursor = DB.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT,
        age INTERGER
        )
        """)
    DB.commit()

    #insertion des données
     
     
db.close()
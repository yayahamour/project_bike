import pandas as pd
import sqlite3

DB = sqlite3.connect('projet_bike.db')

def create_table(name):
    cursor = DB.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS """ + name +"""(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        datetime TIMESERIES,
        season INTERGER,
        holiday INTEGER,
        workingday INTEGER,
        weather INTEGER,
        temp FLOAT,
        atemp FLOAT,
        humidity INTEGER,
        windspeed FLOAT,
        casual INTEGER,
        registered INTEGER,
        count INTEGER
        );""")
    DB.commit()

def add_table(name, datetime,season,holiday,workingday,weather,temp,atemp,humidity,windspeed,casual,registered,count):
    cursor = DB.cursor()
    data = "INSERT INTO "+name+" (datetime,season,holiday,workingday,weather,temp,atemp,humidity,windspeed,casual,registered,count) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
    value = (datetime,season,holiday,workingday,weather,temp,atemp,humidity,windspeed,casual,registered,count)
    cursor.execute (data, value)
    DB.commit()
    cursor.close()

def del_row(name,id):
    cursor = DB.cursor()
    data = "DELETE FROM " + name + " WHERE id = "+ id + ""
    cursor.execute(data)
    DB.commit()
    cursor.close()
    DB.close()
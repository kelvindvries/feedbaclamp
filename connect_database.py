import psycopg2
import random
import time
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection configuration
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables():
    """ Create tables in the PostgreSQL database """

    commands = (
        """
        CREATE TABLE feedbacklamp (
            teHard_id SERIAL PRIMARY KEY,
            lamp_decibel INTEGER,
            datum_teHard DATE,
            tijd_teHard TIME
        );
        """)

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        # for command in commands:
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_feedbacklamp(lamp_decibel, datum_teHard, tijd_teHard):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO feedbacklamp(lamp_decibel, datum_teHard, tijd_teHard)
             VALUES(%s, %s, %s) RETURNING teHard_id;"""
    conn = None
    teHard_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (lamp_decibel, datum_teHard, tijd_teHard, ))
        # get the generated id back
        teHard_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return teHard_id


def get_date():
    d = time.strftime("%x")
    return d


def get_time():
    t = time.strftime("%X")
    return t


def get_decibel_value():
    db_value = random.randint(10, 70)

    return db_value


# This Executes the program in order of functions
if __name__ == '__main__':

    limit = 50

    decibel = get_decibel_value()
    datum = get_date()
    tijd = get_time()

    if decibel > limit:
        print(decibel, datum, tijd)
        insert_feedbacklamp(decibel, datum, tijd)
    else:
        print('Te zacht')



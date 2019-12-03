import sqlite3
from sqlite3 import Error
import sys
import os
import traceback

class SimpleDB:
    conn = None
    def __init__(cls):
        cls.conn = None

    @classmethod
    def create(cls, sql, data):
        try:
            cur = cls.conn.cursor()
            print("create record: ", sql, data)
            cur.execute(sql, data)
            cls.conn.commit()
            return cur.lastrowid
        except Error as sql_err:
            print(sql_err)
            return -2
        except Exception as e:
            print(e)
            return -1
    @classmethod
    def update(cls, sql, data):
        try:
            cur = cls.conn.cursor()
            cur.execute(sql, data)
            cls.conn.commit()
        except Error as sql_err:
            print(sql_err)
        except Exception as e:
            print(e) 

    @classmethod
    def query(cls, sql, cond):
        try:
            cur = cls.conn.cursor()
            cur.execute(sql, cond)
            rows = cur.fetchall()
            return rows
        except Error as sql_err:
            print(sql_err)
            return []
        except Exception as e:
            print(e)
            return []

    @classmethod
    def query_all(cls, sql):
        try:
            cur = cls.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except Error as sql_err:
            print(sql_err)
            return []
        except Exception as e:
            print(e)
            return []

    @classmethod
    def delete(cls, sql):
        try:
            cur = cls.conn.cursor()
            cur.execute(sql)
            cls.conn.commit()
        except Error as sql_err:
            print(sql_err)
        except Exception as e:
            print(e) 

    @classmethod
    def initialize(cls):
        def create_table(conn, sql):
            c = conn.cursor()
            c.execute(sql)
        try:
            print("Create Database tables!!!")
            create_person_table = """ 
                CREATE TABLE IF NOT EXISTS person (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name vchar(32) NOT NULL,
                    sex char(8) NOT NULL,
                    id_card char(18) NOT NULL,
                    update_time TIMESTAMP NOT NULL,
                    create_time TIMESTAMP NOT NULL
            )
            """
            create_doc_table = """
                CREATE TABLE IF NOT EXISTS doc (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name vchar(32) NOT NULL,
                    person_id bigint NOT NULL
                )
            """
            create_file_table = """
                CREATE TABLE IF NOT EXISTS file (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name vchar(32) NOT NULL,
                    path vchar(256) NOT NULL,
                    doc_id bigint NOT NULL
                )
            """
            creation = [create_person_table, create_doc_table, create_file_table]
            for c in creation:
                print("Create table :\n", c)
                create_table(cls.conn, c)
            print("Success!!!")
        except Error as sql_err:
            print(sql_err)
        except Exception as e:
            print(e)

    @classmethod
    def open(cls, db_file):
        try:
            db_file = os.path.abspath(db_file)
            first_launch = False
            if not os.path.exists(db_file):
                if not os.path.exists(os.path.dirname(db_file)):
                    os.makedirs(os.path.dirname(db_file))
                first_launch = True
            cls.conn = sqlite3.connect(db_file)
            if first_launch:
                cls.initialize()

        except Error as sql_err:
            print(sql_err)    
        except Exception as e:
            print("Failed to open database with {}: {}".format(db_file, e))
        
    @classmethod
    def close(cls):
        try:
            pass
        finally:
            if cls.conn:
                cls.conn.close()

import time
import datetime
from datetime import datetime as dt
from model import Person
from model import Document
from model import File

class PersionServiceImpl:
    db = None

    @classmethod
    def __init__(cls, db):
        cls.db = db

    @classmethod
    def get_by_id(cls, id):
        pass
    
    @classmethod
    def get_by_name(cls, name):
        sql = """select * from person where name=?"""
        data = (name, )
        rows = cls.db.query(sql, data)
        records = []
        for row in rows:
            records.append(Person(row[0], row[1], row[2], row[3], dt.fromtimestamp(row[4]), dt.fromtimestamp(row[5])))
        return records

    @classmethod
    def add(cls, person):
        sql = """insert into person(id, name, sex, id_card, update_time, create_time)
                 values(NULL,?,?,?,?,?)"""
        now = dt.timestamp(dt.now())
        data = (person.name, person.sex, person.id_card, now, now)
        person_id = cls.db.create(sql, data)
        return person_id

    @classmethod
    def get_all_by_page(cls, page, size):
        # records = [
        #     Person(0, "TEST1","男","000000000000000000", dt.now(), dt.now()),
        #     Person(1, "TEST2","女","000000000000000001", dt.now(), dt.now()),
        #     Person(2, "TEST3","男","000000000000000002", dt.now(), dt.now())
        # ]
        sql = "select * from person LIMIT {} OFFSET {}".format(size, (page - 1) * size)
        rows = cls.db.query_all(sql)
        records = []
        for row in rows:
            print(row)
            records.append(Person(row[0], row[1], row[2], row[3], dt.fromtimestamp(row[4]), dt.fromtimestamp(row[5])))
        return records

class DocFileServiceImpl:
    db = None
    @classmethod
    def __init__(cls, db):
        cls.db = db 

    @classmethod
    def get_by_id(cls, id):
        pass

    @classmethod
    def get_doc_by_pid(cls, pid):
        sql = """select * from doc where person_id=?"""
        data = (pid, )
        rows = cls.db.query(sql, data)
        records = []
        for row in rows:
            print(row)
            records.append(Document(row[0], row[1], row[2], cls.get_by_doc_id(row[0])))
        return records

    @classmethod
    def add_doc(cls, doc):
        sql = """insert into doc(id, name, person_id) values(NULL,?,?)"""
        data = (doc.name, doc.person_id)
        doc_id = cls.db.create(sql, data)
        return doc_id

    @classmethod
    def add_file(cls, file):
        sql = """insert into file(id, name, path, doc_id) values(NULL,?,?,?)"""
        data = (file.name, file.path, file.doc_id)
        file_id= cls.db.create(sql, data)
        return file_id 

    @classmethod
    def get_by_doc_id(cls, did):
        sql = """select * from file where doc_id=?"""
        data = (did, )
        rows = cls.db.query(sql, data)
        records = []
        for row in rows:
            print(row)
            records.append(File(row[0], row[1], row[2], row[3]))
        return records
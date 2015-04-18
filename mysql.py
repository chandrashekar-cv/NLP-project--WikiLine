#!/usr/bin/python
import MySQLdb as mdb

class MySqlWrapper:
    def __init__(self):
        self.conn = mdb.connect('localhost', 'csci544', 'csci544', 'wikidb')

    def get_cursor(self):
        return self.conn.cursor()

    def create_tables(self):
        cursor = self.get_cursor()
        cursor.execute('''create table document 
                     (doc_id VARCHAR(20) NOT NULL, title VARCHAR(100), PRIMARY KEY (doc_id));''')

        self.conn.commit()

        cursor.execute('''create table event
                        (event_id VARCHAR(20) NOT NULL, doc_id VARCHAR(20) NOT NULL, event_description TEXT, PRIMARY KEY(event_id));''')

        self.conn.commit()

        cursor.execute('''create table event_time
                            (event_id VARCHAR(20), time YEAR, PRIMARY KEY(event_id, time));''')

        cursor.execute('''create table event_entity
                            (event_id VARCHAR(20) NOT NULL, entity VARCHAR(100) NOT NULL, PRIMARY KEY(event_id, entity));''')

        cursor.execute('''create table document_category
                            (doc_id varchar(20) not null, category varchar(100) not null, primary key (doc_id, category));''')

        self.conn.commit()
        cursor.close()

    def drop_tables(self):
        cursor = self.get_cursor()
        try:
            cursor.execute('''drop table event_time''')
            cursor.execute('''drop table event_entity''')
            cursor.execute('''drop table event''')
            cursor.execute('''drop table document''')
            self.conn.commit()
        except mdb.Error, e:
            return False
        finally:
            cursor.close()
            return True

    def execute_query(self, query):
        cursor = self.get_cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
        except mdb.Error, e:
            #print e
            return False
        finally:
            cursor.close()

    def insert_into_table(self, query):
        cursor = self.get_cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
        except mdb.Error, e:
            return False
        finally:
            cursor.close()

if __name__ == "__main__":
    m = MySqlWrapper()
    #m.drop_tables()
    m.create_tables()
    #m.drop_tables()

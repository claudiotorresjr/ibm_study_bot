import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor

class Database:
    def __init__(self):
        self.conn = None
    
    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    database="d398cfen0k69uv", 
                    user="doatjlhomhhmpe", 
                    password="b5f5c59ac8e23a962aa56926d16fe845e36beb5cd57a7baf1f2a6c0c6fca46a5", 
                    host="ec2-44-197-128-108.compute-1.amazonaws.com", 
                    port="5432"
                )
                # self.conn = psycopg2.connect(
                #     database="musicbot_test", 
                #     user="postgres", 
                #     password="123", 
                #     host="127.0.0.1", 
                #     port="5432"
                # )
            except psycopg2.DatabaseError as e:
                raise e

    def create_table(self):
        self.connect()
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            #cur.execute("DROP TABLE IF EXISTS PROFS" )
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS PROFS
                (KEY       SERIAL PRIMARY KEY     NOT NULL,
                NAME             TEXT             NOT NULL,
                EMAIL            TEXT             NOT NULL,
                STARS            INT              NOT NULL,
                VOTES            INT              NOT NULL,
                COMMENTS         JSONB               );''')

            self.conn.commit()

    def select_rows_dict_cursor(self, query, fetchall):
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)

            if fetchall:
                records = cur.fetchall()
            else:
                records = cur.fetchone()
        cur.close()
        return records
    
    def commit_query(self, query):
        self.connect()   
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()

def start_database():
    database = Database()
    database.connect()
    database.create_table()

    return database
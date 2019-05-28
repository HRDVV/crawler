"""
 Created by hanruida on 2019-03-26
"""
import pymysql


class Db:

    def __init__(self, host="127.0.0.1", user="root", password="12345678", database="spider"):
        self.host = host
        self.username = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database,
            charset="utf8"
        )
        self.cursor = self.conn.cursor()
        return self

    def operator(self, sql, multiple):
        self.cursor.execute(sql)
        self.conn.commit()
        if multiple:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            print(exc_type)
            print(exc_val)
            print(exc_tb)
            self.conn.rollback()
            self.conn.close()






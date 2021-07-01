#!/usr/bin/env python3
# coding: utf-8

import MySQLdb

class MySQL:
    def __init__(self, localhost):
        self.conn = MySQLdb.connect(
            user = 'YOUR_USER_NAME',
            passwd = 'YOUR_PASSWORD',
            host = localhost,
            db = 'mysql',
            charset = "utf8"
        )

    def __enter__(self):
        return self

    def call(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return (cur.fetchall())

    def commit(self) :
        self.conn.commit()

    def __exit__(self, exception_type, exceptrion_value, traceback):
        self.conn.close()
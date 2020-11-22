# 01 MySQLdb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import peewee
import pymysql
import MySQLdb
db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='password',
    db='world'
)
cursor = db.cursor()
cursor.execute("SELECT * FROM city")
for row in cursor.fetchall():
    print(row)
db.close()


# 02 pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='password',
    db='world'
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM city")
for row in cursor.fetchall():
    print(row)
cursor.close()
conn.close()


# 03 peewee
db = peewee.MySQLDatabase(
    'friends',
    user='root',
    passwd='password'
)


class Infomation(peewee.Model):
    name = peewee.CharField()
    age = peewee.IntegerField()

    class Meta:
        database = db


Infomation.create_table()
fujiawei = Infomation(name='fujiawei', age=20)
fujiawei.save()

for friend in Infomation.filter(name='fujiawei'):
    print(friend.age)


# 04 SQLAlchemy

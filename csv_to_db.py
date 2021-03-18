import sqlite3
import csv
import os

conn = sqlite3.connect('db.sqlite3')

cur = conn.cursor()

reader = csv.reader(open('data/api_title.csv', encoding='utf-8'))
next(reader)
for row in reader:
    # to_db = [int(row[0]), str(row[1]), int(row[2]), int(row[3])]
    cur.execute("INSERT INTO api_title VALUES (?, ?, ?, ?);", row)
conn.commit()
print(os.listdir('data'))

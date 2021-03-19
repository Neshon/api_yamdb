import sqlite3
import csv
import os
# import pandas as pd


conn = sqlite3.connect('db.sqlite3')

cur = conn.cursor()
files = os.listdir('data')

for file in files:
    if "api" in file:
        name_file = file.split('.')[0]
        reader = csv.reader(open(f'data/{name_file}.csv', encoding='utf-8'))
        first_col = next(reader)
        marks = len(first_col) * '?, '
        col_names = tuple(first_col)
        sql = f"INSERT INTO {name_file} {col_names} VALUES ({marks[0:-2]});"
        for row in reader:
            cur.execute(f"{sql}", row)
conn.commit()
conn.close()

# for file in files:
#     if "api" in file:
#         name_file = file.split('.')[0]
#         reader = pd.read_csv(open(f'data/{name_file}.csv', encoding='utf-8'))
#         reader.to_sql(f'{name_file}', conn, if_exists='append', index=False)
# conn.close()

import json
import sqlite3

# Creating cursor for db
conn = sqlite3.connect('limaHuruf-v2.db')
cur = conn.cursor()

# Creating db
cur.execute('''
CREATE TABLE IF NOT EXISTS kata (
    limaHuruf VARCHAR(10) UNIQUE
);
''')

# Loads .json and storing to db
f = open('kbbi-entries.json')
data = json.load(f)

# Split method for extracting
for i in data['entries']:
    word = i.split('/')[-1]
    if len(word) == 5:
        cur.execute(''' INSERT OR IGNORE INTO kata (limaHuruf) VALUES (?)''', (word, ))
conn.commit()

f.close()
cur.close()
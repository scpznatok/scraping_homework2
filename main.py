import requests
from bs4 import BeautifulSoup
import json
import sqlite3



url = 'https://commits.facepunch.com/r/rust_reboot'
response = requests.get(url) 
soup = BeautifulSoup(response.text,"lxml")
commits = soup.find_all('div', class_='commits-message')
authors = soup.find_all('div', class_='author')
some_data = dict()
for i in range(len(commits)):
    print(authors[i].text.strip())
    print(commits[i].text)
    keys_aut = str(authors[i].text.strip()) + str(i)
    some_data[keys_aut] = commits[i].text.strip()
    print("_____________________")
    
print(some_data)

with open("result.json", "w", encoding="utf-8") as file:

    json.dump(some_data, file)

createSQL = """CREATE TABLE IF NOT EXISTS rust_updates (author TEXT, commits TEXT)"""
conn =sqlite3.connect("rust_updates.db")
cursor = conn.cursor()
cursor.execute(createSQL)
SQL = """INSERT INTO rust_updates (author, commits) VALUES (?,?)"""

for i in range(len(commits)):
    author = authors[i].text.strip()
    commit = commits[i].text.strip()
    cursor.execute(SQL, (author, commit))
    conn.commit()
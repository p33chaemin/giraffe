import sqlite3

conn = sqlite3.connect('users.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')
conn.execute("INSERT INTO users (username, password) VALUES ('admin', '1234')")
conn.execute("INSERT INTO users (username, password) VALUES ('chaemin', '0517')")
conn.execute("INSERT INTO users (username, password) VALUES ('kieun', '0910')")
conn.commit()
conn.close()
print("데이터베이스 초기화 완료!")

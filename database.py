import sqlite3
conn = sqlite3.connect('anonimus.db')
cur = conn.cursor()
cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        name TEXT)
            ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS polls (
    poll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id))  
    ''')
conn.commit()
conn.close()

def create_acc(tg_id, name):
    conn = sqlite3.connect('anonimus.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (tg_id, name) VALUES (?, ?)', (tg_id, name))
    conn.commit()
    conn.close()
    
def check_reg(tg_id):
    conn = sqlite3.connect('anonimus.db')
    cur = conn.cursor()
    tg_id = int(tg_id)
    cur.execute('SELECT * FROM users WHERE tg_id=?', (tg_id,))
    info = cur.fetchall()
    conn.close()
    return info

def get_user_info(tg_id):
    conn = sqlite3.connect('anonimus.db')
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE tg_id=?', (tg_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def create_poll(question, answer, user_id):
    conn = sqlite3.connect('anonimus.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO polls (question, answer, user_id) VALUES (?, ?, ?)', (question, answer, user_id))
    conn.commit()
    conn.close()
    
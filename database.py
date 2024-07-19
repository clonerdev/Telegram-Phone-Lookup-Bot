import sqlite3

def init_db():
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (user TEXT, user_id INTEGER, number TEXT, result TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user TEXT, user_id INTEGER, phone_number TEXT, restricted INTEGER DEFAULT 0, PRIMARY KEY (user, user_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (user TEXT, user_id INTEGER, PRIMARY KEY (user, user_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS authorized_users
                 (user TEXT, phone_number TEXT, PRIMARY KEY (user, phone_number))''')
    conn.commit()
    conn.close()

def save_search(user, user_id, number, result):
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (user, user_id, number, result) VALUES (?, ?, ?, ?)', (user, user_id, number, result))
    conn.commit()
    conn.close()

def save_user(user, user_id, phone_number):
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (user, user_id, phone_number) VALUES (?, ?, ?)', (user, user_id, phone_number))
    conn.commit()
    conn.close()

def restrict_user(user, user_id):
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('UPDATE users SET restricted=1 WHERE user=? AND user_id=?', (user, user_id))
    conn.commit()
    conn.close()

def unrestrict_user(user, user_id):
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('UPDATE users SET restricted=0 WHERE user=? AND user_id=?', (user, user_id))
    conn.commit()
    conn.close()

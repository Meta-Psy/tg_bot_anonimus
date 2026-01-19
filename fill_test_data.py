import sqlite3

conn = sqlite3.connect('anonimus.db')
cur = conn.cursor()

# Создаём таблицы если не существуют
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

cur.execute('''
    CREATE TABLE IF NOT EXISTS matching (
        user1_id INTEGER,
        user2_id INTEGER
    )
''')

# Очистим таблицы и сбросим автоинкремент
cur.execute('DELETE FROM polls')
cur.execute('DELETE FROM matching')
cur.execute('DELETE FROM users')
cur.execute("DELETE FROM sqlite_sequence WHERE name='users'")
cur.execute("DELETE FROM sqlite_sequence WHERE name='polls'")

# Тестовые пользователи
users = [
    (111111111, 'Алексей'),
    (222222222, 'Мария'),
    (333333333, 'Дмитрий'),
    (444444444, 'Анна'),
    (555555555, 'Иван')
]

cur.executemany('INSERT INTO users (tg_id, name) VALUES (?, ?)', users)

# Получим user_id
cur.execute('SELECT user_id, tg_id, name FROM users')
all_users = cur.fetchall()
print('Пользователи:')
for u in all_users:
    print(f'  user_id={u[0]}, tg_id={u[1]}, name={u[2]}')

# Тестовые опросы
polls = [
    ('Какой твой любимый цвет?', 'Синий', 1),
    ('Любимое время года?', 'Лето', 1),
    ('Какую музыку слушаешь?', 'Рок', 2),
    ('Любимая еда?', 'Пицца', 3),
    ('Хобби?', 'Программирование', 4)
]

cur.executemany('INSERT INTO polls (question, answer, user_id) VALUES (?, ?, ?)', polls)

# Связи друзей
matching = [
    (1, 2),  # Алексей -> Мария
    (1, 3),  # Алексей -> Дмитрий
    (2, 1),  # Мария -> Алексей
    (2, 4),  # Мария -> Анна
    (3, 5),  # Дмитрий -> Иван
]

cur.executemany('INSERT INTO matching (user1_id, user2_id) VALUES (?, ?)', matching)

conn.commit()

print('\nОпросы:')
cur.execute('SELECT * FROM polls')
for p in cur.fetchall():
    print(f'  poll_id={p[0]}, question="{p[1]}", answer="{p[2]}", user_id={p[3]}')

print('\nСвязи друзей:')
cur.execute('SELECT * FROM matching')
for m in cur.fetchall():
    print(f'  user1_id={m[0]} -> user2_id={m[1]}')

conn.close()
print('\nГотово!')

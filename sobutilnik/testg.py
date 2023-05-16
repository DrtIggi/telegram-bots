import sqlite3
conn = sqlite3.connect("timebase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''CREATE
TABLE
main
(username
text, time
text)'''
)
cursor.execute("INSERT into main values ('dirtyiggi','15:02')")
conn.commit()
conn.close()
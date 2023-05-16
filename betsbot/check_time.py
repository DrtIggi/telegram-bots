import sqlite3,time,os
from datetime import datetime
while True:
    try:
        conn = sqlite3.connect("timebase.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        cursor.execute("SELECT time,username FROM main")
        v = cursor.fetchall()
        r = datetime.strftime(datetime.now(), "%H:%M")


        for x in v:

            if x[0] == r:
                conn2 = sqlite3.connect("debtorbase.db")  # или :memory: чтобы сохранить в RAM
                cursor2 = conn2.cursor()
                cursor2.execute("insert into main values ('"+x[1]+"') ")
                conn2.commit()
                conn2.close()
                cursor.execute("UPDATE main SET time= '22:71' WHERE username='"+str(x[1])+"'")
                conn.commit()
        conn.close()
        time.sleep(20)
    except Exception as f:
        os.system("echo " + str(f) + " >> exception")

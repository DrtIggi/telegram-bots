import sqlite3
import xlrd, xlwt
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()
result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()

array = []
if len(result) == 0:
    print("Нет опросов")
for x in range(len(result)):
    if result[x][1][0:5] == 'users':
        array.append(result[x][1])
    else:
        continue
wb = xlwt.Workbook()
for x in array:
    ws = wb.add_sheet(f'{x[5:]}')
    result = cursor.execute(f"SELECT * FROM '{x}'").fetchall()
    for y in range(len(result)):
        ws.write(y, 0, result[y][0])
        ws.write(y, 1, result[y][1])
    wb.save('table.xls')

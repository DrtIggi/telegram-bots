from datetime import datetime
r=datetime.strftime(datetime.now(), "%Y.%m %H:%M")
r=r.split(" ")
if r[1][3:]=="46":
    print("k")
print(r[1][3:])
print(r)
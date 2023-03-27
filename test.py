import sqlite3

conn = sqlite3.connect('./db.sqlite')
c = conn.cursor()

c.execute("SELECT custemail, custphone FROm customers")
rs = c.fetchall()

email = 'riteshkpandey28@gmail.com'
phone = '9082407433'

for i in rs:
    if (email == i[0]) and (phone == i[1]):
        print('YES')
else:
    print('NO')
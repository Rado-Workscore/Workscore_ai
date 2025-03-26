import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Տպենք բոլոր աղյուսակները
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Աղյուսակները տվյալ բազայում՝")
for table in tables:
    print("-", table[0])

# Եթե կա 'employees', տպենք դրա սյունակները
print("\n'Employees' աղյուսակի սյունակները՝")
cursor.execute("PRAGMA table_info(employees);")
columns = cursor.fetchall()
for col in columns:
    print("-", col[1])  # col[1] = սյունակի անունը

conn.close()

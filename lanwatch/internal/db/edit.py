import sqlite3

def db_exec(sql_statement):
    # Assuming a connection to the database is established
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute(sql_statement)
    conn.commit()
    conn.close()

def create():
    sql_statement = '''CREATE TABLE IF NOT EXISTS "now" (
        "ID" INTEGER PRIMARY KEY,
        "NAME" TEXT NOT NULL,
        "DNS" TEXT NOT NULL,
        "IFACE" TEXT,
        "IP" TEXT,
        "MAC" TEXT,
        "HW" TEXT,
        "DATE" TEXT,
        "KNOWN" INTEGER DEFAULT 0,
        "NOW" INTEGER DEFAULT 0
    );'''
    db_exec(sql_statement)

    sql_statement = '''CREATE TABLE IF NOT EXISTS "history" (
        "ID" INTEGER PRIMARY KEY,
        "NAME" TEXT NOT NULL,
        "DNS" TEXT NOT NULL,
        "IFACE" TEXT,
        "IP" TEXT,
        "MAC" TEXT,
        "HW" TEXT,
        "DATE" TEXT,
        "KNOWN" INTEGER DEFAULT 0,
        "NOW" INTEGER DEFAULT 0
    );'''
    db_exec(sql_statement)

def insert(table, one_host):
    one_host['Name'] = quote_str(one_host['Name'])
    one_host['Hw'] = quote_str(one_host['Hw'])
    sql_statement = f'''INSERT INTO {table} ("NAME", "DNS", "IFACE", "IP", "MAC", "HW", "DATE", "KNOWN", "NOW") VALUES ('{one_host['Name']}','{one_host['DNS']}','{one_host['Iface']}','{one_host['IP']}','{one_host['Mac']}','{one_host['Hw']}','{one_host['Date']}','{one_host['Known']}','{one_host['Now']}');'''
    db_exec(sql_statement)

def update(table, one_host):
    one_host['Name'] = quote_str(one_host['Name'])
    one_host['Hw'] = quote_str(one_host['Hw'])
    sql_statement = f'''UPDATE {table} SET 
        "NAME" = '{one_host['Name']}', "DNS" = '{one_host['DNS']}', "IFACE" = '{one_host['Iface']}', "IP" = '{one_host['IP']}', "MAC" = '{one_host['Mac']}', "HW" = '{one_host['Hw']}', "DATE" = '{one_host['Date']}', "KNOWN" = '{one_host['Known']}', "NOW" = '{one_host['Now']}' 
        WHERE "ID" = '{one_host['ID']}';'''
    db_exec(sql_statement)

def delete(table, id):
    sql_statement = f'''DELETE FROM {table} WHERE "ID"='{id}';'''
    db_exec(sql_statement)

def delete_list(ids):
    if len(ids) > 0:
        id_string = ', '.join(map(str, ids))
        sql_statement = f'''DELETE FROM history WHERE "ID" IN ({id_string});'''
        db_exec(sql_statement)

def clear(table):
    sql_statement = f'''DELETE FROM {table};'''
    db_exec(sql_statement)

def quote_str(s):
    return s.replace("'", "''")  # Simple SQL injection prevention


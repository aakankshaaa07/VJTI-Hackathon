import sqlite3


def search(ip):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    query = f"""SELECT * FROM users WHERE ip='{ip}'"""
    cur.execute(query)
    return cur.fetchall()


def login(ip):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    data = search(ip)
    if len(data) == 0:
        query = f"""INSERT INTO users(ip) values ('{ip}')"""
        cur.execute(query)
        conn.commit()
        return 'user created'
    else:
        return data


def insert_contacts(ip, contacts):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    query = f"""Update users
    set contact1='{contacts[0]}',contact2='{contacts[1]}',contact3='{contacts[2]}',contact4='{contacts[3]}',contact5='{contacts[4]}' 
    where ip='{ip}'"""
    cur.execute(query)
    conn.commit()
    print("updated")
    return True


def see_table():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    query = f"""DELETE from users"""
    cur.execute(query)
    conn.commit()
    print(cur.fetchall())

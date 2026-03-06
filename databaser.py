import sqlite3



db = "mydb.db"
conn = sqlite3.connect(db)
curs = conn.cursor()

# create db table
curs.execute("CREATE TABLE IF NOT EXISTS users(username varchar(50) , password varchar(50));")

# add some data
add = False
for name,psw in {"ibrahim":"1234","ahmed":"saad"}.items() :
    if add : 
        curs.execute(f"INSERT INTO users values ('{name}','{psw}');")
        conn.commit()
conn.close()

# execute
def get_usernames(result:list):
    return [i[0] for i in result]

def username_exists(username:str):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    result = username in get_usernames(curs.execute("select username from users").fetchall())
    return result

def pass_of_user(username:str):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    result = curs.execute(f"select password from users where username = '{username}'").fetchone()[0]
    conn.close()
    return result
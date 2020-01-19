from sqlalchemy import create_engine
import os

if os.path.exists("base.db"):
    os.remove("base.db")
e = create_engine("sqlite:///base.db")
e.execute("""
    create table users (
        id integer primary key autoincrement,
        chat_id int,
        user_name varchar(60),
        user_surname varchar(70),
        company varchar(100),
        phone_number int
    )
""")

e.execute("""insert into users(chat_id, user_name, user_surname, company, phone_number)
 values ('3229','Ivan','Tsirulik','IDE','+79819668692')""")

result = e.execute(
            "select user_name,user_surname from "
            "users where chat_id=:chat_id",
    chat_id=3229)

result1 = e.execute(
            "select user_name,user_surname from "
            "users where chat_id=:chat_id",
    chat_id=322)

try:
    output = ' '.join(result.fetchone())
    print(output)
    output1 = ' '.join(result1.fetchone())
    print(output1)
except:
    print('No records in database')

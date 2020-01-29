from sqlalchemy import create_engine
import hashlib
import os

if os.path.exists("base.db"):
    os.remove("base.db")
e = create_engine("sqlite:///base.db")
e.execute("""
    create table users (
        id integer primary key autoincrement,
        chat_id int unique,
        user_name varchar(60),
        user_surname varchar(70),
        company varchar(100),
        phone_number int not null,
        group_name int,
        score int default 10,
        reg_date datetime default current_timestamp,
        last_activity datetime,
        number_of_conversation int default 0
    )
""")

e.execute("""
    create table groups (
        id integer primary key autoincrement,
        group_code varchar(15) unique,
        admin_id integer,
        group_name varchar(60) unique,
        company varchar(100)
    )
""")

e.execute("""
    create table conversation (
        id integer primary key autoincrement,
        begin_date datetime default current_timestamp,
        rus_side int,
        china_side int,
        is_finished boolean default false,
        finish_date datetime
    )
""")

e.execute("""
    create table conversation_result (
        id int unique not null,
        SCV int not null,
        duration datetime,
        message_number1 int not null,
        message_number2 int not null
    )
""")

e.execute("""                                                         
    create table admins (
        id integer primary key autoincrement,
        chat_id integer unique,
        name varchar(60),
        surname varchar(70),
        pass varchar(65),
        reg_date datetime default current_timestamp
    )
""")

e.execute("""                                                         
    create table test_res (
        user_id int unique,
        res1 int,
        answers int
    )
""")

e.execute("""insert into admins ('chat_id', 'name', 'surname', 'pass')
         values ('248837560','Иван', 'Цирулик', '{0}')""".format(hashlib.sha3_256(b'12345').hexdigest()))

e.execute("""insert into admins ('chat_id', 'name', 'surname', 'pass')
         values ('2421312331','wqeан', 'qweqрулик', '{0}')""".format(hashlib.sha3_256(b'54321').hexdigest()))


class Controller:
    def __init__(self, db_name, driver_name="sqlite"):
        self.engine('{0}:///{1}'.format(driver_name, db_name))

    def add_record(self, table_name,
                   col_names=('chat_id', 'user_name', 'user_surname', 'company', 'phone_number'),
                   *col_values):
        self.engine.execute("""insert into {0} {1}
         values {2}""".format(table_name, col_names, col_values))

    def query_one(self, cond, table_name, col_name=('user_name', 'user_surname')):
        tmp = self.engine.execute(
            "select {0} from "
            "users where chat_id=:chat_id".format())
        return " ".join(tmp)


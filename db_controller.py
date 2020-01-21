from sqlalchemy import create_engine


class Controller(object):

    def __init__(self, db_name, driver_name="sqlite"):
        self.engine = create_engine('{0}:///{1}'.format(driver_name, db_name))

    def add_record(self, col_values, table_name='users',
                   col_names=('chat_id', 'user_name', 'user_surname', 'company', 'phone_number')):
        self.engine.execute("""insert into {0} {1}
         values {2}""".format(table_name, col_names, col_values))

    def query(self, cond, cond_value, table_name = 'users',
              col_name=('user_name', 'user_surname')):
        res = self.engine.execute(
            "select {0} from "
            "{1} where {2}={3}".format(','.join(col_name), table_name, cond, cond_value))
        try:
            return " ".join(res.fetchone())
        except Exception as err:
            print(err)
            return None

    def query_all(self, table_name):
        res = self.engine.execute(
            "select * from {0}".format(table_name))
        try:
            return res.fetchall()
        except Exception as err:
            print(err)
            return None


if __name__ == '__main__':
    controller = Controller('base.db')
    print(controller.query('chat_id', '2123'))
    print(controller.query_all('users'))

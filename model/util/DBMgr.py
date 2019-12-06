import pymysql

from model.util.Config import Config

class DBMgr:
    def __init__(self):
        self.__state = False
        self.__cfg = Config()
        self.__db_data = self.__cfg.getDatabase()

    def mysql_error(self):
        return pymysql.MySQLError

    def conn(self):
        try:
            self.connection = pymysql.connections.Connection(
                host='localhost',
                user=self.__db_data['user'],
                passwd=self.__db_data['passwd'],
                db=self.__db_data['db'],
                charset=self.__db_data['charset'],
                cursorclass=pymysql.cursors.DictCursor)
            self.state = True
            return self.connection

        except self.mysql_error() as e:
            self.state = False
            print('[@DBMgr] 【{}】{!r}'.format(e.args[0], e.args[1]))
            self.conn()

    def cursor(self):
        try:
            self.connection
        except:
            self.conn()

        return self.connection.cursor()

    def commit(self):
        try:
            self.connection
        except:
            self.conn()

        return self.connection.commit()

    def close(self):
        try:
            self.connection
        except:
            self.conn()
        else:
            self.cursor().close()
            self.connection.close()
            del self.connection

    def insert(self, sql, args, multiple=False):
        row = -1
        result = -1
        if(self.conn()):
            try:
                with self.cursor() as cursor:
                    if not multiple:
                        row = cursor.execute(sql, args)
                    else:
                        row = cursor.executemany(sql, args)
                    self.commit()

                    result_id = cursor.lastrowid if not multiple else [cursor.lastrowid + i for i in range(row)]
            except self.mysql_error() as e:
                print('[@DBMgr] 【{}】{!r}'.format(e.args[0], e.args[1]))
                return False, row, (e.args[0], e.args[1])

        else:
            print("[@DBMgr] Fails to connect to MySQL Server!!")
            return False, row, (e.args[0], e.args[1])

        self.close()
        return True, row, result_id

    def update(self, sql, args):
        row = -1
        result = -1
        if(self.conn()):
            try:
                with self.cursor() as cursor:
                    row = cursor.execute(sql, args)
                    self.commit()

            except self.mysql_error() as e:
                print('[@DBMgr] 【{}】{!r}'.format(e.args[0], e.args[1]))
                return False, row, (e.args[0], e.args[1])

        else:
            print("[@DBMgr] Fails to connect to MySQL Server!!")
            return False, row, (e.args[0], e.args[1])

        self.close()
        return True, row, result

    def query(self, sql, args, fetch='all'):
        row = -1
        result = list()
        if(self.conn()):
            try:
                with self.cursor() as cursor:
                    row = cursor.execute(sql, args)
                    result = cursor.fetchone() if fetch != 'all' else cursor.fetchall()
                    self.commit()

            except self.mysql_error() as e:
                print('[@TaskHandler] 【{}】{!r}'.format(e.args[0], e.args[1]))
                return False, row, (e.args[0], e.args[1])

        else:
            print("[@TaskHandler] Fails to connect to MySQL Server!!")
            return False, row, (e.args[0], e.args[1])

        self.close()

        return True, row, result

    def delete(self, sql, args):
        row = -1
        result = list()
        if(self.conn()):
            try:
                with self.cursor() as cursor:
                    row = cursor.execute(sql, args)
                    self.commit()

            except self.mysql_error() as e:
                print('[@DBMgr] 【{}】{!r}'.format(e.args[0], e.args[1]))
                return False, row, (e.args[0], e.args[1])

        else:
            print("[@DBMgr] Fails to connect to MySQL Server!!")
            return False, row, (e.args[0], e.args[1])

        self.close()

        return True, row, result

    def string_to_list(self, string, d_type='string'):
        if d_type == 'string':
            string_list = [n for n in string.split('|')]
        elif d_type == 'int':
            string_list = [int(n) for n in string.split('|')]
        elif d_type == 'float':
            string_list = [float(n) for n in string.split('|')]

        return string_list

    def list_to_string(self, ori_list):
        string = ""
        if len(ori_list) == 0:
            pass
        else:
            # 使用特殊符號作區隔
            for sub_list in ori_list:
                string = string + "|" + str(sub_list)

            string = string[1:]

        return string

    def list_to_dict(self, key_column, data):
        result_dict = dict()

        for item in data:
            result_dict.update({item[key_column]: item})

        return result_dict

    def get_db_column(self, db, table):
        if(self.conn()):
            try:
                with self.cursor() as cursor:
                    sql = "SELECT `COLUMN_NAME` AS `name` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = %(db)s AND `TABLE_NAME` = %(table)s"
                    args = {
                        'db': db,
                        'table': table
                    }

                    num_of_rows = int(cursor.execute(sql, args))
                    result = cursor.fetchall()
                    self.commit()

            except self.mysql_error() as e:
                print('[@DBMgr] 【{}】{!r}'.format(e.args[0], e.args[1]))

        else:
            print("[@DBMgr] Fails to connect to MySQL Server!!")
        self.close()

        return result

    def insert_sql(self, table, column_dict, have_id):
        if have_id:
            col_dict = column_dict
        else:
            col_dict = column_dict[1:]

        query_columns = list()
        query_placeholders = list()

        for each in col_dict:
            query_columns.append('`' + each['name'] + '`')
            query_placeholders.append('%(' + each['name'] + ')s')

        query_columns = ', '.join(query_columns)
        query_placeholders = ', '.join(query_placeholders)
        insert_query = "INSERT INTO `%s` (%s) VALUES (%s)" %(table, query_columns, query_placeholders)

        return insert_query

    def query_sql(self, table, column_dict, have_id):
        if have_id:
            col_dict = column_dict
        else:
            col_dict = column_dict[1:]

        query = list()

        for each in col_dict:
            query.append('`' + each['name'] + '`' + '=' + '%(' + each['name'] + ')s')

        query = ' AND '.join(query)
        query_sql = "SELECT * FROM %s WHERE %s" %(table, query)

        return query_sql

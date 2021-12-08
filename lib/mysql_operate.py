import pymysql
from conf import database


class MySqlOperate:
    def __init__(self):
        db_object = database['zumoo']['prod']
        self.connect = pymysql.connect(
            host=db_object['host'], port=db_object['port'],
            user=db_object['username'], password=db_object['password'],
            database=db_object['database']
        )
        self.cursor = self.connect.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()

    def get_index_dict(self):
        """
        获取数据库对应表中的字段名
        """
        index_dict = dict()
        index = 0
        for desc in self.cursor.description:
            index_dict[desc[0]] = index
            index = index + 1
        return index_dict

    def execute_sql(self, sql, array=None):
        try:
            self.cursor.execute(sql, args=array)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            raise e

    def query_all(self, sql, array=None):
        self.execute_sql(sql, array)
        return self.cursor.fetchall()

    def query_all_with_column(self, sql, array=None):
        data = self.query_all(sql, array)
        index_dict = self.get_index_dict()
        res = []
        for d in data:
            res_i = dict()
            for index_i in index_dict:
                res_i[index_i] = d[index_dict[index_i]]
            res.append(res_i)
        return res

    def query_one(self, sql):
        self.execute_sql(sql)
        return self.cursor.fetchone()

    def query_one_with_column(self, sql):
        data = self.query_one(sql)
        if data:
            index_dict = self.get_index_dict()
            res = dict()
            for index_i in index_dict:
                res[index_i] = data[index_dict[index_i]]
            return res
        else:
            return data

    def query_many(self, sql, size):
        self.execute_sql(sql)
        return self.cursor.fetchmany(size=size)

    def executemany_sql(self, sql, data_list):
        """
        EXAMPLE
        :param sql:'insert into table_name (column1,column2,column3,...) values (%s, %s, %s, ...);'
        :param data_list: [[content1,content2,content3], [content1,content2,content3]]
        """
        try:
            self.cursor.executemany(sql, data_list)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            raise Exception(e)

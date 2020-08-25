# coding:utf-8
from crawler.settings import SERVICE_DATABASE
import pymysql


class DBUtil:
    def __init__(self, db_config=None):
        if db_config is None:
            self.db_config = SERVICE_DATABASE
        else:
            self.db_config = db_config

    def _get_mysql_connector(self):
        connection = pymysql.connect(**self.db_config)
        return connection

    def query_db_as_list(self, sql):
        connection = self._get_mysql_connector()
        data = []
        try:
            with connection.cursor() as cur:
                index_dict = dict()
                index = 0
                cout = cur.execute(sql)

                for desc in cur.description:
                    index_dict[desc[0]] = index
                    index += 1

                for row in cur.fetchall():
                    resi = dict()
                    for indexi in index_dict:
                        resi[indexi] = row[index_dict[indexi]]
                    data.append(resi)
        finally:
            connection.close()
        return data

    def update(self, sql):
        connection = self._get_mysql_connector()
        try:
            cur = connection.cursor()
            cur.execute(sql)
            connection.commit()
        except:
            raise RuntimeError("更新失败：" + str(sql))
        finally:
            connection.close()

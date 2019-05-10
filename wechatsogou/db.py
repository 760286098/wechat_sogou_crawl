# -*- coding: utf-8 -*-

import pymysql

from . import config


class mysql:
    """数据库类
    """

    def __init__(self, table=''):
        self._conn = pymysql.connect(host=config.host, user=config.user, passwd=config.passwd, db=config.db,
                                     charset=config.charset, cursorclass=pymysql.cursors.DictCursor)
        self._cur = self._conn.cursor()

        if table:
            self._table_name = table
        self._where_sql = ''

    def __update(self, sqls):
        """更新语句，可执行update,insert语句
        """
        if type(sqls) is str:
            self._cur.execute(sqls)
        elif type(sqls) is list:
            for sql in sqls:
                self._cur.execute(sql)
        self._conn.commit()

    def __close(self):
        """关闭所有连接
        """
        self._cur.close()
        self._conn.close()

    def __del__(self):
        """析构函数
        """
        self._conn.commit()
        self.__close()

    """
    以下是封装的提供使用的
    """

    def table(self, table):
        """设置数据表, 链式操作
        """
        self._table_name = table
        return self

    def where(self, where):
        """设置条件, 链式操作
        """
        if type(where) is dict:
            where_sql = ''
            for k, v in where.items():
                where_sql += "`" + str(k) + "` LIKE '" + str(v) + "' and "
            self._where_sql = " where " + where_sql[:-5]
        return self

    def add(self, data):
        """插入数据
        """
        ks = ''
        vs = ''
        for k, v in data.items():
            ks += "`" + str(k).replace('\'', '\\\'') + "`,"
            vs += "'" + str(v).replace('\'', '\\\'') + "',"
        sql = "insert into " + "`" + self._table_name + "` (" + ks[:-1] + ") values (" + vs[:-1] + ")"
        self.__update(sql)

    def update(self, data):
        """更新数据
        """
        data_sql = ''
        for k, v in data.items():
            data_sql += "`" + str(k) + "` = '" + str(v) + "',"
        sql = "update `" + self._table_name + "` set " + data_sql[:-1] + self._where_sql + ";"
        self.__update(sql)

    def find(self, size=25, order_sql=''):
        """查询数据
        """
        sql = "select * from " + "`" + self._table_name + "`" + self._where_sql + order_sql
        self.__update(sql)
        if size == 0:
            return self._cur.fetchall()
        elif size == 1:
            return self._cur.fetchone()
        else:
            return self._cur.fetchmany(size)

    def delete(self):
        """删除语句
        """
        sql = "delete from " + "`" + self._table_name + "`" + self._where_sql
        self.__update(sql)

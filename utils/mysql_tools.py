# -*- coding: utf-8 -*-
# @Time    : 2023/9/26 9:33
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : mysql_tools.py
# @Software: PyCharm

import pymysql

from utils.LogHandler import log


def mysql_link():
    try:
        conn = pymysql.connect(
            host="192.168.102.20",
            port=3306,
            user="root",
            password="123456",
            database="Certificate",
            charset='utf8mb4'
        )
    except Exception as e:
        log.error('数据库连接失败', e.args)

    return conn


# 定义一个函数，用于执行查询语句
def execute_query(sql):
    # 创建一个数据库连接
    conn = mysql_link()
    # 创建一个游标
    cursor = conn.cursor()
    try:
        # 执行查询语句
        cursor.execute(sql)
        # 获取查询结果
        result = cursor.fetchall()
        # 提交查询
        conn.commit()
        # 返回查询结果
        return result
    except Exception as e:
        # 打印查询失败信息
        print('查询失败:', e.args)
        # 回滚查询
        conn.rollback()
        # 返回None
        return None
    finally:
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()


if __name__ == '__main__':
    sql_query = "SELECT * FROM cert"
    result = execute_query(sql_query)
    if result:
        for row in result:
            print(row)

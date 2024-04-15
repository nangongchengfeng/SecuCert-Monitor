# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 17:10
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : controller.py
# @Software: PyCharm
from utils.mysql_tools import execute_query


def get_day_less_30_re():
    """
        获取MySQL数据表中的证书有效期，如果证书有效期小于30天，就发送钉钉给相关人员
        :return:
        """
    sql = """
            SELECT
        service_name,
        use_deploy,
        deployA,
        deployB,
        product,
        scene,
        organ,
        manage,
        manage_id,
        issuance_date,
        expiration_date,
        header,
        yumwei,
        yumwei_time,
        manager,
        type,
        DATEDIFF(expiration_date, NOW()) AS day_validity
    FROM
        Certificate.expiration_monitor
    WHERE
        DATEDIFF(expiration_date, NOW()) >= 0
        AND DATEDIFF(expiration_date, NOW()) < 30  -- 仅包括有效期小于30天的记录
    ORDER BY
        day_validity ASC
    LIMIT 10;
            """
    result = execute_query(sql)
    data_list = []
    for row in result:
        data_dict = {
            "service_name": row[0],
            "use_deploy": row[1],
            "deployA": row[2],
            "deployB": row[3],
            "product": row[4],
            "scene": row[5],
            "organ": row[6],
            "manage": row[7],
            "manage_id": row[8],
            "issuance_date": str(row[9]),
            "expiration_date": str(row[10])[:10],
            "header": row[11],
            "yumwei": row[12],
            "yumwei_time": row[13],
            "manager": row[14],
            "type": row[15],
            "day_validity": row[16]
        }
        data_list.append(data_dict)
    return data_list


def get_days_tops():
    """
    根据证书有效期进行排序，获取前10条数据
    :return:
    """
    sql = """
SELECT
	service_name,
	use_deploy,
	deployA,
	deployB,
	product,
	scene,
	organ,
	manage,
	manage_id,
	issuance_date,
	expiration_date,
	header,
	yumwei,
	yumwei_time,
	manager,
	type,
	DATEDIFF(expiration_date, NOW()) AS day_validity
FROM
	Certificate.expiration_monitor
WHERE
	DATEDIFF(expiration_date, NOW()) >= 0
ORDER BY
	day_validity ASC
LIMIT 10;

    """
    result = execute_query(sql)


    data_list = []
    for row in result:
        data_dict = {
            "service_name": row[0],
            "use_deploy": row[1],
            "deployA": row[2],
            "deployB": row[3],
            "product": row[4],
            "scene": row[5],
            "organ": row[6],
            "manage": row[7],
            "manage_id": row[8],
            "issuance_date": str(row[9]),
            "expiration_date": str(row[10])[:10],
            "header": row[11],
            "yumwei": row[12],
            "yumwei_time": row[13],
            "manager": row[14],
            "type": row[15],
            "day_validity": row[16]
        }
        data_list.append(data_dict)
    return data_list




def get_count_type():
    """
    获取证书类型的数量
    :return:
    """
    sql = f"""
    SELECT type, COUNT(*) AS count
    FROM expiration_monitor
    GROUP BY type;
    """

    result = execute_query(sql)
    return result



def get_datas():
    sql = """
                SELECT
    	service_name,
    	use_deploy,
    	deployA,
    	deployB,
    	product,
    	scene,
    	organ,
    	manage,
    	manage_id,
    	issuance_date,
    	expiration_date,
    	header,
    	yumwei,
    	yumwei_time,
    	manager,
    	type,
    	DATEDIFF(
    		expiration_date,
    	NOW()) AS day_validity 
    FROM
    	Certificate.expiration_monitor;
            """
    data_dict = execute_query(sql)
    data_lists = []
    for row in data_dict:
        data_dict = {
            "service_name": row[0],
            "use_deploy": row[1],
            "deployA": row[2],
            "deployB": row[3],
            "product": row[4],
            "scene": row[5],
            "organ": row[6],
            "manage": row[7],
            "manage_id": row[8],
            "issuance_date": str(row[9]),
            "expiration_date": str(row[10])[:10],
            "header": row[11],
            "yumwei": row[12],
            "yumwei_time": row[13],
            "manager": row[14],
            "type": row[15],
            "day_validity": row[16]
        }

        data_lists.append(data_dict)
    return  data_lists
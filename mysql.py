# -*- coding:utf-8 -*- 

##########################################################
#               Rutap Bot 2019 Mysql Module              #
#                 Under The MIT License                  #
##########################################################

import pymysql, setting

Setting = setting.Settings()

def mysql_do(query):
    connect = pymysql.connect(host=Setting.mysql_ip, user=Setting.mysql_id, password=Setting.mysql_pw, db=Setting.mysql_db, charset='utf8mb4')
    try:
        with connect.cursor() as cur:
            cur.execute(query)
        connect.commit()
    finally:
        connect.close()

def mysql_do_return(query):
    connect = pymysql.connect(host=Setting.mysql_ip, user=Setting.mysql_id, password=Setting.mysql_pw, db=Setting.mysql_db, charset='utf8mb4')
    try:
        with connect.cursor() as cur:
            cur.execute(query)
            row = cur.fetchall()
        connect.commit()
    finally:
        connect.close()
        return row

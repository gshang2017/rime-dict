#!/usr/bin/env python
# coding=utf-8

import os
import requests
import sqlite3

def download_sogou_secl():

    #指定工作目录
    os.chdir('./')
    #创建目录
    if os.path.exists("sogou.temp.scel"):
        os.remove("sogou.temp.scel")
    if os.path.exists("sogou.temp.txt"):
        os.remove("sogou.temp.txt")
    dict_db = sqlite3.connect('dict.db')
    #创建一个游标 cursor
    cursor = dict_db.cursor()
    cursor.execute("SELECT * FROM status WHERE download_status=0" )
    data = cursor.fetchall()
    for i in data:
        cursor.execute("DROP TABLE IF EXISTS update_tmp_old" )
        cursor.execute("CREATE TABLE IF NOT EXISTS update_tmp_old (dict_name TEXT,index_num TEXT,dict TEXT,dict_frequency INTEGER)" )
        cursor.execute("DROP TABLE IF EXISTS update_tmp_new" )
        cursor.execute("CREATE TABLE IF NOT EXISTS update_tmp_new (dict_name TEXT,index_num TEXT,dict TEXT,dict_frequency INTEGER)" )

        dict_db.commit()

        dict_name = i[0]
        index_num = i[2]
        dict_download_url = i[3]
        dict_table_name = i[5]
        cursor.execute("SELECT dict FROM %s WHERE index_num='%s'  LIMIT 1 " %(dict_table_name,index_num))
        dict_len = len(cursor.fetchall())
        print(index_num)
        #print(dict_len)
        if dict_len > 0:
            cursor.execute("insert into update_tmp_old select * from '%s' WHERE index_num='%s'" %(dict_table_name,index_num) )
            cursor.execute("DELETE FROM %s WHERE index_num='%s'" %(dict_table_name,index_num))
        dict_db.commit()


        #下载细胞词文件sogou.temp.scel
        r = requests.get(dict_download_url)
        scel_file = open("sogou.temp.scel", "wb+")
        scel_file.write(r.content)
        scel_file.close()
        command = os.system("dotnet ./imewlconverter/ImeWlConverterCmd.dll -i:scel sogou.temp.scel -o:word sogou.temp.txt")
        if command == 0 :
            file = open('sogou.temp.txt')
            for line in file.readlines():
                line_data = line.strip()
                cursor.execute("SELECT dict FROM update_tmp_old WHERE index_num='%s' and dict='%s'  LIMIT 1 " %(index_num,line_data))
                dict_old_len = len(cursor.fetchall())
                if dict_old_len > 0:
                    cursor.execute("insert into update_tmp_new select * from update_tmp_old WHERE dict='%s'" %line_data )
                else:
                    cursor.execute("insert into update_tmp_new values('%s','%s','%s',NULL)" %(dict_name,index_num,line_data))
                dict_db.commit()
            file.close()
            cursor.execute("insert into %s select * from update_tmp_new WHERE index_num='%s'" %(dict_table_name,index_num) )
            dict_db.commit()
            cursor.execute("SELECT dict FROM %s WHERE index_num='%s'  LIMIT 1 " %(dict_table_name,index_num))
            dict_len = len(cursor.fetchall())
            if dict_len > 0:
                cursor.execute("UPDATE status SET download_status=1 WHERE index_num='%s'" %index_num)
        dict_db.commit()

    cursor.execute("DROP TABLE IF EXISTS update_tmp_old" )
    cursor.execute("DROP TABLE IF EXISTS update_tmp_new" )
    dict_db.commit()
    cursor.execute("VACUUM" )


    # 关闭游标
    cursor.close()
    # 关闭连接
    dict_db.close()
    if os.path.exists("sogou.temp.scel"):
        os.remove("sogou.temp.scel")
    if os.path.exists("sogou.temp.txt"):
        os.remove("sogou.temp.txt")

if __name__ == '__main__':

    download_sogou_secl()

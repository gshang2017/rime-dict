#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

dict_db = sqlite3.connect('dict.db')
cursor = dict_db.cursor()
cursor.execute("SELECT table_name FROM dict_name " )
data_table_name = cursor.fetchall()
for i in data_table_name:
    cursor.execute("SELECT %s FROM %s " %(i[0]+"_dict_table_name",i[0]) )
    data_dict_table_name = cursor.fetchall()
    for j in data_dict_table_name:
        cursor.execute("SELECT DISTINCT dict FROM %s WHERE dict_frequency IS NULL "%(j[0]))
        data_dict_name = cursor.fetchall()
        for k in data_dict_name:
            if  k[0] is None or len(k[0].encode('utf-8').decode("utf-8-sig")) == 0:
                continue
            elif i[0] == "english_character_encoding" :
                tengxun_ai_name = "tengxun_ai_english"
            elif i[0] == "lettered_word" :
                tengxun_ai_name = "tengxun_ai_split_8"
            elif len(k[0].encode('utf-8').decode("utf-8-sig")) > 6:
                tengxun_ai_name = "tengxun_ai_split_7"
            else:
                tengxun_ai_name = "tengxun_ai_split_"+str(len(k[0].encode('utf-8').decode("utf-8-sig")))
            if i[0] == "lettered_word" :
                cursor.execute("SELECT dict_frequency FROM %s  WHERE dict='%s' LIMIT 1 " %(tengxun_ai_name,k[0].encode('utf-8').decode("utf-8-sig").lower()))
            else:
                cursor.execute("SELECT dict_frequency FROM %s  WHERE dict='%s' LIMIT 1 " %(tengxun_ai_name,k[0].encode('utf-8').decode("utf-8-sig")))
            tengxun_freq_unm = cursor.fetchall()
            if len(tengxun_freq_unm) > 0:
                dict_freq_num = tengxun_freq_unm[0][0]
                cursor.execute("UPDATE %s SET dict_frequency='%s' WHERE dict='%s'" %(j[0],dict_freq_num,k[0]))
            else:
                cursor.execute("UPDATE %s SET dict_frequency=0 WHERE dict='%s'" %(j[0],k[0]))
        dict_db.commit()
dict_db.commit()
cursor.execute("VACUUM" )
cursor.close()
dict_db.close()

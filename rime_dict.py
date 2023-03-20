#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import lxml
from bs4 import BeautifulSoup
import sqlite3
import pandas.io.sql as sql
import datetime
import shutil
import csv
import fileinput

#创建输出目录
if not os.path.exists('./output'):
    os.mkdir('./output')

#转换格式
def imewlconverter(name):
    scel_output_file = name + '.dict.yaml'
    if name.find("basic") != -1:
        rime_freq = os.getenv('RIME_BASIC_FREQ',default = 3)
    elif name.find(".official") != -1:
        rime_freq = os.getenv('RIME_OFFICIAL_FREQ',default = 2)
    else:
        rime_freq =  os.getenv('RIME_UNOFFICIAL_FREQ',default = 1)
    if tengxun_freq:
        command='''dotnet ../imewlconverter/ImeWlConverterCmd.dll -i:rime %s -ft:"rm:eng|rm:num|rm:space|rm:pun" -o:self "%s"  "-f:213 \tnyyy" -ct:%s ''' % (name+".txt",scel_output_file,rime_converter_type)
    else:
        command='''dotnet ../imewlconverter/ImeWlConverterCmd.dll -i:word %s -r:%s -ft:"rm:eng|rm:num|rm:space|rm:pun" -o:rime "%s"  -ct:%s ''' % (name+".txt",rime_freq,scel_output_file,rime_converter_type)
    attempts = 0
    while attempts < 4:
        try:
            if os.path.exists(scel_output_file):
                break
            os.system(command)
        except:
            attempts += 1
            if attempts==4:
                os._exit(0)

#拆分文件
def split_file(name):
    shutil.copy(name+".txt","part1."+name+".txt")
    shutil.copy(name+".txt","part2."+name+".txt")
    fr = open(name+".txt",'r')
    count = len(fr.readlines())
    fr.close()
    num = count//2
    fr_part2 = open("part2."+name+".txt", 'r')
    a = fr_part2.readlines()
    fw_part2 = open("part2."+name+".txt", 'w')
    b = ''.join(a[num:])
    fw_part2.write(b)
    fr_part2.close()
    if (count % 2) == 0:
        num2 = num
    else:
        num2 = num+1
    fr_part1 = open("part1."+name+".txt", 'r')
    a = fr_part1.readlines()
    fw_part1 = open("part1."+name+".txt", 'w')
    b = ''.join(a[:-num2])
    fw_part1.write(b)
    fr_part1.close()

#合并文件
def merge_file(filename_1, filename_2):
    f1 = open(filename_1,'a+',encoding='utf-8')
    with open(filename_2,'r',encoding='utf-8') as f2:
        for i in f2:
            f1.write(i)

#输出rime文件
def rime_yaml_output(filename_1,filename_2):

    #完善yaml文件输出格式
    data1 = '''# Rime dictionary
# encoding: utf-8
#
'''
    if filename_1.find("basic_dict") != -1:
        data2 = "#自定义基础词汇"+"\n"
        data3 = "#"
    elif filename_1.find("english_dict") != -1:
        data2 = "#自定义英语词汇"+"\n"
        data3 = "#"
    else:
        data2 = "#sogou输入法("+filename_2+")词汇"+"\n"
        data3 = "#"+sogou_nav_url
    data4 = '''
# 部署位置：
# ~/.config/ibus/rime  (Linux ibus)
# ~/.config/fcitx/rime  (Linux fcitx)
# ~/Library/Rime  (Mac OS)
# %APPDATA%\Rime  (Windows)
#
# 于重新部署后生效
#
---
'''
    #创建名称
    data5 = "name: "+filename_1+"\n"
    #创建时间
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data6 = "version: \""+now+"\""
    data7 = '''
sort: by_weight
use_preset_vocabulary: false
columns:
  - text #第一列字／词
  - code #第二列码
  - weight #第三列字／词频
...
'''
    output_file = open(filename_1+".dict.yaml", "r+")
    old = output_file.read()
    output_file.seek(0)
    output_file.write(data1)
    output_file.write(data2)
    output_file.write(data3)
    output_file.write(data4)
    output_file.write(data5)
    output_file.write(data6)
    output_file.write(data7)
    output_file.write(old)
    #opencc转换
    if rime_opencc:
            os.system('''opencc  --noflush 1 -i %s -o %s -c %s''' %(filename_1+".dict.yaml",filename_1+".dict.yaml",rime_opencc_config))
    os.chmod(filename_1+".dict.yaml", 0o0777)

#输出原始文件
def conver_file(tablename,filename_1,filename_2):
    yaml_dict_name = filename_1+".txt"
    tablename.to_csv(yaml_dict_name,header=0,sep='\t',index=False)
    if tengxun_freq and yaml_dict_name.find("basic_dict") == -1:
        cursor.execute("CREATE TABLE IF NOT EXISTS tmp_tengxun_freq (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
        if yaml_dict_name.find(".official") != -1:
            rime_freq = os.getenv('RIME_OFFICIAL_FREQ',default = 2)
        else:
            rime_freq =  os.getenv('RIME_UNOFFICIAL_FREQ',default = 1)
        fr1 = open(yaml_dict_name, 'r',encoding='UTF-8')
        for line in fr1.readlines():
            tmp_data = line.replace("\n","").split("\t", 1)
            if tmp_data[1] == '0':
                cursor.execute("insert into tmp_tengxun_freq values('%s','%s','%s')"%(tmp_data[0],'',rime_freq))
            else:
                cursor.execute("insert into tmp_tengxun_freq values('%s','%s','%s')"%(tmp_data[0],'',tmp_data[1]))
        dict_db.commit()
        fr1.close()
        if basic_dict_set:
            table_freq = sql.read_sql("SELECT * FROM tmp_tengxun_freq a WHERE a.dict NOT IN (SELECT DISTINCT b.dict FROM tmp_basic_dict b )  GROUP BY dict" , dict_db)
        else:
            table_freq = sql.read_sql("SELECT * FROM tmp_tengxun_freq  GROUP BY dict" , dict_db)
        table_freq.to_csv(yaml_dict_name,header=0,sep='\t',index=False)
        cursor.execute("DROP TABLE IF EXISTS tmp_tengxun_freq" )
    txt_size = os.path.getsize(filename_1+".txt")
    if txt_size > 30000000:
        split_file(filename_1)
    #转换sql导出文件
    if os.path.exists("part1."+filename_1+".txt"):
        imewlconverter("part1."+filename_1)
        imewlconverter("part2."+filename_1)
        merge_file("part1."+filename_1+".dict.yaml", "part2."+filename_1+".dict.yaml")
        shutil.copy("part1."+filename_1+".dict.yaml",filename_1+".dict.yaml")
        os.remove("part1."+filename_1+".txt")
        os.remove("part2."+filename_1+".txt")
        os.remove("part1."+filename_1+".dict.yaml")
        os.remove("part2."+filename_1+".dict.yaml")
    else:
        imewlconverter(filename_1)
    if polyphonic_set and yaml_dict_name.find("basic_dict") != -1:
        basic_freq = os.getenv('RIME_BASIC_FREQ',default = 3)
        table_polyphonic_dict = sql.read_sql("SELECT * FROM polyphonic_all a WHERE a.dict IN (SELECT b.dict FROM tmp_basic_dict b) GROUP BY dict,dict_code" , dict_db)
        table_polyphonic_dict.to_csv('polyphonic_dict.txt',header=0,sep='\t',index=False)
        fr1 = open('polyphonic_dict.txt', 'r',encoding='UTF-8')
        for line in fr1.readlines():
            tmp_data = line.replace("\n","").split("\t", 2)
            if tmp_data[2] == '0' or not tengxun_freq:
                cursor.execute("insert into tmp_polyphonic values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],basic_freq))
            else:
                cursor.execute("SELECT * FROM polyphonic_percentage WHERE dict='%s'" % tmp_data[0])
                polyphonic_dict = cursor.fetchall()
                polyphonic_dict_len = len(polyphonic_dict)
                if  polyphonic_dict_len > 0:
                    cursor.execute("SELECT * FROM polyphonic_percentage WHERE dict='%s' AND dict_code='%s'" % (tmp_data[0],tmp_data[1]))
                    polyphonic_percentage = cursor.fetchall()
                    polyphonic_percentage_len = len(polyphonic_percentage)
                    if  polyphonic_percentage_len > 0:
                        cursor.execute("insert into tmp_polyphonic values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],int(int(tmp_data[2])*polyphonic_percentage[0][2])))
                    else:
                        cursor.execute("insert into tmp_polyphonic values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],basic_freq))
                else:
                    cursor.execute("insert into tmp_polyphonic values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],tmp_data[2]))
        fr1.close()
        dict_db.commit()
        fr2 = open(prefix_dict_name+"basic_dict.dict.yaml", 'r',encoding='UTF-8')
        for line in fr2.readlines():
            tmp_data = line.replace("\n","").split("\t", 2)
            if tmp_data[2] == '1':
                cursor.execute("insert into tmp_polyphonic values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],basic_freq))
                if len(tmp_data[0]) == 1:
                    cursor.execute("insert into tmp_polyphonic_fix values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],basic_freq))
            else:
                cursor.execute("insert into tmp_polyphonic values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],tmp_data[2]))
                if len(tmp_data[0]) == 1:
                    cursor.execute("insert into tmp_polyphonic_fix values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],tmp_data[2]))
        #无韵母多音字修正 no_finals
        if no_finals_fix_set:
            no_finals = ['m','n','hm','ng','hng']
            for line in no_finals:
                cursor.execute("SELECT * FROM tmp_polyphonic_fix a WHERE a.dict IN (SELECT b.dict FROM tmp_polyphonic b WHERE dict_code='%s' ) "% line)
                tmp_data = cursor.fetchall()
                tmp_data_len = len(tmp_data)
                if tmp_data_len > 0:
                    for i in range(0, tmp_data_len):
                        cursor.execute("UPDATE tmp_polyphonic SET dict_code='%s',dict_frequency='%s' WHERE dict='%s' and (dict_code='%s' or dict_code='%s' )" % (tmp_data[i][1],tmp_data[i][2],tmp_data[i][0],line,tmp_data[i][1]))
        dict_db.commit()
        fr2.close()
        table_polyphonic_dict_new = sql.read_sql("SELECT * FROM tmp_polyphonic GROUP BY dict,dict_code" , dict_db)
        table_polyphonic_dict_new.to_csv(filename_1+".dict.yaml",header=0,sep='\t',index=False)
    if order_set:
        cursor.execute("DROP TABLE IF EXISTS tmp_order" )
        cursor.execute("CREATE TABLE IF NOT EXISTS tmp_order (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
        fr3 = open(filename_1+".dict.yaml", 'r',encoding='UTF-8')
        for line in fr3.readlines():
            tmp_data = line.replace("\n","").split("\t", 2)
            if int(len_num_set):
                if len(tmp_data[0]) <= int(len_num_set):
                    cursor.execute("insert into tmp_order values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],tmp_data[2]))
            else:
                cursor.execute("insert into tmp_order values('%s','%s','%s')"%(tmp_data[0],tmp_data[1],tmp_data[2]))
        dict_db.commit()
        fr3.close()
        table_order_dict = sql.read_sql("SELECT * FROM tmp_order GROUP BY length(dict),dict,dict_code" , dict_db)
        table_order_dict.to_csv(filename_1+".dict.yaml",header=0,sep='\t',index=False)
        cursor.execute("DROP TABLE IF EXISTS tmp_order" )
    rime_yaml_output(filename_1,filename_2)
#指定工作目录
os.chdir('./output')
#环境变量
sogou_dict_set = os.getenv('SOGOU_DICT',default = 'True') == 'True'
sogou_official = os.getenv('SOGOU_OFFICIAL', default = 'False') == 'True'
sogou_single_file = os.getenv('SOGOU_SINGLE_FILE',default = 'True') == 'True'
sogou_official_total = os.getenv('SOGOU_OFFICIAL_TOTAL',default = 'False') == 'True'
prefix_dict_name = os.getenv('PREFIX_DICT_NAME',default = 'luna_pinyin.')
rime_converter_type = os.getenv('RIME_CONVERTER_TYPE',default = 'pinyin')
rime_opencc = os.getenv('RIME_OPENCC',default = 'False')== 'True'
rime_opencc_config = os.getenv('RIME_OPENCC_CONFIG',default = 's2t.json')
tengxun_freq = os.getenv('TENGXUN_FREQ',default = 'False') == 'True'
basic_dict_set = os.getenv('BASIC_DICT',default = 'True') == 'True'
english_dict_set = os.getenv('ENGLISH_DICT',default = 'True') == 'True'
chinese_character_encoding_set = os.getenv('CHINESE_CHARACTER_ENCODING',default = 'True') == 'True'
english_character_encoding_set = os.getenv('ENGLISH_CHARACTER_ENCODING',default = 'False') == 'True'
corpus_set = os.getenv('CORPUS',default = 'True') == 'True'
googlepinyin_set = os.getenv('GOOGLEPINYIN',default = 'True') == 'True'
thuocl_set = os.getenv('THUOCL',default = 'True') == 'True'
polyphonic_set = os.getenv('POLYPHONIC',default = 'True') == 'True'
order_set = os.getenv('ORDER',default = 'True') == 'True'
len_num_set = os.getenv('LEN_NUM',default = '0')
no_finals_fix_set = os.getenv('NO_FINALS_FIX',default = 'True') == 'True'
#创建表格
dict_db = sqlite3.connect('../dict.db')
cursor = dict_db.cursor()
cursor.execute("DROP TABLE IF EXISTS tmp_1" )
cursor.execute("DROP TABLE IF EXISTS tmp_2" )
cursor.execute("DROP TABLE IF EXISTS tmp_tengxun_freq" )
cursor.execute("DROP TABLE IF EXISTS tmp_basic_dict" )
cursor.execute("DROP TABLE IF EXISTS tmp_english_dict" )
cursor.execute("DROP TABLE IF EXISTS tmp_polyphonic" )
cursor.execute("DROP TABLE IF EXISTS tmp_polyphonic_fix" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_1 (dict TEXT,dict_name TEXT,dict_frequency INTEGER)" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_2 (dict TEXT,dict_frequency INTEGER)" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_tengxun_freq (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_basic_dict (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_english_dict (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_polyphonic (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
cursor.execute("CREATE TABLE IF NOT EXISTS tmp_polyphonic_fix (dict TEXT,dict_code TEXT,dict_frequency INTEGER)" )
#基础词库
if basic_dict_set:
    #谷歌拼音
    if googlepinyin_set:
        cursor.execute("SELECT * FROM googlepinyin " )
        data_googlepinyin = cursor.fetchall()
        for i in data_googlepinyin:
            googlepinyin_nav_name = i[0]
            googlepinyin_dict_table_name = i[1]
            googlepinyin_env_set = os.getenv(googlepinyin_dict_table_name.upper(), default = 'True') == 'True'
            if googlepinyin_env_set:
                cursor.execute("insert into tmp_basic_dict(dict,dict_frequency) select dict,dict_frequency from '%s' GROUP BY dict" %googlepinyin_dict_table_name )
    #清华大学开放中文词库
    if thuocl_set:
        cursor.execute("SELECT * FROM thuocl " )
        data_thuocl = cursor.fetchall()
        for i in data_thuocl:
            thuocl_nav_name = i[0]
            thuocl_dict_table_name = i[1]
            thuocl_env_set = os.getenv(thuocl_dict_table_name.upper(), default = 'True') == 'True'
            if thuocl_env_set:
                cursor.execute("insert into tmp_basic_dict(dict,dict_frequency) select dict,dict_frequency from '%s' GROUP BY dict" %thuocl_dict_table_name )
    #语料库在线
    if corpus_set:
        cursor.execute("SELECT * FROM corpus " )
        data_corpus = cursor.fetchall()
        for i in data_corpus:
            corpus_nav_name = i[0]
            corpus_dict_table_name = i[1]
            corpus_env_set = os.getenv(corpus_dict_table_name.upper(), default = 'True') == 'True'
            if corpus_env_set:
                cursor.execute("insert into tmp_basic_dict(dict,dict_frequency) select dict,dict_frequency from '%s' GROUP BY dict" %corpus_dict_table_name )
    #中文字符编码
    if chinese_character_encoding_set:
        cursor.execute("SELECT * FROM chinese_character_encoding " )
        data_chinese_character_encoding = cursor.fetchall()
        for i in data_chinese_character_encoding:
            chinese_character_encoding_nav_name = i[0]
            chinese_character_encoding_dict_table_name = i[1]
            chinese_character_encoding_env_set = os.getenv(chinese_character_encoding_dict_table_name.upper(), default = 'True') == 'True'
            if chinese_character_encoding_env_set:
                cursor.execute("insert into tmp_basic_dict(dict,dict_frequency) select dict,dict_frequency from '%s' GROUP BY dict" %chinese_character_encoding_dict_table_name )
    if tengxun_freq:
        table_basic_dict = sql.read_sql("SELECT * FROM tmp_basic_dict GROUP BY dict" , dict_db)
    else:
        table_basic_dict = sql.read_sql("SELECT DISTINCT dict FROM tmp_basic_dict" , dict_db)
    filename_1 = prefix_dict_name+'basic_dict'
    filename_2 = '自定义基础词汇'
    conver_file(table_basic_dict,filename_1,filename_2)
#英语词库
if english_dict_set:
    #英语字符
    if english_character_encoding_set:
        cursor.execute("SELECT * FROM english_character_encoding " )
        data_english_character_encoding = cursor.fetchall()
        for i in data_english_character_encoding:
            english_character_encoding_nav_name = i[0]
            english_character_encoding_dict_table_name = i[1]
            english_character_encoding_env_set = os.getenv(english_character_encoding_dict_table_name.upper(), default = 'True') == 'True'
            if english_character_encoding_env_set:
                cursor.execute("insert into tmp_english_dict(dict,dict_code,dict_frequency) select dict,dict_code,dict_frequency from '%s' GROUP BY dict" %english_character_encoding_dict_table_name )
    if tengxun_freq:
        table_english_dict = sql.read_sql("SELECT * FROM tmp_english_dict GROUP BY dict" , dict_db)
    else:
        table_english_dict = sql.read_sql("SELECT dict,dict_code FROM tmp_english_dict GROUP BY dict" , dict_db)
    filename_1 = 'english_dict'
    filename_2 = '自定义英语词汇'
    yaml_dict_name = filename_1+".dict.yaml"
    table_english_dict.to_csv(yaml_dict_name,header=0,sep='\t',index=False,float_format='%.0f')
    if not tengxun_freq:
        file_out = open(yaml_dict_name, 'w',encoding='UTF-8')
        for line in fileinput.input(yaml_dict_name):
            line = line.split()
            file_out.write(line[0]+'	1\n')
        file_out.close()
    rime_yaml_output(filename_1,filename_2)
#搜狗词库
if sogou_dict_set:
    cursor.execute("SELECT * FROM sogou " )
    data = cursor.fetchall()
    if sogou_official_total:
        for i in data:
            sogou_dict_table_name = i[1]
            cursor.execute("insert into tmp_1 select dict,dict_name,dict_frequency from '%s' WHERE dict_name LIKE '%%官方推荐%%'" %sogou_dict_table_name )
    for i in data:
        sogou_nav_name = i[0]
        sogou_dict_table_name = i[1]
        env_set = os.getenv(sogou_dict_table_name.upper(), default = 'True') == 'True'
        if sogou_official and not sogou_single_file:
            filename_1 = prefix_dict_name+'sogou_total_dict.official'
            filename_2 = '官方推荐全部词汇'
            filename_3 = prefix_dict_name+'sogou_total_dict.unofficial'
            filename_4 = '非官方全部词汇'
        elif not sogou_official and not sogou_single_file:
            filename_1 = prefix_dict_name+'sogou_total_dict'
            filename_2 = '全部词汇'
        elif not sogou_official and sogou_single_file:
            filename_1 = prefix_dict_name+sogou_dict_table_name
            filename_2 = sogou_nav_name
        elif sogou_single_file and sogou_official_total and sogou_official:
            filename_1 = prefix_dict_name+sogou_dict_table_name+".unofficial"
            filename_2 = sogou_nav_name
            filename_3 = prefix_dict_name+'sogou_total_dict.official'
            filename_4 = '官方推荐全部词汇'
        else:
            filename_1 = prefix_dict_name+sogou_dict_table_name+".official"
            filename_2 = sogou_nav_name
            filename_3 = prefix_dict_name+sogou_dict_table_name+".unofficial"
        if sogou_single_file:
            sogou_nav_url = i[2]
            if sogou_official:
                if sogou_official_total:
                    if tengxun_freq:
                        table_1 = sql.read_sql( "SELECT a.dict,a.dict_frequency FROM '%s' a  WHERE a.dict NOT IN (SELECT b.dict FROM  tmp_1 b WHERE b.dict_name LIKE '%%官方推荐%%' GROUP BY dict)" %(sogou_dict_table_name), dict_db)
                    else:
                        table_1 = sql.read_sql( "SELECT DISTINCT a.dict FROM '%s' a WHERE a.dict NOT IN (SELECT b.dict FROM  tmp_1 b WHERE b.dict_name LIKE '%%官方推荐%%')" %(sogou_dict_table_name), dict_db)
                else:
                    if env_set:
                        if tengxun_freq:
                            table_1 = sql.read_sql("SELECT dict,dict_frequency FROM '%s'  WHERE dict_name LIKE '%%官方推荐%%' GROUP BY dict" %sogou_dict_table_name, dict_db)
                            table_2 = sql.read_sql( "SELECT  a.dict,a.dict_frequency FROM '%s' a  WHERE a.dict NOT IN (SELECT b.dict FROM '%s' b  WHERE b.dict_name LIKE '%%官方推荐%%') GROUP BY dict" %(sogou_dict_table_name,sogou_dict_table_name), dict_db)
                        else:
                            table_1 = sql.read_sql("SELECT DISTINCT dict FROM '%s' WHERE dict_name LIKE '%%官方推荐%%'" %sogou_dict_table_name, dict_db)
                            table_2 = sql.read_sql( "SELECT DISTINCT a.dict FROM '%s' a WHERE a.dict NOT IN (SELECT b.dict FROM '%s' b  WHERE b.dict_name LIKE '%%官方推荐%%')" %(sogou_dict_table_name,sogou_dict_table_name), dict_db)
            else:
                if env_set:
                    if tengxun_freq:
                        table_1 = sql.read_sql("SELECT dict,dict_frequency FROM '%s' GROUP BY dict" %sogou_dict_table_name, dict_db)
                    else:
                        table_1 = sql.read_sql("SELECT DISTINCT dict FROM '%s'" %sogou_dict_table_name, dict_db)
            if env_set:
                conver_file(table_1,filename_1,filename_2)
                if sogou_official and not sogou_official_total:
                    conver_file(table_2,filename_3,filename_2)
        else:
            sogou_nav_url = 'https://pinyin.sogou.com/dict/cate/index'
            if sogou_official:
                if sogou_official_total:
                    if env_set:
                        cursor.execute("insert into tmp_2 select dict,dict_frequency FROM '%s' GROUP BY dict" %sogou_dict_table_name )
                else:
                    if env_set:
                        cursor.execute("insert into tmp_1 select dict,dict_name,dict_frequency from '%s' WHERE dict_name LIKE '%%官方推荐%%'" %sogou_dict_table_name )
                        cursor.execute("insert into tmp_2 select dict,dict_frequency FROM '%s' GROUP BY dict" %sogou_dict_table_name )
            else:
                if env_set:
                    cursor.execute("insert into tmp_1 select dict,dict_name,dict_frequency from %s" %sogou_dict_table_name )

    if sogou_single_file and sogou_official_total and sogou_official:
            if tengxun_freq:
                table_2 = sql.read_sql("SELECT dict,dict_frequency FROM tmp_1 GROUP BY dict" , dict_db)
            else:
                table_2 = sql.read_sql("SELECT DISTINCT dict FROM tmp_1" , dict_db)
            conver_file(table_2,filename_3,filename_4)
    if not sogou_single_file:
            if tengxun_freq:
                table_1 = sql.read_sql("SELECT dict,dict_frequency FROM tmp_1 GROUP BY dict" , dict_db)
                table_2 = sql.read_sql("SELECT a.dict,a.dict_frequency FROM tmp_2 a  WHERE a.dict NOT IN (SELECT b.dict FROM tmp_1 b  WHERE b.dict_name LIKE '%%官方推荐%%') GROUP BY dict",  dict_db)
            else:
                table_1 = sql.read_sql("SELECT DISTINCT dict FROM tmp_1" , dict_db)
                table_2 = sql.read_sql("SELECT DISTINCT a.dict FROM tmp_2 a WHERE a.dict NOT IN (SELECT b.dict FROM tmp_1 b  WHERE b.dict_name LIKE '%%官方推荐%%')",  dict_db)
            conver_file(table_1,filename_1,filename_2)
            if sogou_official:
                conver_file(table_2,filename_3,filename_4)
#删除表格
cursor.execute("DROP TABLE IF EXISTS tmp_1" )
cursor.execute("DROP TABLE IF EXISTS tmp_2" )
cursor.execute("DROP TABLE IF EXISTS tmp_tengxun_freq" )
cursor.execute("DROP TABLE IF EXISTS tmp_basic_dict" )
cursor.execute("DROP TABLE IF EXISTS tmp_english_dict" )
cursor.execute("DROP TABLE IF EXISTS tmp_polyphonic" )
cursor.execute("DROP TABLE IF EXISTS tmp_polyphonic_fix" )
dict_db.commit()
cursor.execute("VACUUM" )
cursor.close()
dict_db.close()

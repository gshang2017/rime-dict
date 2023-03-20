#!/usr/bin/env python
# coding=utf-8

import os
import requests
import lxml
from bs4 import BeautifulSoup
import sqlite3
import time
import pytz
from datetime import datetime

def download_sogou_url():
    os.chdir('./')
    dict_db = sqlite3.connect('dict.db')
    cursor = dict_db.cursor()
    sql_text_1 = '''CREATE TABLE IF NOT EXISTS status
                (dict_name TEXT,
                dict_url TEXT,
                index_num TEXT,
                dict_download_url TEXT,
                dict_updatetime TEXT,
                dict_table_name TEXT,
                download_status BOOLEAN);'''
    cursor.execute(sql_text_1)
    cursor.execute("SELECT * FROM sogou " )
    data = cursor.fetchall()
    for i in data:
        dict_table_name = i[1]
        index_num = i[3]
        url='https://pinyin.sogou.com/dict/cate/index/' + str(index_num)
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'lxml')
        for select_list_show in soup.find_all("div", {"id": "select_list_show"}):
            order_way_content =  select_list_show.find_all("div", {"class": "order_way_content"})
            order_way_num = order_way_content[1].a.get('href')
        for page in soup.find_all("div", {"id": "dict_page_list"}):
            li = page.find_all('li')
            try:
                page_num = li[-2].text
            except:
                page_num = 1
            #检查是否需要更新文件
            #检查最后一个词库
            url_end_check = 'https://pinyin.sogou.com' + str(order_way_num) + '/' + page_num
            r_end_check = requests.get(url_end_check)
            soup_end_check = BeautifulSoup(r_end_check.text,'lxml')
            #细胞词名称
            detail_title_list_end_check = soup_end_check.find_all("div", {"class": "detail_title"})
            end_num = len(detail_title_list_end_check)
            end_dict_url = detail_title_list_end_check[end_num-1].a.get('href')
            cursor.execute("SELECT dict_url FROM status WHERE dict_url='%s'" %(end_dict_url))
            end_dict_name_len = len(cursor.fetchall())
            #检查第一个词库
            url_first_check = 'https://pinyin.sogou.com' + str(order_way_num) + '/' + '1'
            r_first_check = requests.get(url_first_check)
            soup_first_check = BeautifulSoup(r_first_check.text,'lxml')
            #更新时间
            detail_title_list_first_check = soup_first_check.find_all("div", {"class": "detail_title"})
            first_dict_url = detail_title_list_first_check[0].a.get('href')
            dict_detail_content_list_first_check = soup_first_check.find_all("div", {"class": "dict_detail_content"})
            first_num = len(dict_detail_content_list_first_check)
            show_content_list_first_check = dict_detail_content_list_first_check[0].find_all("div", {"class": "show_content"})
            time_list_first_check = datetime.strptime(show_content_list_first_check[2].string, "%Y-%m-%d %H:%M:%S")
            dict_updatetime_first_check = int(pytz.timezone("Asia/Shanghai").localize(time_list_first_check).timestamp())
            cursor.execute("SELECT dict_url FROM status WHERE dict_url='%s' AND dict_updatetime='%s'"%(first_dict_url,dict_updatetime_first_check))
            first_dict_name_len = len(cursor.fetchall())
            if end_dict_name_len < 1 or first_dict_name_len < 1:
                for j in range(1, int(page_num) + 1):
                    url2 = 'https://pinyin.sogou.com' + str(order_way_num) + '/' + str(j)
                    r2 = requests.get(url2)
                    soup2 = BeautifulSoup(r2.text,'lxml')
                    #细胞词名称
                    detail_title_list = soup2.find_all("div", {"class": "detail_title"})
                    for k in range(0,  len(detail_title_list)):
                        dict_name = detail_title_list[k].string
                        dict_url = detail_title_list[k].a.get('href')
                        index_num = dict_url.replace('/dict/detail/index/','')
                        #下载网址
                        dict_dl_btn_list = soup2.find_all("div", {"class": "dict_dl_btn"})
                        dict_download_url = dict_dl_btn_list[k].a.get('href')
                        #更新时间
                        dict_detail_content_list = soup2.find_all("div", {"class": "dict_detail_content"})
                        show_content_list = dict_detail_content_list[k].find_all("div", {"class": "show_content"})
                        time_list = datetime.strptime(show_content_list[2].string, "%Y-%m-%d %H:%M:%S")
                        dict_updatetime = int(pytz.timezone("Asia/Shanghai").localize(time_list).timestamp())
                        cursor.execute("CREATE TABLE IF NOT EXISTS %s (dict_name TEXT,index_num TEXT,dict TEXT)" %dict_table_name)
                        cursor.execute("SELECT index_num FROM status WHERE index_num='%s'" %index_num)
                        index_num_len_1 = len(cursor.fetchall())
                        if index_num_len_1 > 0:
                            cursor.execute("SELECT index_num FROM status WHERE index_num='%s' AND dict_updatetime='%s'"%(index_num,dict_updatetime))
                            index_num_len_2 = len(cursor.fetchall())
                        if index_num_len_1 == 0:
                            sql_text_3 = "INSERT INTO status VALUES(?,?,?,?,?,?,false)"
                            cursor.execute(sql_text_3,(dict_name,dict_url,index_num,dict_download_url,dict_updatetime,dict_table_name))
                        elif index_num_len_1 > 0 and  index_num_len_2 == 0:
                            cursor.execute("UPDATE status SET dict_name='%s',dict_url='%s',index_num='%s',dict_download_url='%s',dict_updatetime='%s',dict_table_name='%s', download_status=0 WHERE index_num='%s'" %(dict_name,dict_url,index_num , dict_download_url, dict_updatetime,dict_table_name, index_num))
                        elif end_dict_name_len > 0 and index_num_len_1 > 0 and  index_num_len_2 > 0:
                            break
                        dict_db.commit()
    cursor.close()
    dict_db.close()

if __name__ == '__main__':

    download_sogou_url()

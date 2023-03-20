#!/usr/bin/env python
# coding=utf-8

#城市信息 City Information                  https://pinyin.sogou.com/dict/cate/index/167
#自然科学 Natural Science                   https://pinyin.sogou.com/dict/cate/index/1
#社会科学 Social Sciences                   https://pinyin.sogou.com/dict/cate/index/76
#工程应用 Engineering Application           https://pinyin.sogou.com/dict/cate/index/96
#农业渔畜 Agriculture and Fishing Livestock https://pinyin.sogou.com/dict/cate/index/127
#医学医药 Medicine and Medicine             https://pinyin.sogou.com/dict/cate/index/132
#电子游戏 Video Games                       https://pinyin.sogou.com/dict/cate/index/436
#艺术设计 Art Design                        https://pinyin.sogou.com/dict/cate/index/154
#生活百科 Life Encyclopedia                 https://pinyin.sogou.com/dict/cate/index/389
#运动休闲 Sports and leisure                https://pinyin.sogou.com/dict/cate/index/367
#人文科学 Humanities                        https://pinyin.sogou.com/dict/cate/index/31
#娱乐休闲 Entertainment and leisure         https://pinyin.sogou.com/dict/cate/index/403

import os
import requests
import lxml
from bs4 import BeautifulSoup
import sqlite3

def download_sogou_nav():
    os.chdir('./')
    dict_db = sqlite3.connect('dict.db')
    cursor = dict_db.cursor()
    sql_text_1 = '''CREATE TABLE IF NOT EXISTS sogou
               (sogou_nav_name TEXT,
                sogou_dict_table_name TEXT,
                sogou_nav_url TEXT,
                sogou_nav_index_num TEXT);'''
    cursor.execute(sql_text_1)
    url='https://pinyin.sogou.com/dict/cate/index/1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for page in soup.find_all("div", {"id": "dict_nav_list"}):
        for li in page.find_all('li'):
            sogou_nav_url = li.a.get('href')
            sogou_nav_index_num = sogou_nav_url.replace('/dict/cate/index/','')
            if sogou_nav_index_num == '167':
                sogou_nav_name='城市信息'
                sogou_dict_table_name='sogou_city_information'
            elif sogou_nav_index_num == '1':
                sogou_nav_name='自然科学'
                sogou_dict_table_name='sogou_natural_science'
            elif sogou_nav_index_num == '76':
                sogou_nav_name='社会科学'
                sogou_dict_table_name='sogou_social_sciences'
            elif sogou_nav_index_num == '96':
                sogou_nav_name='工程应用'
                sogou_dict_table_name='sogou_engineering_application'
            elif sogou_nav_index_num == '127':
                sogou_nav_name='农业渔畜'
                sogou_dict_table_name='sogou_agriculture_and_fishing_livestock'
            elif sogou_nav_index_num == '132':
                sogou_nav_name='医学医药'
                sogou_dict_table_name='sogou_medicine_and_medicine'
            elif sogou_nav_index_num == '436':
                sogou_nav_name='电子游戏'
                sogou_dict_table_name='sogou_video_games'
            elif sogou_nav_index_num == '154':
                sogou_nav_name='艺术设计'
                sogou_dict_table_name='sogou_art_design'
            elif sogou_nav_index_num == '389':
                sogou_nav_name='生活百科'
                sogou_dict_table_name='sogou_life_encyclopedia'
            elif sogou_nav_index_num == '367':
                sogou_nav_name='运动休闲'
                sogou_dict_table_name='sogou_sports_and_leisure'
            elif sogou_nav_index_num == '31':
                sogou_nav_name='人文科学'
                sogou_dict_table_name='sogou_humanities'
            elif sogou_nav_index_num == '403':
                sogou_nav_name='娱乐休闲'
                sogou_dict_table_name='sogou_entertainment_and_leisure'
            cursor.execute("select sogou_nav_index_num from sogou where sogou_nav_index_num='%s'" %sogou_nav_index_num)
            num = len(cursor.fetchall())
            if num == 0:
                sql_text_2 = "insert into sogou values(?,?,?,?)"
                cursor.execute(sql_text_2,(sogou_nav_name,sogou_dict_table_name,sogou_nav_url,sogou_nav_index_num))
            dict_db.commit()
    cursor.close()
    dict_db.close()

if __name__ == '__main__':

    download_sogou_nav()

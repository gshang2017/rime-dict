#! /usr/bin/with-contenv bash

#删除rime_dict目录下output文件夹
if [ -d /usr/local/rime_dict/output ]; then
  rm -rf /usr/local/rime_dict/output/
fi

#更新rime_dict数据库
if [ "$RIME_DICT_UPDATE" == "true" ]; then
  TAG_NAME=$(curl --silent https://api.github.com/repos/gshang2017/rime-dict/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
  if [ "$(cat /usr/local/rime_dict/version.txt)" != "$TAG_NAME" ]; then
    wget -P /tmp https://github.com/gshang2017/rime-dict/releases/download/$TAG_NAME/dict.tar.gz
    tar -zxf /tmp/dict.tar.gz -C /usr/local/rime_dict/
    rm /usr/local/rime_dict/version.txt
    echo $TAG_NAME > /usr/local/rime_dict/version.txt
    rm -rf /tmp/*
  fi
fi

#更新搜狗词库数据
if [ "$SOGOU_DICT_UPDATE" == "true" ]; then
  cd /usr/local/rime_dict/
  python3 sogou_dict.py
  python3 dict_frequency_ai.py
fi

#检查环境变量更改
if [ ! -f "/usr/local/rime_dict/env_set.txt" ]; then
  env > /usr/local/rime_dict/env_set.txt
fi
env_name[1]=PREFIX_DICT_NAME
env_name[2]=RIME_CONVERTER_TYPE
env_name[3]=RIME_OPENCC
env_name[4]=RIME_OPENCC_CONFIG
env_name[5]=TENGXUN_FREQ
env_name[6]=POLYPHONIC
env_name[7]=ORDER
env_name[8]=LEN_NUM
env_name[9]=NO_FINALS_FIX
env_name[10]=SOGOU_DICT
env_name[11]=SOGOU_OFFICIAL
env_name[12]=SOGOU_SINGLE_FILE
env_name[13]=SOGOU_OFFICIAL_TOTAL
env_name[14]=SOGOU_ENGINEERING_APPLICATION
env_name[15]=SOGOU_AGRICULTURE_AND_FISHING_LIVESTOCK
env_name[16]=SOGOU_SOCIAL_SCIENCES
env_name[17]=SOGOU_NATURAL_SCIENCE
env_name[18]=SOGOU_CITY_INFORMATION
env_name[19]=SOGOU_ENTERTAINMENT_AND_LEISURE
env_name[20]=SOGOU_HUMANITIES
env_name[21]=SOGOU_SPORTS_AND_LEISURE
env_name[22]=SOGOU_LIFE_ENCYCLOPEDIA
env_name[23]=SOGOU_ART_DESIGN
env_name[24]=SOGOU_VIDEO_GAMES
env_name[25]=SOGOU_MEDICINE_AND_MEDICINE
env_name[26]=BASIC_DICT
env_name[27]=CHINESE_CHARACTER_ENCODING
env_name[28]=CHINESE_CHARACTER_ENCODING_BIG5
env_name[29]=CHINESE_CHARACTER_ENCODING_BIG5_CHANGYONG
env_name[30]=CHINESE_CHARACTER_ENCODING_GB2312
env_name[31]=CHINESE_CHARACTER_ENCODING_GBK
env_name[32]=CORPUS
env_name[33]=CORPUS_CHANGYONG
env_name[34]=CORPUS_GUIFAN
env_name[35]=CORPUS_PHRASE
env_name[36]=CORPUS_SINGLE
env_name[37]=CORPUS_TONGYONG
env_name[38]=GOOGLEPINYIN
env_name[39]=GOOGLEPINYIN_PHRASE
env_name[40]=GOOGLEPINYIN_SINGLE
env_name[41]=THUOCL
env_name[42]=ENGLISH_DICT
env_name[43]=ENGLISH_CHARACTER_ENCODING
env_name[44]=ENGLISH_CHARACTER_ENCODING_COCA
env_name[45]=NON_TENGXUN_DEL
env_name[46]=TOTAL_OFFICIAL_NON_TENGXUN_DEL
env_name[47]=WIKI_DICT
env_name[48]=LETTERED_WORD_DICT
env_name[49]=LETTERED_WORD_NON_DELIMITER
env_name[50]=IMEWLCONVERTER
env_name[51]=CHAIZI_DICT
ENV_CHANGE=false
for i in ${env_name[*]}; do
  if [ "$(cat '/usr/local/rime_dict/env_set.txt'|grep $i)" != "$(env|grep $i)" ]; then
    ENV_CHANGE=true
    env > /usr/local/rime_dict/env_set.txt
    break
  fi
done

#生成rime词库
if [ ! -f "/config/version.txt" ] || [ "$(cat /usr/local/rime_dict/version.txt)" != "$(cat /config/version.txt)" ] || [ "$ENV_CHANGE" == "true"  ] ; then
  cd /usr/local/rime_dict/
  python3 rime_dict.py
  cp -rf /usr/local/rime_dict/output/* /output/
  #检查version.txt文件
  if [ ! -f "/config/version.txt" ] || [ "$(cat /usr/local/rime_dict/version.txt)" != "$(cat /config/version.txt)" ]; then
    cp -rf /usr/local/rime_dict/version.txt /config
  fi
fi

#设定rime_dict_update更新任务
if [ "$RIME_DICT_UPDATE_AUTO" == "true" ]; then
  if [ `grep  -c rime_dict_update.sh /var/spool/cron/crontabs/root` -eq 0 ]; then
    echo "0       0      *       *       *       /usr/local/rime_update/rime_dict_update.sh" >> /var/spool/cron/crontabs/root
    echo rime_dict_update更新任务已设定。
  else
    echo rime_dict_update更新任务已存在。
  fi
fi

#设置时区
ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone

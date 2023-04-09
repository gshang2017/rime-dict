## RIME输入法自用词库：

### 简介

* 自动生成带词频的rime输入法(拼音)使用文件(包含英语，基础，搜狗词库)。词频基于腾讯AI向量词库逆序生成。

### GitHub:

[https://github.com/gshang2017/rime-dict](https://github.com/gshang2017/rime-dict)

### 预生成文件明细

#### 下载地址

[https://github.com/gshang2017/rime-dict/releases](https://github.com/gshang2017/rime-dict/releases)

* rime-dict.txt.tar.gz

|文件名称|说明|
|:-|:-|
| `english_dict.dict.yaml` |coca前60000英语词库|
| `luna_pinyin_simp.basic_dict.dict.yaml` |包含谷歌拼音,清华大学开放中文词库,语料库在线,big5,gb2312,gbk|
| `luna_pinyin_simp.sogou_total_dict.official.dict.yaml` |包含搜狗官方所有类推荐词库|
| `luna_pinyin_simp.sogou_agriculture_and_fishing_livestock.unofficial.dict.yaml` |搜狗农业渔畜非官方推荐词库|
| `luna_pinyin_simp.sogou_art_design.unofficial.dict.yaml` |搜狗艺术设计非官方推荐词库|
| `luna_pinyin_simp.sogou_city_information.unofficial.dict.yaml` |搜狗城市信息非官方推荐词库|
| `luna_pinyin_simp.sogou_engineering_application.unofficial.dict.yaml` |搜狗工程应用非官方推荐词库|
| `luna_pinyin_simp.sogou_entertainment_and_leisure.unofficial.dict.yaml` |搜狗娱乐休闲非官方推荐词库|
| `luna_pinyin_simp.sogou_humanities.unofficial.dict.yaml` |搜狗人文科学非官方推荐词库|
| `luna_pinyin_simp.sogou_life_encyclopedia.unofficial.dict.yaml` |搜狗生活百科非官方推荐词库|
| `luna_pinyin_simp.sogou_medicine_and_medicine.unofficial.dict.yaml` |搜狗医学医药非官方推荐词库|
| `luna_pinyin_simp.sogou_natural_science.unofficial.dict.yaml` |搜狗自然科学非官方推荐词库|
| `luna_pinyin_simp.sogou_social_sciences.unofficial.dict.yaml` |搜狗社会科学非官方推荐词库|
| `luna_pinyin_simp.sogou_sports_and_leisure.unofficial.dict.yaml` |搜狗运动休闲非官方推荐词库|
| `luna_pinyin_simp.sogou_video_games.unofficial.dict.yaml` |搜狗电子游戏非官方推荐词库|

* rime-dict.txt.tar.gz

|文件名称|说明|
|:-|:-|
| `polyphonic_dict.txt` |多音字|
| `luna_pinyin_simp.basic_dict.txt` |包含谷歌拼音,清华大学开放中文词库,语料库在线,big5,gb2312,gbk|
| `luna_pinyin_simp.sogou_total_dict.official.txt` |包含搜狗官方所有类推荐词库|
| `luna_pinyin_simp.sogou_agriculture_and_fishing_livestock.unofficial.txt` |搜狗农业渔畜非官方推荐词库|
| `luna_pinyin_simp.sogou_art_design.unofficial.txt` |搜狗艺术设计非官方推荐词库|
| `luna_pinyin_simp.sogou_city_information.unofficial.txt` |搜狗城市信息非官方推荐词库|
| `luna_pinyin_simp.sogou_engineering_application.unofficial.txt` |搜狗工程应用非官方推荐词库|
| `luna_pinyin_simp.sogou_entertainment_and_leisure.unofficial.txt` |搜狗娱乐休闲非官方推荐词库|
| `luna_pinyin_simp.sogou_humanities.unofficial.txt` |搜狗人文科学非官方推荐词库|
| `luna_pinyin_simp.sogou_life_encyclopedia.unofficial.txt` |搜狗生活百科非官方推荐词库|
| `luna_pinyin_simp.sogou_medicine_and_medicine.unofficial.txt` |搜狗医学医药非官方推荐词库|
| `luna_pinyin_simp.sogou_natural_science.unofficial.txt` |搜狗自然科学非官方推荐词库|
| `luna_pinyin_simp.sogou_social_sciences.unofficial.txt` |搜狗社会科学非官方推荐词库|
| `luna_pinyin_simp.sogou_sports_and_leisure.unofficial.txt` |搜狗运动休闲非官方推荐词库|
| `luna_pinyin_simp.sogou_video_games.unofficial.txt` |搜狗电子游戏非官方推荐词库|

### 用docker生成

#### 版本：

|名称|版本|说明|
|:-|:-|:-|
|rime-dict|latest|amd64;arm64v8;arm32v7|

#### docker命令行设置：

1. 下载镜像

    |镜像源|命令|
    |:-|:-|
    |DockerHub|docker pull johngong/rime-dict:latest|
    |GitHub|docker pull ghcr.io/gshang2017/rime-dict:latest|

2. 创建rime-dict容器

        docker create  \
           --name=rime-dict  \
           -v /dict位置:/output  \
           -v /rime词库版本存储位置:/config  \
           --restart unless-stopped  \
           johngong/rime-dict:latest

3. 运行

       docker start rime-dict

4. 停止

       docker stop rime-dict

5. 删除容器

       docker rm rime-dict

6. 删除镜像

       docker image rm johngong/rime-dict:latest

#### 变量:

|参数|说明|
|:-|:-|
| `--name=rime-dict` |容器名|
| `-v /dict位置:/output` |生成新词位置|
| `-v /rime词库版本存储位置:/config` |rime词库版本存储位置|
| `-e TZ=Asia/Shanghai` |系统时区设置,默认为Asia/Shanghai|
| `-e RIME_DICT_UPDATE=true` |(true\|false)rime词库更新,默认开启|
| `-e SOGOU_DICT_UPDATE=false` |搜狗词库更新(时间太长建议不更新)|
| `-e RIME_DICT_UPDATE_AUTO=false` |自动更新rime词库|
| `-e PREFIX_DICT_NAME=luna_pinyin.` |词库前缀|
| `-e RIME_CONVERTER_TYPE=pinyin` |词库转换(默认pinyin)|
| `-e RIME_OPENCC=False` |opencc设定|
| `-e RIME_OPENCC_CONFIG=s2t.json` |opencc配置|
| `-e TENGXUN_FREQ=True` |(True\|False)腾讯词频,默认开启|
| `-e POLYPHONIC=True` |多音字|
| `-e ORDER=True` |对词库排序|
| `-e LEN_NUM=7` |搜狗词库限制长度|
| `-e NO_FINALS_FIX=True` |无韵母多音字修正|
| `-e SOGOU_DICT=True` |搜狗词库(开启才能配置其它搜狗词库)|
| `-e SOGOU_OFFICIAL=True` |搜狗官方推荐词库|
| `-e SOGOU_SINGLE_FILE=True` |单个输出搜狗词库文件|
| `-e SOGOU_OFFICIAL_TOTAL=True` |合并输出搜狗官方推荐词库|
| `-e SOGOU_ENGINEERING_APPLICATION=True` |搜狗工程应用词库|
| `-e SOGOU_AGRICULTURE_AND_FISHING_LIVESTOCK=True` |搜狗农业渔畜词库|
| `-e SOGOU_SOCIAL_SCIENCES=True` |搜狗社会科学词库|
| `-e SOGOU_NATURAL_SCIENCE=True` |搜狗自然科学词库词库|
| `-e SOGOU_CITY_INFORMATION=True` |搜狗城市信息词库|
| `-e SOGOU_ENTERTAINMENT_AND_LEISURE=True` |搜狗娱乐休闲词库|
| `-e SOGOU_HUMANITIES=True` |搜狗人文科学词库|
| `-e SOGOU_SPORTS_AND_LEISURE=True` |搜狗运动休闲词库|
| `-e SOGOU_LIFE_ENCYCLOPEDIA=True` |搜狗生活百科词库|
| `-e SOGOU_ART_DESIGN=True` |搜狗艺术设计词库|
| `-e SOGOU_VIDEO_GAMES=True` |搜狗电子游戏词库|
| `-e SOGOU_MEDICINE_AND_MEDICINE=True` |搜狗医学医药词库|
| `-e BASIC_DICT=True` |基础词库(开启才能配置除搜狗以外中文词库)|
| `-e CHINESE_CHARACTER_ENCODING=True` |中文编码词库(开启才能配置其它中文编码词库)|
| `-e CHINESE_CHARACTER_ENCODING_BIG5=True` |中文编码BIG5词库|
| `-e CHINESE_CHARACTER_ENCODING_BIG5_CHANGYONG=True` |中文编码BIG5常用词库|
| `-e CHINESE_CHARACTER_ENCODING_GB2312=True` |中文编码GB2312词库|
| `-e CHINESE_CHARACTER_ENCODING_GBK=True` |中文编码GBK词库|
| `-e CORPUS=True` |语料库在线(开启才能配置其它语料库在线词库)|
| `-e CORPUS_CHANGYONG=True` |语料库在线常用|
| `-e CORPUS_GUIFAN=True` |语料库在线规范|
| `-e CORPUS_PHRASE=True` |语料库在线短语|
| `-e CORPUS_SINGLE=True` |语料库在线单字|
| `-e CORPUS_TONGYONG=True` |语料库在线通用|
| `-e GOOGLEPINYIN=True` |谷歌拼音(开启才能配置其它谷歌拼音词库)|
| `-e GOOGLEPINYIN_PHRASE=True` |谷歌拼音短语|
| `-e GOOGLEPINYIN_SINGLE=True` |谷歌拼音单字|
| `-e THUOCL=True` |清华大学开放中文词库|
| `-e ENGLISH_DICT=False` |英语词库(开启才能配置其它英语词库)|
| `-e ENGLISH_CHARACTER_ENCODING=False` |英文编码词库(开启才能配置其它英文编码词库)|
| `-e ENGLISH_CHARACTER_ENCODING_COCA=True` |英文编码COCA词库|

#### 群晖docker设置：

1. 卷

|参数|说明|
|:-|:-|
| `本地文件夹1:/output` |生成新词位置|
| `本地文件夹2:/config` |rime词库版本存储位置|

2. 环境变量：

|参数|说明|
|:-|:-|
| `TZ=Asia/Shanghai` |系统时区设置,默认为Asia/Shanghai|
| `RIME_DICT_UPDATE=true` |(true\|false)rime词库更新,默认开启|
| `SOGOU_DICT_UPDATE=false` |搜狗词库更新(时间太长建议不更新)|
| `RIME_DICT_UPDATE_AUTO=false` |自动更新rime词库|
| `PREFIX_DICT_NAME=luna_pinyin.` |词库前缀|
| `RIME_CONVERTER_TYPE=pinyin` |词库转换(默认pinyin)|
| `RIME_OPENCC=False` |opencc设定|
| `RIME_OPENCC_CONFIG=s2t.json` |opencc配置|
| `TENGXUN_FREQ=True` |(True\|False)腾讯词频,默认开启|
| `POLYPHONIC=True` |多音字|
| `ORDER=True` |对词库排序|
| `LEN_NUM=7` |搜狗词库限制长度|
| `NO_FINALS_FIX=True` |无韵母多音字修正|
| `SOGOU_DICT=True` |搜狗词库(开启才能配置其它搜狗词库)|
| `SOGOU_OFFICIAL=True` |搜狗官方推荐词库|
| `SOGOU_SINGLE_FILE=True` |单个输出搜狗词库文件|
| `SOGOU_OFFICIAL_TOTAL=True` |合并输出搜狗官方推荐词库|
| `SOGOU_ENGINEERING_APPLICATION=True` |搜狗工程应用词库|
| `SOGOU_AGRICULTURE_AND_FISHING_LIVESTOCK=True` |搜狗农业渔畜词库|
| `SOGOU_SOCIAL_SCIENCES=True` |搜狗社会科学词库|
| `SOGOU_NATURAL_SCIENCE=True` |搜狗自然科学词库词库|
| `SOGOU_CITY_INFORMATION=True` |搜狗城市信息词库|
| `SOGOU_ENTERTAINMENT_AND_LEISURE=True` |搜狗娱乐休闲词库|
| `SOGOU_HUMANITIES=True` |搜狗人文科学词库|
| `SOGOU_SPORTS_AND_LEISURE=True` |搜狗运动休闲词库|
| `SOGOU_LIFE_ENCYCLOPEDIA=True` |搜狗生活百科词库|
| `SOGOU_ART_DESIGN=True` |搜狗艺术设计词库|
| `SOGOU_VIDEO_GAMES=True` |搜狗电子游戏词库|
| `SOGOU_MEDICINE_AND_MEDICINE=True` |搜狗医学医药词库|
| `BASIC_DICT=True` |基础词库(开启才能配置除搜狗以外中文词库)|
| `CHINESE_CHARACTER_ENCODING=True` |中文编码词库(开启才能配置其它中文编码词库)|
| `CHINESE_CHARACTER_ENCODING_BIG5=True` |中文编码BIG5词库|
| `CHINESE_CHARACTER_ENCODING_BIG5_CHANGYONG=True` |中文编码BIG5常用词库|
| `CHINESE_CHARACTER_ENCODING_GB2312=True` |中文编码GB2312词库|
| `CHINESE_CHARACTER_ENCODING_GBK=True` |中文编码GBK词库|
| `CORPUS=True` |语料库在线(开启才能配置其它语料库在线词库)|
| `CORPUS_CHANGYONG=True` |语料库在线常用|
| `CORPUS_GUIFAN=True` |语料库在线规范|
| `CORPUS_PHRASE=True` |语料库在线短语|
| `CORPUS_SINGLE=True` |语料库在线单字|
| `CORPUS_TONGYONG=True` |语料库在线通用|
| `GOOGLEPINYIN=True` |谷歌拼音(开启才能配置其它谷歌拼音词库)|
| `GOOGLEPINYIN_PHRASE=True` |谷歌拼音短语|
| `GOOGLEPINYIN_SINGLE=True` |谷歌拼音单字|
| `THUOCL=True` |清华大学开放中文词库|
| `ENGLISH_DICT=False` |英语词库(开启才能配置其它英语词库)|
| `ENGLISH_CHARACTER_ENCODING=False` |英文编码词库(开启才能配置其它英文编码词库)|
| `ENGLISH_CHARACTER_ENCODING_COCA=True` |英文编码COCA词库|

### 用命令行生成（ubuntu-20.04）

1.安装下载依赖

    sudo apt-get update
    sudo apt install -y git wget

2.下载代码

    git clone --depth 1 https://github.com/gshang2017/rime-dict.git rime-dict

3.进入rime-dict目录

    cd rime-dict

4.下载修改版imewlconverter

    wget https://github.com/gshang2017/rime-dict/releases/download/2023.03.20/v3.0.0_imewlconverter_Linux_Mac.tar.gz
    mkdir -p imewlconverter
    tar -zxf v3.0.0_imewlconverter_Linux_Mac.tar.gz -C imewlconverter

5.下载rime-dict数据库

    wget https://github.com/gshang2017/rime-dict/releases/download/2023.03.20/dict.tar.gz
    tar -zxf dict.tar.gz

6.安装rime-dict依赖

    sudo apt install python3-pip
    sudo pip install --upgrade setuptools==57.5.0
    sudo pip install -r requirements.txt
    sudo apt install -y opencc
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
    sudo dpkg -i packages-microsoft-prod.deb
    rm packages-microsoft-prod.deb
    sudo apt-get update
    sudo apt install -y dotnet-sdk-6.0

7.更新搜狗词库及词频（可选，因更新时间太长）

    python3 sogou_dict.py
    python3 dict_frequency_ai.py

8.配置环境变量（参考docker配置）

    export SOGOU_OFFICIAL=True
    export SOGOU_SINGLE_FILE=True
    export SOGOU_OFFICIAL_TOTAL=True
    export TENGXUN_FREQ=True
    export ENGLISH_CHARACTER_ENCODING=True
    export LEN_NUM=7
    export PREFIX_DICT_NAME=luna_pinyin_simp.

9.输出输入法文件（rime-dict/output）

    python3 rime_dict.py

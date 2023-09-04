## RIME输入法自用词库：

### 简介

* 自动生成带词频的rime输入法(拼音)使用文件(包含英语，基础，维基，搜狗等词库)。词频基于腾讯AI向量词库逆序生成。

### GitHub:

[https://github.com/gshang2017/rime-dict](https://github.com/gshang2017/rime-dict)

### 预生成文件明细

#### 下载地址

[https://github.com/gshang2017/rime-dict/releases](https://github.com/gshang2017/rime-dict/releases)

* rime-dict.txt.tar.gz（原始文件）及rime-dict.yaml.tar.gz（词库文件）
* non-tengxun版为自用词库仅含有腾讯词频的词(搜狗推荐词库除外)
* 搜狗流行词库详见： [https://github.com/gshang2017/docker/tree/master/rime-sogou](https://github.com/gshang2017/docker/tree/master/rime-sogou)

|文件名称|说明|
|:-|:-|
| `polyphonic_dict` |多音字(仅txt)|
| `basic_dict` |包含谷歌拼音,清华大学开放中文词库,语料库在线,big5,gb2312,gbk|
| `sogou_total_dict.official` |包含搜狗官方所有类推荐词库|
| `sogou_total_dict.unofficial` |包含搜狗非官方推荐所有类词库|
| `sogou_agriculture_and_fishing_livestock.unofficial` |搜狗农业渔畜非官方推荐词库|
| `sogou_art_design.unofficial` |搜狗艺术设计非官方推荐词库|
| `sogou_city_information.unofficial` |搜狗城市信息非官方推荐词库|
| `sogou_engineering_application.unofficial` |搜狗工程应用非官方推荐词库|
| `sogou_entertainment_and_leisure.unofficial` |搜狗娱乐休闲非官方推荐词库|
| `sogou_humanities.unofficial` |搜狗人文科学非官方推荐词库|
| `sogou_life_encyclopedia.unofficial` |搜狗生活百科非官方推荐词库|
| `sogou_medicine_and_medicine.unofficial` |搜狗医学医药非官方推荐词库|
| `sogou_natural_science.unofficial` |搜狗自然科学非官方推荐词库|
| `sogou_social_sciences.unofficial` |搜狗社会科学非官方推荐词库|
| `sogou_sports_and_leisure.unofficial` |搜狗运动休闲非官方推荐词库|
| `sogou_video_games.unofficial` |搜狗电子游戏非官方推荐词库|
| `wiki_dict` |维基百科词库|
| `chaizi_dict` |拆字词库|
| `lettered_word_dict` |字母词词库|

### 用docker生成

* 详见：[https://github.com/gshang2017/rime-dict/tree/main/docker](https://github.com/gshang2017/rime-dict/tree/main/docker "https://github.com/gshang2017/rime-dict/tree/main/docker")

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

8.配置环境变量（参数详见docker设置：[https://github.com/gshang2017/rime-dict/tree/main/docker](https://github.com/gshang2017/rime-dict/tree/main/docker "https://github.com/gshang2017/rime-dict/tree/main/docker")）

    export SOGOU_OFFICIAL=True
    export SOGOU_SINGLE_FILE=True    
    export SOGOU_OFFICIAL_TOTAL=True
    export TENGXUN_FREQ=True
    export ENGLISH_DICT=True
    export ENGLISH_CHARACTER_ENCODING=True
    export LETTERED_WORD_DICT=True
    export WIKI_DICT=True
    export CHAIZI_DICT=True
    export LEN_NUM=7
    export PREFIX_DICT_NAME=luna_pinyin_simp.

9.输出输入法文件（rime-dict/output）

    python3 rime_dict.py

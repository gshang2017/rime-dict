## RIME输入法自用词库：

### 简介

* 自动生成带词频的rime输入法(拼音)使用文件(包含英语，基础，维基，搜狗等词库)。词频基于腾讯AI向量词库逆序生成。

### GitHub:

[https://github.com/gshang2017/rime-dict](https://github.com/gshang2017/rime-dict)

### 版本：

|名称|版本|说明|
|:-|:-|:-|
|rime-dict|latest|amd64;arm64v8;arm32v7|

### docker命令行设置：

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

### 变量:

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
| `-e NON_TENGXUN_DEL=False` |设定刪除无腾讯词频的词,默认关闭|
| `-e TOTAL_OFFICIAL_NON_TENGXUN_DEL=False` |设定刪除搜狗官方推荐词库的无腾讯词频的词,默认关闭|
| `-e POLYPHONIC=True` |多音字|
| `-e ORDER=True` |对词库排序|
| `-e LEN_NUM=7` |搜狗词库限制长度|
| `-e NO_FINALS_FIX=True` |无韵母多音字修正|
| `-e IMEWLCONVERTER=False` |imewlconverter转换开关,关闭后为pypinyin转换,默认关闭|
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
| `-e WIKI_DICT=False` |维基百科|
| `-e LETTERED_WORD_DICT=False` |字母词|
| `-e LETTERED_WORD_NON_DELIMITER=False` |无分隔符的字母词(开启去掉带分隔符的字母词)|
| `-e CHAIZI_DICT=False` |拆字词库|
| `-e ENGLISH_DICT=False` |英语词库(开启才能配置其它英语词库)|
| `-e ENGLISH_CHARACTER_ENCODING=False` |英文编码词库(开启才能配置其它英文编码词库)|
| `-e ENGLISH_CHARACTER_ENCODING_COCA=True` |英文编码COCA词库|

### 群晖docker设置：

1. 卷

|参数|说明|
|:-|:-|
| `本地文件夹1:/output` |生成新词位置|
| `本地文件夹2:/config` |rime词库版本存储位置|

2. 环境变量：

|参数|说明|
|:-|:-|
| `详见前面变量参数中-e` |详见前面变量说明|

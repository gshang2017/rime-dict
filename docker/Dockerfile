FROM mcr.microsoft.com/dotnet/runtime:6.0-alpine3.17

ARG S6_VER=3.1.5.0

ENV TZ=Asia/Shanghai
ENV SOGOU_DICT_UPDATE=false
ENV RIME_DICT_UPDATE=true
ENV RIME_DICT_UPDATE_AUTO=false
ENV PREFIX_DICT_NAME=luna_pinyin_simp.
ENV RIME_CONVERTER_TYPE=pinyin
ENV RIME_OPENCC=False
ENV RIME_OPENCC_CONFIG=s2t.json
ENV TENGXUN_FREQ=True
ENV NON_TENGXUN_DEL=False
ENV TOTAL_OFFICIAL_NON_TENGXUN_DEL=False
ENV POLYPHONIC=True
ENV ORDER=True
ENV LEN_NUM=7
ENV NO_FINALS_FIX=True
ENV IMEWLCONVERTER=False
ENV SOGOU_DICT=True
ENV SOGOU_OFFICIAL=True
ENV SOGOU_SINGLE_FILE=True
ENV SOGOU_OFFICIAL_TOTAL=True
ENV SOGOU_ENGINEERING_APPLICATION=True
ENV SOGOU_AGRICULTURE_AND_FISHING_LIVESTOCK=True
ENV SOGOU_SOCIAL_SCIENCES=True
ENV SOGOU_NATURAL_SCIENCE=True
ENV SOGOU_CITY_INFORMATION=True
ENV SOGOU_ENTERTAINMENT_AND_LEISURE=True
ENV SOGOU_HUMANITIES=True
ENV SOGOU_SPORTS_AND_LEISURE=True
ENV SOGOU_LIFE_ENCYCLOPEDIA=True
ENV SOGOU_ART_DESIGN=True
ENV SOGOU_VIDEO_GAMES=True
ENV SOGOU_MEDICINE_AND_MEDICINE=True
ENV BASIC_DICT=True
ENV CHINESE_CHARACTER_ENCODING=True
ENV CHINESE_CHARACTER_ENCODING_BIG5=True
ENV CHINESE_CHARACTER_ENCODING_BIG5_CHANGYONG=True
ENV CHINESE_CHARACTER_ENCODING_GB2312=True
ENV CHINESE_CHARACTER_ENCODING_GBK=True
ENV CORPUS=True
ENV CORPUS_CHANGYONG=True
ENV CORPUS_GUIFAN=True
ENV CORPUS_PHRASE=True
ENV CORPUS_SINGLE=True
ENV CORPUS_TONGYONG=True
ENV GOOGLEPINYIN=True
ENV GOOGLEPINYIN_PHRASE=True
ENV GOOGLEPINYIN_SINGLE=True
ENV THUOCL=True
ENV WIKI_DICT=False
ENV LETTERED_WORD_DICT=False
ENV LETTERED_WORD_NON_DELIMITER=False
ENV CHAIZI_DICT=False
ENV ENGLISH_DICT=False
ENV ENGLISH_CHARACTER_ENCODING=False
ENV ENGLISH_CHARACTER_ENCODING_COCA=True
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0

COPY --chmod=755 root /

RUN apk add --no-cache bash ca-certificates tzdata python3 py3-pip py3-requests py3-feedparser py3-beautifulsoup4 \
            py3-lxml py3-pandas py3-matplotlib curl wget \
&& apk add --no-cache --virtual rime-dict-dep build-base python3-dev git \
# use_2to3 is invalid
&& pip3 install --no-cache-dir setuptools==57.5.0 \
&& pip3 install --no-cache-dir datetime python-csv \
&& apk add --no-cache font-wqy-zenhei opencc --repository https://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
# install s6-overlay
&& if [ "$(uname -m)" = "x86_64" ];then s6_arch=x86_64;elif [ "$(uname -m)" = "aarch64" ];then s6_arch=aarch64;elif [ "$(uname -m)" = "armv7l" ];then s6_arch=arm; fi \
&& wget -P /tmp https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-noarch.tar.xz \
&& tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz \
&& wget -P /tmp https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-${s6_arch}.tar.xz \
&& tar -C / -Jxpf /tmp/s6-overlay-${s6_arch}.tar.xz \
&& wget -P /tmp https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-symlinks-noarch.tar.xz \
&& tar -C / -Jxpf /tmp/s6-overlay-symlinks-noarch.tar.xz \
&& wget -P /tmp https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-symlinks-arch.tar.xz \
&& tar -C / -Jxpf /tmp/s6-overlay-symlinks-arch.tar.xz \
# install rime_dict
&& git clone --depth 1 https://github.com/gshang2017/rime-dict.git  /usr/local/rime_dict \
#install rime-dict dep
&& pip3 install --no-cache-dir -r /usr/local/rime_dict/requirements.txt \
# install imewlconverter
&& TAG_NAME=$(curl --silent https://api.github.com/repos/gshang2017/rime-dict/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/') \
&& IMEWLCONVERTER_FILE_NAME=$(curl --silent https://api.github.com/repos/gshang2017/rime-dict/releases/latest | grep 'imewlconverter' | grep 'name' | sed -E 's/.*"([^"]+)".*/\1/') \
&& wget -P /tmp https://github.com/gshang2017/rime-dict/releases/download/$TAG_NAME/${IMEWLCONVERTER_FILE_NAME} \
&& mkdir -p /usr/local/rime_dict/imewlconverter \
&& tar -zxf /tmp/${IMEWLCONVERTER_FILE_NAME} -C /usr/local/rime_dict/imewlconverter \
# download dict.db
&& wget -P /tmp https://github.com/gshang2017/rime-dict/releases/download/$TAG_NAME/dict.tar.gz \
&& tar -zxf /tmp/dict.tar.gz -C /usr/local/rime_dict/ \
&& echo $TAG_NAME > /usr/local/rime_dict/version.txt \
#
&& apk del rime-dict-dep \
&& rm -rf /var/cache/apk/* /tmp/*

VOLUME /output /config
ENTRYPOINT [ "/init" ]

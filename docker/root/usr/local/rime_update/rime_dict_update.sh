#! /bin/sh

if [ "$RIME_DICT_UPDATE_AUTO" == "true" ]; then
  TAG_NAME=$(curl --silent https://api.github.com/repos/gshang2017/rime-dict/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
  if [ "$(cat /usr/local/rime_dict/version.txt)" != "$TAG_NAME" ]; then
    wget -P /tmp https://github.com/gshang2017/rime-dict/releases/download/$TAG_NAME/dict.tar.gz
    tar -zxf /tmp/dict.tar.gz -C /usr/local/rime_dict/
    rm /usr/local/rime_dict/version.txt
    echo $TAG_NAME > /usr/local/rime_dict/version.txt
    cp -rf /usr/local/rime_dict/version.txt /config
    rm -rf /tmp/*
    if [ -d /usr/local/rime_dict/output ]; then
      rm -rf /usr/local/rime_dict/output/
    fi
    #生成rime词库
    cd /usr/local/rime_dict/
    python3 rime_dict.py
    cp -rf /usr/local/rime_dict/output/* /output/
  fi
fi

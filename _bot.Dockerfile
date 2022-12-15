FROM python:3.9-slim as builder
ENV URL=https://gitee.com/mikumifa/QChatGPT/releases/download/1.0/QChatGPT-1.0.zip

WORKDIR /bot
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list\
    && apt-get clean \
    && apt-get update \
    && apt install unzip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget git libbz2-dev -y\
    && python -m pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com\
    && pip install -r /bot/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install websockets --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python main.py


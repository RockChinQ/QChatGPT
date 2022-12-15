FROM openjdk:17-jdk-alpine

ENV URL=https://github.com/iTXTech/mirai-console-loader/releases/download/v2.1.2/mcl-2.1.2.zip
WORKDIR /mirai
CMD   java -jar mcl.jar --update-package net.mamoe:mirai-api-http --channel stable-v2 --type plugin \
    && java -jar mcl.jar
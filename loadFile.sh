!#bin/sh

wget -O bot.zip https://gitee.com/mikumifa/QChatGPT/releases/download/1.0/QChatGPT-1.0.zip 
unzip -o -d  ./bot bot.zip 
rm bot.zip
wget -O mcl.zip https://github.com/iTXTech/mirai-console-loader/releases/download/v2.1.2/mcl-2.1.2.zip
unzip -o -d  ./mirai mcl.zip 
rm mcl.zip
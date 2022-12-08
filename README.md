# QChatGPT

通过调用OpenAI GPT-3模型提供的Completion API来实现一个更加智能的QQ机器人  
已部署的测试机器人QQ: 960164003  

## 技术栈

- [Mirai](https://github.com/mamoe/mirai) 高效率 QQ 机器人支持库
- [YiriMirai](https://github.com/YiriMiraiProject/YiriMirai) 一个轻量级、低耦合的基于 mirai-api-http 的 Python SDK。
- PyMySQL MySQL驱动
- [OpenAI API](https://openai.com/api/) OpenAI API

## 项目结构

- `pkg.database` 数据库操作相关
- `pkg.openai` OpenAI API相关
- `pkg.qqbot` QQ机器人相关

## 部署

### 1. 注册OpenAI账号并取得api_key

参考以下文章

- [只需 1 元搞定 ChatGPT 注册](https://zhuanlan.zhihu.com/p/589470082)
- [手把手教你如何注册ChatGPT，超级详细](https://guxiaobei.com/51461)

注册成功后请前往[个人中心查看](https://beta.openai.com/account/api-keys)api_key

### 2. 配置Mirai

按照[此教程](https://yiri-mirai.wybxc.cc/tutorials/01/configuration)配置Mirai及YiriMirai

### 3. 配置MySQL数据库

安装MySQL数据库，创建数据库`qchatgpt`

### 4. 配置此程序

1. 克隆此项目

```bash
git clone https://github.com/RockChinQ/QChatGPT
```

2. 安装依赖

```bash
pip install pymysql yiri-mirai openai colorlog
```

3. 运行一次主程序，生成配置文件

```bash
python main.py
```

4. 编辑配置文件`config.py`

按照文件内注释填写配置信息

5. 运行主程序

```bash
python main.py
```

无报错信息即为运行成功

## 使用

### 私聊使用

1. 添加机器人QQ为好友
2. 发送消息给机器人，机器人即会自动回复
3. 可以通过`!help`查看帮助信息

<img alt="私聊示例" src="res/屏幕截图%202022-12-08%20150949.png" width="917" height="465"/>

### 群聊使用

1. 将机器人拉进群
2. at机器人并发送消息，机器人即会自动回复
3. at机器人并发送`!help`查看帮助信息

<img alt="群聊示例" src="res/屏幕截图%202022-12-08%20150511.png" width="671" height="522"/>
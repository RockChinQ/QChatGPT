# Mirai的配置
# 请到配置mirai的步骤中的教程查看每个字段的信息
# host: 运行mirai的主机地址
# port: 运行mirai的主机端口
# verifyKey: mirai-api-http的verifyKey
# qq: 机器人的QQ号
mirai_http_api_config = {
    "host": "",
    "port": 8080,
    "verifyKey": "",
    "qq": 0
}

# MySQL数据库的配置
# host: 数据库地址
# port: 数据库端口
# user: 数据库用户名
# password: 数据库密码
# database: 数据库名
mysql_config = {
    "host": "",
    "port": 3306,
    "user": "",
    "password": "",
    "database": ""
}

# OpenAI的配置
# api_key: OpenAI的API Key
openai_config = {
    "api_key": "",
}

# OpenAI的completion API的参数
# 不了解的话请不要修改，具体请查看OpenAI的文档
completion_api_params = {
    "model": "text-davinci-003",
    "temperature": 0.9,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0.4,
    "presence_penalty": 0.3,
}

# 消息处理的超时时间
process_message_timeout = 45

# 消息处理超时重试次数
retry_times = 3

# 每个会话的过期时间
session_expire_time = 60 * 60 * 24 * 7

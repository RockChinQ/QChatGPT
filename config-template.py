mirai_http_api_config = {
    "host": "",
    "port": 8080,
    "verifyKey": "",
    "qq": 0
}

mysql_config = {
    "host": "",
    "port": 3306,
    "user": "",
    "password": "",
    "database": ""
}

openai_config = {
    "api_key": "",
}

completion_api_params = {
    "model": "text-davinci-003",
    "temperature": 0.9,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0.4,
    "presence_penalty": 0.3,
}

process_message_timeout = 45

retry_times = 3

session_expire_time = 60 * 60 * 24 * 7

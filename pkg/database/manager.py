import time

import pymysql
from pymysql.converters import escape_string

import config

inst = None


class DatabaseManager:
    host = ''
    port = 0
    user = ''
    password = ''
    database = ''
    conn = None
    cursor = None

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.reconnect()

        global inst
        inst = self

    def reconnect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.database, autocommit=True)
        self.cursor = self.conn.cursor()

    def initialize_database(self):
        self.cursor.execute("""
        create table if not exists `sessions` (
            `id` bigint not null auto_increment primary key,
            `name` varchar(255) not null,
            `type` varchar(255) not null,
            `number` bigint not null,
            `create_timestamp` bigint not null,
            `last_interact_timestamp` bigint not null,
            `prompt` text not null
        )
        """)
        print('Database initialized.')

    def persistence_session(self, subject_type: str, subject_number: int, create_timestamp: int,
                            last_interact_timestamp: int, prompt: str):
        # 检查是否已经有了此name和create_timestamp的session
        # 如果有，就更新prompt和last_interact_timestamp
        # 如果没有，就插入一条新的记录
        self.cursor.execute("""
        select count(*) from `sessions` where `type` = '{}' and `number` = {} and `create_timestamp` = {}
        """.format(subject_type, subject_number, create_timestamp))
        count = self.cursor.fetchone()[0]
        if count == 0:
            self.cursor.execute("""
            insert into `sessions` (`name`, `type`, `number`, `create_timestamp`, `last_interact_timestamp`, `prompt`) 
            values ('{}', '{}', {}, {}, {}, '{}')
            """.format("{}_{}".format(subject_type, subject_number), subject_type, subject_number, create_timestamp,
                       last_interact_timestamp, escape_string(prompt)))
        else:
            self.cursor.execute("""
            update `sessions` set `last_interact_timestamp` = {}, `prompt` = '{}' 
            where `type` = '{}' and `number` = {} and `create_timestamp` = {}
            """.format(last_interact_timestamp, escape_string(prompt), subject_type,
                       subject_number, create_timestamp))

    # 记载还没过期的session数据
    def load_valid_sessions(self) -> dict:
        # 从数据库中加载所有还没过期的session
        self.cursor.execute("""
        select `name`, `type`, `number`, `create_timestamp`, `last_interact_timestamp`, `prompt` 
        from `sessions` where `last_interact_timestamp` > {}
        """.format(int(time.time()) - config.session_expire_time))
        results = self.cursor.fetchall()
        sessions = {}
        for result in results:
            session_name = result[0]
            subject_type = result[1]
            subject_number = result[2]
            create_timestamp = result[3]
            last_interact_timestamp = result[4]
            prompt = result[5]

            sessions[session_name] = {
                'subject_type': subject_type,
                'subject_number': subject_number,
                'create_timestamp': create_timestamp,
                'last_interact_timestamp': last_interact_timestamp,
                'prompt': prompt
            }
        return sessions


def get_inst() -> DatabaseManager:
    global inst
    return inst

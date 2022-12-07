import pymysql

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
                                    database=self.database)
        self.cursor = self.conn.cursor()


def get_inst() -> DatabaseManager:
    global inst
    return inst

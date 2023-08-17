import time
import asyncio
import logging

from src.models.middleware.session import Session

from ...models.middleware import session
from ...models.system import config as cfg
from ...models import application


session_expire_time = cfg.ConfigEntry(
    "Session.yaml",
    "session_expire_time",
    10*60,
    "# session过期时间（秒）\n# 默认10分钟",
)


class DefaultSession(session.Session):

    create_time: int
    """创建时间"""

    update_time: int
    """最近一次更新时间"""

    def __init__(self):
        """初始化
        """
        self.create_time = int(time.time())
        self.update_time = int(time.time())


class DefaultSessionManagerFactory(session.SessionManagerFactory):
    """默认session管理器工厂
    """

    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'DefaultSessionManager':
        """创建session管理器
        """
        return DefaultSessionManager(config)


class DefaultSessionManager(session.SessionManager):
    """默认session管理器
    """

    config: cfg.ConfigManager

    sessions: dict[str, DefaultSession]
    """session字典"""

    def __init__(self, config: cfg.ConfigManager):
        """初始化
        """
        self.config = config

        self.sessions = {}
        
    async def expire_task(self):
        """过期任务
        """
        while True:
            await asyncio.sleep(20)
            if application.get_application(self.config.namespace) is None:  # 当前应用已经被销毁
                break
            for launcher in self.sessions:
                session = self.sessions[launcher]
                if session.update_time + self.config.get(session_expire_time) < int(time.time()):
                    self.reset_session(session)
                    logging.info(f"session {launcher} expired, reset.")

    def _create_session(self, launcher: str) -> session.Session:
        """创建session
        """
        return DefaultSession()

    def get_session(self, launcher: str) -> session.Session:
        """获取session
        """
        if launcher not in self.sessions:
            self.sessions[launcher] = self._create_session(launcher)
        return self.sessions[launcher]

    def append_message(self, session: DefaultSession, message: dict[str, str]):
        """添加消息
        """
        session.messages.append(message)
        session.update_time = int(time.time())

    def reset_session(self, session: DefaultSession):
        """重置session
        """
        session.messages = []
        session.create_time = int(time.time())
        session.update_time = int(time.time())

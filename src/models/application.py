
from .system import config
from .frontend import controller as frontctrl
from .backend import controller as backctrl

applications: dict[str, 'Application'] = {}


def get_application(namespace: str) -> 'Application':
    """获取应用实例
    
    Args:
        namespace (str): 应用命名空间。
    
    Returns:
        Application: 应用实例。
    """
    return applications[namespace]


class Application:
    
    namespace: str
    
    config_manager: config.ConfigManager
    
    front_controller: frontctrl.FrontendController
    
    back_controller: backctrl.BackendController
    
    def __init__(
        self,
        namespace: str,
        config_manager: config.ConfigManager,
        front_controller: frontctrl.FrontendController,
        back_controller: backctrl.BackendController,
    ):
        global applications
        
        applications[namespace] = self
    
    async def run(self):
        """运行应用
        """
        raise NotImplementedError
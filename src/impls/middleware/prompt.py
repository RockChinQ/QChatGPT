from ...models.middleware import prompt
from ...runtime import module
from ...models.system import config as cfg


system_prompts = cfg.ConfigEntry(
    "QueryProcessor.yaml",
    "system_prompts",
    {
        "default": "如果用户之后看起来需要获取帮助，请说“输入!help获取帮助”"
    },
    """# 情景预设（机器人人格）
# 每个会话的预设信息，影响所有会话，无视指令重置
# 可以通过这个字段指定某些情况的回复，可直接用自然语言描述指令
# 
# 可参考 https://github.com/PlexPt/awesome-chatgpt-prompts-zh
#
# 如果需要多个情景预设，并在运行期间方便切换，请使用字典的形式填写，例如
# system_prompts = {
#   "default": "如果我之后想获取帮助，请你说“输入!help获取帮助”",
#   "linux-terminal": "我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。",
#   "en-dict": "我想让你充当英英词典，对于给出的英文单词，你要给出其中文意思以及英文解释，并且给出一个例句，此外不要有其他反馈。",
# }
#
# 在使用期间即可通过指令：
# !reset [名称]
#   来使用指定的情景预设重置会话
# 例如：
# !reset linux-terminal
# 若不指定名称，则使用默认情景预设
# 
# 也可以使用指令：
# !default <名称>
#   将指定的情景预设设置为默认情景预设
# 例如：
# !default linux-terminal
# 之后的会话重置时若不指定名称，则使用linux-terminal情景预设
# 
# 还可以加载文件中的预设文字，使用方法请查看：https://github.com/RockChinQ/QChatGPT/wiki/%E5%8A%9F%E8%83%BD%E4%BD%BF%E7%94%A8#%E9%A2%84%E8%AE%BE%E6%96%87%E5%AD%97"""
)


@module.component(prompt.PromptManagerFactory)
class SingleSystemPromptModePromptManagerFactory(prompt.PromptManagerFactory):
    """仅设置单条System Prompt的Prompt模式工厂类"""

    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'SingleSystemPromptModePromptManager':
        return SingleSystemPromptModePromptManager(config)


class SingleSystemPromptModePromptManager(prompt.PromptManager):
    """仅设置单条System Prompt的Prompt模式"""

    config: cfg.ConfigManager

    defalut_prompt_key: str

    def __int__(self, config: cfg.ConfigManager):
        """初始化
        """
        self.config = config

        self.defalut_prompt_key = "default"

        if self.defalut_prompt_key not in self.list_prompt():
            self.defalut_prompt_key = self.list_prompt()[0]

    def list_prompt(self) -> list[str]:
        """列出所有prompt的key

        Returns:
            list[str]: prompt的key列表
        """
        return list(self.config.get(system_prompts).keys())
    
    def get_prompt(self, prompt_key: str = None) -> tuple[str, list[dict[str, str]]]:

        if prompt_key is None:
            prompt_key = self.defalut_prompt_key

        for key, value in self.config.get(system_prompts).items():
            if key.startswith(prompt_key):
                return key, value
            
        raise KeyError(f"未找到对应的prompt: {prompt_key}")
    
    def set_as_default(self, prompt_key: str):
        """设置默认prompt
        """
        key, _ = self.get_prompt(prompt_key)

        self.defalut_prompt_key = key

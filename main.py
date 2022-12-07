import os
import shutil
import sys

import pkg.openai.manager
import pkg.database.manager
import pkg.openai.session


def init_db():
    import config
    database = pkg.database.manager.DatabaseManager(**config.mysql_config)

    database.initialize_database()


def main():
    # 检查是否有config.py,如果没有就把config-template.py复制一份,并退出程序
    if not os.path.exists('config.py'):
        shutil.copy('config-template.py', 'config.py')
        print('请先在config.py中填写配置')
        return
    # 导入config.py
    assert os.path.exists('config.py')
    import config

    # 主启动流程
    openai_interact = pkg.openai.manager.OpenAIInteract(config.openai_config['api_key'], config.completion_api_params)

    database = pkg.database.manager.DatabaseManager(**config.mysql_config)

    # 加载所有未超时的session
    pkg.openai.session.load_sessions()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init_db':
        init_db()
        sys.exit(0)
    main()

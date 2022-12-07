import os
import shutil


def main():
    # 检查是否有config.py,如果没有就把config-template.py复制一份,并退出程序
    if not os.path.exists('config.py'):
        shutil.copy('config-template.py', 'config.py')
        print('请先在config.py中填写配置')
        return
    # 导入config.py
    assert os.path.exists('config.py')
    import config

    # print(config.mirai_http_api_config)


if __name__ == '__main__':
    main()

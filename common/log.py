import logging.config
import logging
import os


def log():
    #获取配置文件
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join('conf','logconfig.ini')
    #配置日志文件
    logging.config.fileConfig(file_path)
    #创建日志生成器
    logger = logging.getLogger()
    return logger



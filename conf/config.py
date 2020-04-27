from configparser import ConfigParser
import os

#读取配置文件
def getconfig():
    #获取配置文件
    current_path = os.path.dirname(__file__)
    conf_path = os.path.join(current_path,'config.ini')

    #读取配置文件
    confp = ConfigParser()
    confp.read(conf_path)
    
    return confp

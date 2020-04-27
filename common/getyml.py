import yaml
import os

#传入参数文件的路径，获取参数
def getdata(filepath):
    print(filepath)
    with open(filepath,'r',encoding='utf-8') as f:
        data = yaml.load(f.read())
    return data


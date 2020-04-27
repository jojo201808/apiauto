import pytest
from apiauto.common import getyml
import os
import requests
from apiauto.conf import config
import allure

'''
测试登录接口的用例
'''
#获取参数
def getdata(reqnum):
    #参数文件路径
    filepath = os.path.join(os.getcwd(),'params','tenantmanage','login.yml')
    data = getyml.getdata(filepath)
    path = data['login'][reqnum]['path']
    headers = data['login'][reqnum]['headers']
    param = data['login'][reqnum]['param']
    expected = data['login'][reqnum]['expected']
    #获取baseurl
    base_url = config.getconfig()['test_env']['baseurl']
    urlpath = base_url + path
    return urlpath,headers,param,expected

@allure.feature('登录')
class TestLogin:
    @allure.story('正确的用户名密码')
    def test_success(self):
        urlpath,headers,param,expected = getdata(0)
        print(urlpath)
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content

    @allure.story('错误的用户名密码')
    def test_fail(self):
        urlpath,headers,param,expected = getdata(1)
        print(urlpath)
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
        
pytest.main(['-s'])
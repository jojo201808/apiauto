
import pytest
from apiauto.common import getyml
import os
import requests
from apiauto.conf import config
import allure
    
def getdata(reqnum):
    filepath = os.path.join(os.getcwd(),'params','tenantmanage','login.yml')
    data = getyml.getdata(filepath)
    path = data['cdata'][reqnum]['path']
    headers = data['cdata'][reqnum]['headers']
    param = data['cdata'][reqnum]['param']
    expected = data['cdata'][reqnum]['expected']
    #获取baseurl
    base_url = config.getconfig()['test_env']['baseurl']
    urlpath = base_url + path
    fdesc = data['cdata'][reqnum]['fdesc']
    fname = data['cdata'][reqnum]['fname']
    return urlpath,headers,param,expected    
    
@allure.feature('登录')
@pytest.mark.tt
class TestLogin:    
    
    @allure.story('正确的用户名，密码')
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
pytest.main(['-s','-m','tt'])
    
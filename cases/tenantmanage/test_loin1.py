import pytest
from apiauto.common import getyml
import os
import requests
from apiauto.conf import config
import allure
    
    #登录的接口用例 AutoCreate
    
@allure.feature('登录')
class TestLogin:    
    
    @allure.story('正确的用户名，密码')
    @pytest.mark.parametrize('getdata',[{'seq': 0, 'filep': 'e:\\test\\apiauto\\params\\tenantmanage\\login.yml'}],indirect=True)
    def test_success(self,getdata):
        urlpath,headers,param,expected = getdata
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
    
    @allure.story('错误的用户名密码')
    @pytest.mark.parametrize('getdata',[{'seq': 1, 'filep': 'e:\\test\\apiauto\\params\\tenantmanage\\login.yml'}],indirect=True)
    def test_fail(self,getdata):
        urlpath,headers,param,expected = getdata
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content

pytest.main(['-s'])
    
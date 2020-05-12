import pytest
from apiauto.common import getyml,log
import os
import requests
from apiauto.conf import config
import allure

logger = log.log()
    
    #发送消息接口用例 AutoCreate
    
@allure.feature('发送消息')
class TestAddmessage:    
    
    @allure.story('发送消息内容为通知')
    @pytest.mark.parametrize(('getdata','getrspparam'),[({'seq': 0, 'filep': 'e:\\test\\apiauto\\params\\tenantmanage\\sendmessage.yml'},r'e:\test\apiauto\params\tenantmanage\sendmessage.yml')],indirect=True)
    def test_send01(self,getrspparam,getdata):
        usertoken,paramname = getrspparam
        urlpath,headers,param,expected = getdata
        headers[paramname] = usertoken
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
    
    @allure.story('发送消息内容为公告')
    @pytest.mark.parametrize(('getdata','getrspparam'),[({'seq': 1, 'filep': 'e:\\test\\apiauto\\params\\tenantmanage\\sendmessage.yml'},r'e:\test\apiauto\params\tenantmanage\sendmessage.yml')],indirect=True)
    def test_send02(self,getrspparam,getdata):
        usertoken,paramname = getrspparam
        urlpath,headers,param,expected = getdata
        headers[paramname] = usertoken
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
    
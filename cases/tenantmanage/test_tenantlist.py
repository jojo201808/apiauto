import pytest
from apiauto.common import getyml,log
import os
import requests
from apiauto.conf import config
import allure

logger = log.log()
    
    #登录列表的接口用例 AutoCreate
    
@allure.feature('租户列表')
class TestTenantList:    
    
    @allure.story('搜索存在的kaixin')
    @pytest.mark.parametrize(('getdata','getrspparam'),[({'seq': 0, 'filep': 'e:\\test\\apiauto\\params\\tenantmanage\\tenantlist.yml'},r'e:\test\apiauto\params\tenantmanage\tenantlist.yml')],indirect=True)
    def test_kaixin(self,getrspparam,getdata):
        usertoken,paramname = getrspparam
        urlpath,headers,param,expected = getdata
        headers[paramname] = usertoken
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
    
    @allure.story('搜索没有数据的1111')
    @pytest.mark.parametrize(('getdata','getrspparam'),[({'seq': 1, 'filep': 'e:\\test\\apiauto\\params\\tenantmanage\\tenantlist.yml'},r'e:\test\apiauto\params\tenantmanage\tenantlist.yml')],indirect=True)
    def test_111(self,getrspparam,getdata):
        usertoken,paramname = getrspparam
        urlpath,headers,param,expected = getdata
        headers[paramname] = usertoken
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
    
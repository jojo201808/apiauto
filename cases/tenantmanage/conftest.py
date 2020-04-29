import pytest
import os
from apiauto.common import getyml
from apiauto.conf import config

#获取参数
@pytest.fixture(scope="function")
def getdata(request):
    reqparm= request.param
    #参数文件路径
    filepath = reqparm['filep']
    reqnum = reqparm['seq']
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
    


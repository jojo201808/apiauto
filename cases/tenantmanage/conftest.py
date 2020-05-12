import pytest
import os
from apiauto.common import getyml,log,db
from apiauto.conf import config
import requests
import json

logger = log.log()


#获取yml数据文件，返回请求值以及期望值
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
    
#返回数据给下一个接口使用，如token
@pytest.fixture(scope="class")
def getrspparam(request):
    filepath= request.param
    data = getyml.getdata(filepath)
    path = data['fixtures']['pre'][1]['fdata']['path']
    #获取baseurl
    base_url = config.getconfig()['test_env']['baseurl']
    urlpath = base_url + path
    headers = data['fixtures']['pre'][1]['fdata']['headers']
    params = data['fixtures']['pre'][1]['fdata']['param']
    r = requests.post(url=urlpath,headers=headers,json=params)
    content = json.loads(r.text)
    userparam = content['data']
    paramname = data['fixtures']['pre'][1]['fdata']['resparam']
    return userparam,paramname
 
    
#数据库操作
@pytest.fixture(scope="function")
def dealsql(request):
    sql,deal = request.param
    logger.info('数据库操作%s%s' % (deal,sql))

    db = db.Mydb()
    if deal == 'select':
        result = db.select(sql)
        return result
    elif deal == 'update':
        db.update(sql)
    elif deal == 'insert':
        db.insert(sql)
    elif deal == 'delete':
        db.delete(sql)
    
    db.closedb()    
    
    
#单纯的接口前置操作
@pytest.fixture(scope="function")
def reqbefore(request):
    filepath= request.param
    data = getyml.getdata(filepath)
    path = data['prefixture']['path']
    #获取baseurl
    base_url = config.getconfig()['test_env']['baseurl']
    urlpath = base_url + path
    headers = data['prefixture']['headers']
    params = data['prefixture']['param']
    r = requests.post(url=urlpath,headers=headers,json=params)
    return r.status
 
    
#单纯的接口后置操作
@pytest.fixture(scope="function")
def reqafter(request):
    filepath= request.param
    data = getyml.getdata(filepath)
    path = data['aftfixture']['path']
    #获取baseurl
    base_url = config.getconfig()['test_env']['baseurl']
    urlpath = base_url + path
    headers = data['aftfixture']['headers']
    params = data['aftfixture']['param']
    r = requests.post(url=urlpath,headers=headers,json=params)
    return r.status
 
    
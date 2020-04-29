#用于定义测试用例生成的模板
from string import Template
from apiauto.common import getyml
import os

#获取yml数据
def getdata():
    filepath = os.path.join(os.getcwd(),'params','tenantmanage','login.yml')
    print(filepath)
    data = getyml.getdata(filepath)
    return data



#模板1：test 普通的post请求模板
def case_tem1():
    data = getdata()
    #引入库模板
    si = '''
import pytest
from apiauto.common import getyml
import os
import requests
from apiauto.conf import config
import allure
    '''
    #获取数据函数
    sd = '''
def getdata(reqnum):
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
    '''

    #脚本描述
    sdesc = Template('''
    $fidesc
    ''')
    sdesc_data = {'fidesc':data['fidesc']}
    sdesc = sdesc.substitute(sdesc_data)

    #类模板
    sc = Template('''
@allure.feature('$cdesc')
class $cname:    
    ''')
    sc_data = {'cdesc':data['cdesc'],'cname':data['cname']}
    sc = sc.substitute(sc_data)

    #方法模板
    sf = Template('''
    @allure.story('$fdesc')
    def $funcname(self):
        urlpath,headers,param,expected = getdata($seqnum)
        print(urlpath)
        r = requests.post(url=urlpath,headers=headers,json=param)
        content = r.text
        #循环断言
        for i in expected:
            assert i in content
    ''')
    #获取参数
    paramlist = []
    for i in data['cdata']:
        d = {}
        d['fdesc'] = i['fdesc']
        d['funcname'] = i['fname']
        d['seqnum'] = i['seq']
        paramlist.append(d)
    
    print(paramlist)
    #合并
    script = si + sd + sc
    #赋值
    for d in paramlist:
        sfd = sf.substitute(d)
        script = script + sfd
    
    filepath = os.path.join(os.getcwd(),'cases',data['fppath'][0],data['fppath'][1])
    with open(filepath,'w',encoding='utf-8') as f:
        f.write(script)

case_tem1()
#模板2 固件
def fixture_tem():
    pass

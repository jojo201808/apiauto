#用于定义测试用例生成的模板
from string import Template
from apiauto.common import getyml
import os

#获取yml数据
def getdata():
    filepath = os.path.join(os.getcwd(),'params','tenantmanage','login.yml')
    print(filepath)
    data = getyml.getdata(filepath)
    return data,filepath



#模板1：test 普通的post请求模板
def case_tem1():
    data,filepath = getdata()
    #引入库模板
    si = '''import pytest
from apiauto.common import getyml
import os
import requests
from apiauto.conf import config
import allure
    '''
    #脚本描述
    sdesc = Template('''
    #$fidesc
    ''')
    sdesc_data = {'fidesc':data['filedesc']}
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
    @pytest.mark.parametrize('$fixturefunc',$fixtureparam,indirect=True)
    def $funcname(self,$fixturefunc):
        urlpath,headers,param,expected = $fixturefunc
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
        d['fixturefunc'] = data['prefixture']['funcname']
        d['fixtureparam'] = [{'seq':i['seq'],'filep':filepath }]
        paramlist.append(d)
    
    print(paramlist)
    #合并
    script = si + sdesc + sc
    #赋值
    for d in paramlist:
        sfd = sf.substitute(d)
        script = script + sfd
    
    #创建py用例脚本文件
    filepath = os.path.join(os.getcwd(),'cases',data['savepath'][0],data['savepath'][1])
    with open(filepath,'w',encoding='utf-8') as f:
        f.write(script)

    #创建fixture固件文件
    sfixture = Template('''
#获取参数
@pytest.fixture(scope="$funcscope")
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
    ''')
    fixturedata = {'funcscope':data['prefixture']['funcscope']}
    sfixture = sfixture.substitute(fixturedata)
    #创建测试固件
    ffilepath = os.path.join(os.getcwd(),'cases',data['prefixture']['savepath'][0],data['prefixture']['savepath'][1])
    with open(ffilepath,'a',encoding='utf-8') as f:
        f.write(sfixture)    


case_tem1()



    

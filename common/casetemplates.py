#用于定义测试用例生成的模板
from string import Template
from apiauto.common import getyml
import os
from apiauto.common import log

logger = log.log()

#获取yml数据
def getdata(filepath):
    logger.info('获取%s的数据' % filepath)
    data = getyml.getdata(filepath)
    return data,filepath
'''
case_tem1: 普通的post请求模板 templatetype 0
case_tem2: 增加获取前置token templatetype 1

fixture_tem1: 获取数据的固件fixturetype: 0   
fixture_tem2：获取返回值的固件如：token的固件 1
fixture_tem3:
fixture_tem4:

'''

#获取params下面的yml文件列表
def getallfilelist():
    #获取params下面的目录
    dirlist = os.listdir(os.path.join(os.getcwd(),'params'))
    logger.info('params文件夹下的所有文件%s' % dirlist)
    filelist = []
    #获取每个目录下的yml文件
    for d in dirlist:
        flist = os.listdir(os.path.join(os.getcwd(),'params',d))
        fpath = os.path.join(os.getcwd(),'params',d)
        for f in flist:
            p = os.path.join(fpath,f)
            filelist.append(p)
    return filelist

#获取params下指定目录下的yml文件列表
def gettargetfilelist(dirname):
    filelist = []
    flist = os.listdir(os.path.join(os.getcwd(),'params',dirname))
    logger.info('params文件夹下指定目录的文件%s' % dirlist)
    fpath = os.path.join(os.getcwd(),'params',dirname)
    for f in flist:
        p = os.path.join(fpath,f)
        filelist.append(p)
    return filelist

#根据yml里的数据判断使用什么模板生成脚本
def generate_script():
    #获取yml文件列表
    logger.info('开始获取params下的yml文件列表')
    filelist = getallfilelist()
    #读取每个yml，生成脚本
    for f in filelist:
        data,filepath = getdata(f)
        #0:模板1 1：模板2
        if data['templatetype'] == -1:
            logger.info('生成conftest中的数据:')
            logger.info('当前fixture数据路径为：')
            logger.info(filepath)
            fixture_tem1(data,filepath)
        elif data['templatetype'] == 1:
            case_tem1(data,filepath)


#写入conftest模板数据
def write_cases(num,sfixture,data):
    fixturedata = {
        'funcscope':data['templates'][num]['funcscope'],
        'fixturefuncname':data['templates'][num]['funcname'],
        'desc':data['templates'][num]['desc'] 
        }
    sfixture = sfixture.substitute(fixturedata)
    #创建测试固件
    ffilepath = os.path.join(os.getcwd(),'cases',data['templates'][num]['savepath'][0],data['templates'][num]['savepath'][1])
    logger.info('生成fixture%d' % num)
    if num == 0:
        with open(ffilepath,'w',encoding='utf-8') as f:
            f.write(sfixture) 
    else:
        with open(ffilepath,'a',encoding='utf-8') as f:
            f.write(sfixture)


    


#模板1：test 普通的post请求模板
def case_tem1(data,filepath):
    #引入库模板
    si = '''import pytest
from apiauto.common import getyml,log
import os
import requests
from apiauto.conf import config
import allure

logger = log.log()
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
        d['fixturefunc'] = data['fixturefuncname']
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

#要用token的模板        
def case_tem2(data,filepath):
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
    @pytest.mark.parametrize(('getdata','$fixturefunc'),[($fixtureparam,r'$fpath')],indirect=True)
    #@pytest.mark.parametrize('$fixturefunc','$fpath',indirect=True)
    def $funcname(self,$fixturefunc,getdata):
        usertoken,paramname = $fixturefunc
        urlpath,headers,param,expected = getdata
        headers[paramname] = usertoken
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
        d['fixturefunc'] = data['fixturefuncname']
        d['fixtureparam'] = {'seq':i['seq'],'filep':filepath }
        d['fpath'] = filepath
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

    #创建前置
    if 'prefixture' in data.keys():
        fixture_tem2(data,filepath)    


#写入conftest模板数据
def write_conftest(num,sfixture,data):
    fixturedata = {
        'funcscope':data['templates'][num]['funcscope'],
        'fixturefuncname':data['templates'][num]['funcname'],
        'desc':data['templates'][num]['desc'] 
        }
    sfixture = sfixture.substitute(fixturedata)
    #创建测试固件
    ffilepath = os.path.join(os.getcwd(),'cases',data['templates'][num]['savepath'][0],data['templates'][num]['savepath'][1])
    logger.info('生成fixture%d' % num)
    if num == 0:
        with open(ffilepath,'w',encoding='utf-8') as f:
            f.write(sfixture) 
    else:
        with open(ffilepath,'a',encoding='utf-8') as f:
            f.write(sfixture)

#创建固件
def fixture_tem1(data,filepath):
    #fixture1 获取数据,并且返回
    sfixture1 = Template('''import pytest
import os
from apiauto.common import getyml,log,db
from apiauto.conf import config
import requests
import json

logger = log.log()


#$desc
@pytest.fixture(scope="$funcscope")
def $fixturefuncname(request):
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
    write_conftest(0,sfixture1,data)

    #fixture2 获取返回值
    sfixture2 = Template('''
#$desc
@pytest.fixture(scope="$funcscope")
def $fixturefuncname(request):
    filepath= request.param
    data = getyml.getdata(filepath)
    path = data['prefixture']['path']
    #获取baseurl
    base_url = config.getconfig()['test_env']['baseurl']
    urlpath = base_url + path
    headers = data['prefixture']['headers']
    params = data['prefixture']['param']
    r = requests.post(url=urlpath,headers=headers,json=params)
    content = json.loads(r.text)
    userparam = content['data']
    paramname = data['prefixture']['resparam']
    return userparam,paramname
 
    ''')
    write_conftest(1,sfixture2,data)

    #fixture3数据库操作
    sfixture3 = Template('''
#$desc
@pytest.fixture(scope="$funcscope")
def $fixturefuncname(request):
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
    
    ''')
    write_conftest(2,sfixture3,data)

    #fixture4 单纯的接口前置操作，跟fixture2类似，但是不要求返回值
    sfixture4 = Template('''
#$desc
@pytest.fixture(scope="$funcscope")
def $fixturefuncname(request):
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
 
    ''')
    write_conftest(3,sfixture4,data)    

    sfixture5 = Template('''
#$desc
@pytest.fixture(scope="$funcscope")
def $fixturefuncname(request):
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
 
    ''')
    write_conftest(4,sfixture5,data)    

generate_script()
    

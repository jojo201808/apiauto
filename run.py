import pytest
import requests
#pytest.main(['-s'])

url = 'http://testoptional.ejoy99.com/proxy/admin/message/deleteMessage'
headers = {
    'userToken':'olja3mscgfvn3727qr419lwq0hrgz3gu',
    'Content-Type':'application/json;charset=UTF-8',
    'tId':'4',
    'appId':'20191204',
    'clientId':'2'
    }
param = {'messageId': 116}

r = requests.post(url,headers=headers,params=param)
print(r.text)
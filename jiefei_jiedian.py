import random
import requests
from lxml import etree
import os

register_url='https://www.jafiyun.online/auth/register'
url=''
def register():
    data={
        'email': '136040875321@gmail.com',
        'name': 'Aike',
        'passwd': '123456789',
        'repasswd': '123456789',
        'code': '0'
    }
    email=''
    for i in range(10):
        email=email+str(random.randint(0,9))
    print(email)
    data['email']=email+'@gmail.com'
    print(data)
    repose=requests.post(register_url,data=data)
    print(repose.status_code)
    return data['email'],data['passwd']

# 通过email和passwd登录网页，返回cookies
def login(email,passwd):
    url='https://www.jafiyun.online/auth/login'
    data={
        'email': email,
        'passwd': passwd,
        'code':'',
        'remember_me': '1'
    }
    # data['email']='8172366342@gmail.com'
    session = requests.session()
    repose = session.post(url, data=data)
    print(repose.status_code)
    print('登录成功')

    cookie_jar=repose.cookies
    cookie = requests.utils.dict_from_cookiejar(cookie_jar)
    print(cookie)
    return cookie

def get_context(cookie):
    url='https://www.jafiyun.online/user'
    session = requests.session()
    repose = session.get(url, cookies=cookie)

    print(repose.status_code)
    print('用户中心登录成功')

    html=repose.content
    tree=etree.HTML(html)
    a=tree.xpath('//*[@id="app"]/div/div[3]/section/div[4]/div[2]/div[2]/div[2]/div/a[7]/@data-clipboard-text')
    print(a[0])
    return a[0]
if __name__ == '__main__':
# 注册
    email,passwd = register()
# 登录
    cookie = login(email,passwd)
# 获取订阅链接
    info=get_context(cookie)
    SKey=os.environ.get('SKEY') #CoolPush酷推KEY
    print(123)
    api = 'https://push.xuthus.cc/send/{}'.format(SKey)
    print(info)
    requests.post(api, info.encode('utf-8'))

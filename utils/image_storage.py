# -*- coding:utf-8 -*-

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'kiKv7Zb6y9Bn7_GKcYNh09COycP8yOOJrtg3CzT4'
secret_key = 'VbgcUWH8QAOngcGhFhWEX22XTAdOrhLsw_N9MDCF'

def storage(image_data):
    #构建鉴权对象
    if not image_data:
        return None
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'ihome'

    #上传到七牛后保存的文件名
    #key = 'my-python-logo.png';

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    #要上传文件的本地路径
    #localfile = './sync/bbb.jpg'

    ret, info = put_data(token, None, image_data)
    print(info)
    #assert ret['key'] == key
    #assert ret['hash'] == etag(image_data)
    return ret['key']


if __name__=='__main__':
    file_name = raw_input('请输入文件名:')
    file = open(file_name,'rb')
    file_data = file.read()
    key = storage(file_data)
    print key
    file.close()

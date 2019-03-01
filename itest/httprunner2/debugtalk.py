# encoding: utf-8
"""
@author: han.li
@file  : debugtalk.py
@time  : 12/27/18 4:32 PM
@dec   : 
"""

import requests, json
import uuid

def get_token():
    url = 'https://api.kingdee.com/auth/user/access_token'
    params = {
        'username': '15220121922',
        'password': 'Test1234@',
        'client_id': '201384',
        'client_secret': '8be6ca3bee8258402dd11b05cad29334'
    }

    response = requests.get(url, headers={}, params=params)
    if response.status_code == 200:
        return json.loads(response.text)['data']['access_token']
    else:
        return ''

# 获取sd
def get_unique_id():
    return str(uuid.uuid4()).replace('-', '')

if __name__ == '__main__':
    print(str(get_unique_id()).replace('-',''))
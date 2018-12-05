# encoding: utf-8
"""
@author: han.li
@file  : ocr.py
@time  : 11/1/18 5:31 PM
@dec   : 
"""
from itest.utils.request import uri_join
from bson import ObjectId
import requests, json
import base64
from itest.test_data.models import ImageData

BAIDU_URL = 'https://aip.baidubce.com/'
OCR_BASIC_API = 'rest/2.0/ocr/v1/general_basic'
OCR_API = 'rest/2.0/ocr/v1/general'
OAUTH_API = '/oauth/2.0/token'
OAUTH_TOKEN = '24.2de4f121e459554a658ec0b174a73f91.2592000.1543373303.282335-14595206'

TEST_URL = 'http://api.test.com/'
TEST_GATEWAY = 'https://gateway.testresearch.com'
KD_ORC_API = '/brpocr/general'
KD_OAUTH_API = '/certification/oauth2/token'
KD_OAUTH_TOKEN = 'JytFJdiXdVIiFLkr1qF9QtAF4Rnrs8Nb'


class BaiduOcr(object):
    """
    Baidu ocr 识别
    """
    words_result = []

    def __init__(self):
        self.baidu_url = BAIDU_URL

    @staticmethod
    def get_access_token():
        at_url = uri_join(BAIDU_URL, OAUTH_API)
        data = {
            'grant_type': 'client_credentials',
            'client_id': 'GU3UUC8rjB8enetiMkW7nfl3',
            'client_secret': 'DrozEeXNp48z7CyhF76YOLFzc0R6E4Ip'
        }

        response = requests.post(at_url, headers={}, params={}, data=data)
        if response.status_code == 200:
            return json.loads(response.text)['access_token']
        else:
            return ''

    def recognize(self, uri, image_path):
        # params = {
        #     'access_token': OAUTH_TOKEN,
        # }
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # 直接调用开发环境接口，图片先转码
        with open(image_path, "rb") as f:
            imgBase64 = base64.b64encode(f.read())
        data = {
            'image': imgBase64,
            'access_token': OAUTH_TOKEN
        }
        print(data)
        response = requests.post(uri, headers={}, data=data)
        print(response.text)
        self.words_result = json.loads(response.text)['words_result']

    def recognize_basic(self, image_path):
        uri = uri_join(self.baidu_url, OCR_BASIC_API)
        self.recognize(uri, image_path)

    def recognize_location(self, image_path):
        uri = uri_join(self.baidu_url, OCR_API)
        self.recognize(uri, image_path)

    def get_url(self, api):
        return uri_join(self.baidu_url, api)

    def get_words_result(self):
        return self.words_result


class TestOrc(object):
    """
    金蝶 ocr 识别
    """
    words_result = []

    def __init__(self):
        self.url = TEST_URL

    @staticmethod
    def get_access_token():
        at_url = uri_join(TEST_GATEWAY, KD_OAUTH_API)
        data = {
            'grant_type': 'client_credentials',
            'client_id': 'lrmKr2a4L742Z5pu0au0amkGBSJU02Hg',
            'client_secret': 'AI2qlrygcaRy1bsGBiXfmVmrZOBoHkry'
        }

        response = requests.post(at_url, headers={}, params={}, data=data)

        if response.status_code == 200:
            return json.loads(response.text)['access_token']
        else:
            return ''
    # orc识别方法
    def recognize(self, uri, image_path):
        token = self.get_access_token()
        params = {
            'access_token': token,
            'client_id': '201415',
            'client_secret': '8005bcb39ae666289a0e4d8d77e7f920',
            'passwd': 'test_research_generalocr'
        }
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded'
        # }

        # 直接调用生产接口，上传图片
        file = {'image': ('orc识别', open(image_path, 'rb'), 'multipart/form-data')}
        print(params)
        response = requests.post(uri, headers={}, params=params, files=file)
        print(response.text)
        self.words_result = json.loads(response.text)['data']

    def recognize_location(self, image_path):
        uri = uri_join(self.url, KD_ORC_API)
        self.recognize(uri, image_path)

    def get_words_result(self):
        return self.words_result

if __name__ == '__main__':
    images = ImageData.objects(project_id=ObjectId('5badbff15f627df409838fa1'));
    print(images.count())
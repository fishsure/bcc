import requests
from os import path
import requests
import time
label_num = 6
def get_top_keys(key_list: list):
    return key_list[0: min(label_num, len(key_list))]
def translate(query):
    url = 'http://fanyi.youdao.com/translate'
    data = {
        "i": query,  # 待翻译的字符串
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }
    res = requests.post(url, data=data).json()
    return res['translateResult'][0][0]['tgt']  # 打印翻译后的结果

def img_formatter(res, filePath):
    # 翻译英文标签为中文
    time.sleep(3)
    labels = [item['tag']['en'] for item in get_top_keys(res['result']['tags'])]
    labels_cn = []
    for label in labels:
        label_cn = translate(label)
        labels_cn.append(label_cn)
    return {
        'labels': labels_cn,
        'property': '{' +
                    'name: ' + '\'' + path.split(filePath)[1] + '\'' + ', ' +
                    'ext: ' + '\'' + path.splitext(filePath)[-1][1:] + '\'' + ', ' +
                    'size: ' + '\'' + str(path.getsize(filePath)) + '\''+ ', ' +
                    'path: ' + '\'' + filePath + '\''
                    + '}'
    }
def img_tag(image_path: str):
    api_key = 'acc_ec9b217a28c4e19'

    api_secret = 'de16ce61cf5497198e70815b1104e6e7'

    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')})
    print(img_formatter(response.json(), image_path))
img_tag("/root/jfs/357.png")

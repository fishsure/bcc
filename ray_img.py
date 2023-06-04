import requests
from os import path
import requests
import time
import ray
ray.init(address="auto", _redis_password='5241590000000000')
label_num = 6
@ray.remote
def get_top_keys(key_list: list):
    print("777")
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
    print("888")
    res = requests.post(url, data=data).json()
    return res['translateResult'][0][0]['tgt']  # 打印翻译后的结果
@ray.remote
def img_formatter(res, filePath):
    # 翻译英文标签为中文
    time.sleep(3)
    labels = [item['tag']['en'] for item in ray.get(get_top_keys.remote(res['result']['tags']))]
    labels_cn = []
    print("666")
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
@ray.remote
def img_tag(image_path: str):
    api_key = 'acc_ec9b217a28c4e19'

    api_secret = 'de16ce61cf5497198e70815b1104e6e7'

    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')})
    print("333")
    result=ray.get(img_formatter.remote(response.json(), image_path))
    print(result)
    print("111")
def ok():
    print("000")
    ray.get(img_tag.remote("/root/jfs/bnb.png"))
    print("222")
ok()

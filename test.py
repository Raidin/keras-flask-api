import requests
import json

def sample_test():
    url = 'http://127.0.0.1:5000'
    res = requests.get(url)
    print(res.status_code)
    print(res.text)

def predict_json_test():
    url = 'http://127.0.0.1:8989/predict_json'
    with open('./json_to_image_sample/42847.json', 'rb') as json_file:
        data = json.load(json_file)
    res = requests.post(url, json=data)
    print(res.status_code)
    print(res.text)

def predict_img_test():
    url = 'http://127.0.0.1:8989/predict_img'

    with open('./json_to_image_sample/42847.jpg', 'rb') as f:
        files = {'image': f}
        res = requests.post(url, files=files)
    print(res.status_code)
    print(res.text)

if __name__ == '__main__':
    # sample_test()
    predict_json_test()
    # predict_img_test()
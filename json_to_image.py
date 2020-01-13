import json
import base64
import io
import os

from PIL import Image

def Image2Json(path):
    # image to json
    with open(path, mode='rb') as file:
        img = file.read()

    data = dict()
    # data['image_data'] = base64.b64encode(img)
    data['image_data'] = base64.encodebytes(img).decode("utf-8")

    json_data = json.dumps(data)

    save_dir = os.path.split(path)[0]
    save_file = '{}.json'.format(os.path.splitext(os.path.basename(path))[0])

    with open(os.path.join(save_dir, save_file), 'w') as f:
        f.write(json_data)


def Json2Image(path):
    save_dir = os.path.split(path)[0]
    save_file = '{}.png'.format(os.path.splitext(os.path.basename(path))[0])

    # json to image
    with open(path, 'r') as json_file:
        json_data = json.load(json_file)

    img_file = base64.b64decode(json_data['image_data'])
    img = Image.open(io.BytesIO(img_file))
    img.save(os.path.join(save_dir, save_file))

if __name__ == '__main__':
    # Image2Json('./json_to_image_sample/42847.jpg')
    Json2Image('./json_to_image_sample/json_image.json')

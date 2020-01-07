import json
import base64
import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

with open('/home/jihunjung/Desktop/42845.jpg', mode='rb') as file:
    img = file.read()

data = dict()
data['img'] = base64.b64encode(img)

# print(data)

with open('/home/jihunjung/Desktop/json_image.json') as json_file:
    json_data = json.load(json_file)

# print(json_data.keys())
img_file = base64.b64decode(json_data['image_data'])


img = np.array(Image.open(io.BytesIO(img_file)))

print(img.shape)

plt.imshow(img)
plt.show()
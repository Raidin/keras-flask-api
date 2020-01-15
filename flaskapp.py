import matplotlib.pyplot as plt
import numpy as np
import os
import io
import base64

from flask import Flask, render_template, url_for, jsonify, request, redirect
from werkzeug.utils import secure_filename

from keras.models import model_from_json
from PIL import Image
from module import *

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="1"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['myName']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('myName')
        return redirect(url_for('success', name=user))

@app.route('/upload', methods=['GET'])
def load_file():
   return render_template('upload.html')

@app.route('/upload_test', methods=['POST'])
def upload_img_file():
    if request.method == 'POST':
        upload_path = os.path.join('static', 'images/')
        f = request.files['file']
        f.save(upload_path + secure_filename(f.filename))
        img_path = os.path.join(upload_path, f.filename)
        return render_template('draw_image.html', user_image=img_path)

@app.route('/upload_test_2', methods=['POST'])
def upload_img_json():
    if request.method == 'POST':
        data = request.get_json()
        f = base64.b64decode(data['image_data'])
        upload_path = os.path.join('static', 'images/')
        f.save(upload_path + secure_filename(f.filename))
        return render_template('draw_image.html', user_image=img_path)

#### Inference Practice Using Keras ####
###########################################################################
model = None

def load_model():
    global model
    MODEL_DIR = os.path.join('static', 'model/')
    model_struct = os.path.join(MODEL_DIR, 'network_model.json')
    with open(model_struct, 'r') as f:
        model = model_from_json(f.read())

    model_weight = os.path.join(MODEL_DIR, 'trained_weight.h5')
    model.load_weights(model_weight)

def predict(img):
    rois = SelectiveSearch(img)
    print('ROI Shape ::', rois.shape)

    # Predict object
    print('Predict Object Start!!!')
    predict_bbox = PredictObject(model, rois, img)
    print('Predict BBox Shape ::', predict_bbox.shape)

    # Apply Bounding Box Regression
    # refine_bbox = BoundingBoxRegression(reg_model, predict_bbox, img)
    # print('Refine BBox Shape ::', refine_bbox.shape)

    # Apply Non Maximum Suppression
    nms_bbox = NonMaximumSuppression(predict_bbox)
    print('Before regions ::', predict_bbox.shape)
    print('NMS regions ::', nms_bbox.shape)

    return nms_bbox
###########################################################################

@app.route('/detection_test', methods=['GET'])
def detection_test():
    return render_template('detection_test.html')

@app.route('/predict_img', methods=['POST'])
def predict_img():
    if request.method == 'POST':
        load_file = request.files['image']
        file = load_file.read()
        img = np.array(Image.open(io.BytesIO(file)))

        bbox = predict(img)

        DrawBoxes(img, bbox, title='Detection Results', color='red', linestyle="-")
        save_path = os.path.join('static', 'images', '{}_result.png'.format(load_file.filename))
        plt.savefig(save_path)

        return render_template('draw_image.html', user_image=save_path)

@app.route('/predict_json', methods=['POST'])
def predict_json():
    if request.method == 'POST':
        data = request.get_json()

        f = base64.b64decode(data['image_data'])
        img = np.array(Image.open(io.BytesIO(f)))

        bbox = predict(img)

        results = dict()
        obj_data = []
        results['objectCount'] = bbox.shape[0]
        for i in bbox:
            sub = dict()
            sub['class_id'] = 0
            sub['p1_x'] = i[0]
            sub['p1_y'] = i[1]
            sub['p2_x'] = i[2]
            sub['p2_y'] = i[3]
            obj_data.append(sub)
        results['objectData'] = obj_data

        return jsonify(results)

print(' ========== Load Detection Model START ========== ')
load_model()
print(' ========== Load Detection Model END ========== ')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8989', debug=True)

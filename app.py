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
def upload_test():
    if request.method == 'POST':
        upload_path = os.path.join('static', 'images/')
        f = request.files['file']
        f.save(upload_path + secure_filename(f.filename))
        img_path = os.path.join(upload_path, f.filename)
        print('img_path :: ', img_path)
        return render_template('draw_image.html', user_image=img_path)

@app.route('/upload_test_2', methods=['POST'])
def upload_test2():
    if request.method == 'POST':
        data = request.get_json()
        f = base64.b64decode(data['image_data'])
        upload_path = os.path.join('static', 'images/')
        f.save(upload_path + secure_filename(f.filename))
        return render_template('draw_image.html', user_image=img_path)

@app.route('/upload_test_3', methods=['POST'])
def upload_test3():
    if request.method == 'POST':
        upload_path = os.path.join('static', 'images/')
        f = request.files['file']
        f.save(upload_path + secure_filename(f.filename))
        return 'file uploaded successfully'

#### Inference Practice Using Keras ####
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
    print(model)
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

@app.route('/sample_test', methods=['GET'])
def sample_test():
   return render_template('sample_test.html')

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

        file = f.read()
        img = np.array(Image.open(io.BytesIO(file)))

        bbox = predict(img)

        results = []
        for i in bbox:
            sub = dict()
            sub['class_id'] = 0
            sub['bbox'] = i[:4].tolist()
            results.append(sub)

        return jsonify(results)


if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port='8989')

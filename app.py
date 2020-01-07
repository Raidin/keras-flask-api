import os

from flask import Flask, render_template, url_for, jsonify, request, redirect
from werkzeug import secure_filename


# Flask 객체를 App 에 할당
app = Flask(__name__)

# app 객체를 이용해 라우팅 경로 설정 -> 실행 할 함수
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/json_test')
def json_test():
    data = {'name':'jihun', 'age':30}
    return jsonify(data)

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

@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify(data)

@app.route('/upload')
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
        upload_path = os.path.join('static', 'images/')
        f = request.files['file']
        f.save(upload_path + secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8989')

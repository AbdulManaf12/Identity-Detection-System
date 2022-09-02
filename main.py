import os
import Model
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request

UPLOAD_FOLDER = './static\\model_data\\upload_test\\'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = Model.MyModel()


def DeleteTemporaryFiles():
    files = os.scandir('./static/model_data/upload_test')
    for file in files:
        if file.is_file():
            os.remove(file)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/predict', methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        DeleteTemporaryFiles()
        file = request.files['image']
        fileName = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(fileName)
        (name, prob) = model.predict(fileName)
        return render_template("predict.html", predicted_name=name, probability=prob, url=fileName)
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        label = request.form['employee-name']
        video_name = request.files['uploaded-video']
        if len(video_name.filename) != 0 and len(label) != 0:
            DeleteTemporaryFiles()
            fileName = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_name.filename))
            video_name.save(fileName)
            model.AddNewDataIntoDataSet(1, label, fileName)
    return render_template('register.html', employees=model.Categories)


@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        label = request.form['name']
        print('me: ' + label)
        files = os.scandir('./static/model_data/dataset')
        for file in files:
            if file.is_file() and file.name.split('-')[0] == label:
                os.remove(file)
        model.Train_Model()
    return render_template('register.html', employees=model.Categories)


app.run(debug=True)

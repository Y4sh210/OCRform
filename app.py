from flask import Flask, render_template, url_for, request, redirect, flash
from OCR import main
import os
from werkzeug.utils import secure_filename
import urllib.request

UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/home')
def home():
    return render_template("index1.html")


@app.route('/data', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        data = main.data()
        print(data)
        email = data[0]
        firstName = data[1]
        lastName = data[2]
        address = data[3]
        phone = data[4]
        tc = data[5]

        return render_template('dataForm.html', email=email, firstName=firstName, lastName=lastName, address=address, phone=phone, tc=tc)

    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["first-name"]

    return render_template('index1.html')


if __name__ == "__main__":
    app.run(debug=True)

import os
# import magic
import urllib.request
from app import app
import PyPDF2
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/upload', methods=['POST'])
def upload_file():
    print("In method upload file")
    if request.method == 'POST':
        print("Request: {}".format(request.files))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # if not os.path.isdir(app.config['UPLOAD_FOLDER']):
            #     os.mkdir(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # flash('File successfully uploaded')
            pdfFileObj = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            text = pageObj.extractText()
            pdfFileObj.close()
            return text
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
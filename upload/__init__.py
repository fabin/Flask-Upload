import os
import sae.storage
from flask import Flask, request, redirect, url_for, send_from_directory
import sys
import logging

UPLOAD_FOLDER = '~/Documents/deploy/Flask-UploadFile'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DOMAIN_NAME = 'album'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            s = sae.storage.Client()
            uploadedFile = request.files['file']
            if uploadedFile and allowed_file(uploadedFile.filename):
                filename = uploadedFile.filename
#                 without sae
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 return redirect(url_for('uploaded_file', filename=filename))
                
#                 with sae
                ob = sae.storage.Object(uploadedFile.read())
                return redirect(s.put(DOMAIN_NAME, filename, ob))
        except:
            logging.exception("Something awful happened!")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File (in package)</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == '__main__':
    app.run()

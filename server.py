# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for
from time import time
from werkzeug import secure_filename
import hashlib

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_FILTERS = ['blur','grayscale','rotate90','rotate180','rotate270']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

def allowed_file(filename):
    '''
        Checks if the file has a permitted extension.
    '''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def generate_hash(string, salt='42'):
    '''
        This function returns the SHA-1 hash of a string.
    '''
    hasher = hashlib.sha1()
    hasher.update(salt)
    hasher.update(string)
    return hasher.hexdigest()

@app.route('/upload_image', methods=['POST'])
def upload_image():
    '''
        This method allows you to send an image file and save it with a name generated hash
        involving the file name and the date of dispatch.
    '''
    file = request.files['file']
    if file and allowed_file(file.filename):
        # change the name of file
        filename = '%s.%s' % (generate_hash('%s%f' % (file.filename, time())), file.filename.rsplit('.', 1)[1])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect(url_for('uploaded_file', filename=filename))
        return filename, 200

@app.route('/apply_effects', methods=['GET','POST'])
def apply_effects():
    '''
        This method applies effects to an image, whose name is given by the "file" attribute.
        The following parameters should be informed (via GET or POST) in the following way, if you want to use them.
        Any parameter that is not on this list will be ignored.
        On success, returns the address of the resulting file.

             file: Required. The file name to be modified.
             width: The new width of image.
             height: The new height of image.
                *If you are informed only of the resizing values (width or height), the ratio will be maintained.
                Alternatively, specify both values.
             effects = [blur, grayscale]: The applied effects must be separated by commas. They will be applied in the
                order in which they are informed.
    '''

    try:
        filename = request.args[file]

        original_file = open(filename)
        imagem = original_file.read()
        original_file.close()

        new_file_name = '%d_%s' % (int(time.time()), filename)
        new_file = open(new_file_name, 'w')
        new_file.write(imagem)
        new_file.close()

        return new_file_name

    except Exception as e:
        raise e
        return 'Processing failed.', 500

@app.route('/upload_form', methods=['GET'])
def upload_form():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="upload_image" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(port=9999)

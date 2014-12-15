# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for
from imagens import *
from time import time
from werkzeug import secure_filename
import hashlib
import os

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_FILTERS = ['QUADRICULATE','GRAYSCALE','CROP','NEGATIVE','GREENING','REDDENING','BLUENING','WIDTH','HEIGHT','ROTATE90','ROTATE180','ROTATE270']

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
    print str(dict(request.args))
    try:
        # Open the file.
        filename = request.args['file']
        img = load_image('%s/%s' % (UPLOAD_FOLDER, filename))

        # Aply the efects.
        if 'effects' in request.args:
            effects = [_.upper() for _ in request.args['effects'].split(',')]

        print
        print effects
        print
        # Applies the independent effects.
        for e in effects:
            try:
                if e in ['QUADRICULATE','GRAYSCALE','CROP','NEGATIVE','GREENING','REDDENING','BLUENING']:
                    img = apply_filter(img, e) or img

                elif e in ['ROTATE90','ROTATE180','ROTATE270']:
                    img = rotate_image(img, int(e[6:])) or img
            except:
                pass

        # Applies the intertwined effects.
        try:
            width = int(request.args['width']) if 'width' in request.args else None
            height = int(request.args['height']) if 'height' in request.args else None
            resize_image(img, width=width, height=height)
        except:
            pass

        new_file_name = '%s/%s' % (DOWNLOAD_FOLDER, filename)
        save_image(img, new_file_name)

        return new_file_name

    except Exception as e:
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

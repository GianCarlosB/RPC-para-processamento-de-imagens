# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for
from images import *
from time import time
from werkzeug import secure_filename
import hashlib
import os
import cv2
import Image
import numpy

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_FILTERS = ['FACE','QUADRICULATE','GRAYSCALE','CROP','NEGATIVE','GREENING','REDDENING','BLUENING','WIDTH','HEIGHT','ROTATE90','ROTATE180','ROTATE270']

app = Flask(__name__, static_folder=DOWNLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

# Default path for Haar Cascade
CASC_PATH = 'haarcascade_frontalface_default.xml'

# Execute a recognition of faces and returne the coordinates of the faces.
def recognize(imagePath, cascPath = CASC_PATH, sf = 1.1, mn = 5, ms = (30, 30), f = cv2.cv.CV_HAAR_SCALE_IMAGE):
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = faceCascade.detectMultiScale( gray, scaleFactor=sf, minNeighbors=mn, minSize=ms, flags=f )

    # Return the list
    return faces

def see_faces(image, coordinates, mode=None):
    try:
        # Reads the image as array.
        img = numpy.array(Image.open(image))

        # Demarcates the faces found.
        for c in coordinates:
            # Filling the face area.
            if mode=='fill':
                # Red layer.
                img[c[1]:c[1]+c[2], c[0]:c[0]+c[2], 0] = 255
            # Drawing a rectangle.
            else:
                # Red layer.
                img[c[1]:c[1]+5, c[0]:c[0]+c[2], 0] = 255
                img[c[1]+c[2]:c[1]+c[2]+5, c[0]:c[0]+c[2], 0] = 255
                img[c[1]:c[1]+c[2], c[0]:c[0]+5, 0] = 255
                img[c[1]:c[1]+c[2], c[0]+c[2]:c[0]+c[2]+5, 0] = 255

                # Green and blue layer.
                img[c[1]:c[1]+5, c[0]:c[0]+c[2], 1:] = 0
                img[c[1]+c[2]:c[1]+c[2]+5, c[0]:c[0]+c[2], 1:] = 0
                img[c[1]:c[1]+c[2], c[0]:c[0]+5, 1:] = 0
                img[c[1]:c[1]+c[2], c[0]+c[2]:c[0]+c[2]+5, 1:] = 0

        # Returns the image obtained.
        return Image.fromarray(img)
    except:
        return None

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
        fullfilename = '%s/%s' % (UPLOAD_FOLDER, filename)
        img = load_image(fullfilename)


        # Aply the efects.
        if 'effects' in request.args:
            effects = [_.upper() for _ in request.args['effects'].split(',')]
        else:
            effects = []

        # Applies the independent effects.
        for e in effects:
            try:
                if e in ['QUADRICULATE','GRAYSCALE','CROP','NEGATIVE','GREENING','REDDENING','BLUENING']:
                    img = apply_filter(img, e) or img

                elif e in ['ROTATE90','ROTATE180','ROTATE270']:
                    img = rotate_image(img, int(e[6:])) or img
                elif e == 'FACES':
                    img = see_faces(fullfilename, recognize(fullfilename))
                elif e == 'FILLFACES':
                    img = see_faces(fullfilename, recognize(fullfilename), 'fill')
            except:
                pass

        # Applies the intertwined effects.
        try:
            if 'width' in request.args and 'height' in request.args:
                width = int(request.args['width'])
                height = int(request.args['height'])
                resize_image(img, width=width, height=height)
        except:
            raise
            pass

        new_file_name = '%s/%s' % (DOWNLOAD_FOLDER, filename)
        save_image(img, new_file_name)

        return new_file_name

    except Exception as e:
        raise
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
    app.run(host= '0.0.0.0', port=9999)
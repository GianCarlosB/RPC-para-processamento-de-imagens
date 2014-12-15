# -*- coding: utf-8 -*-
import Image
import numpy

def load_image(infile):
    '''
        Loads an image file. Returns the image already read or None on failure.
    '''
    try:
        im = Image.open(infile)
        return im
    except:
        return None

def save_image(image, file_name):
    '''
        Save the image with the specified name. Returns the file name itself informed or None on failure.
    '''
    try:
        image.save(file_name)
        return file_name
    except:
        return None

def resize_image(image, width=None, height=None):
    '''
        Resizes the image. If one of the parameters (width or height) is omitted or invalid,
        the output image will be proportional to another parameter.
        Returns a copy of the image on success or None on failure.
    '''
    # Maintains the proportion of the original image, if necessary.
    # In the absence of the two parameters or non-numeric values,
    # the exception generated will result in return None.
    try:
        w,h = image.size
        ratio = float(w)/h

        if not width:
            width = int(ratio * height)
        if not height:
            height = int(width / ratio)
    except:
        return None

    # Resize the image.
    try:
        return image.resize((width, height))
    except:
        return None

def rotate_image(image, angle):
    '''
        Returns a copy of the image rotated at angles of 90, 180 or 270 degrees.
        Any other value is ignored.
        On failure, returns None.
    '''
    try:
        if angle in [90, 180, 270]:
            return image.rotate(angle)
    except:
        return None

def apply_filter(image, filter):
    '''
        Applies a certain filter to the image.
        Returns the image with the filter applied, None if there is error or the chosen filter does not exist.
    '''
    try:
        # Converts the image sent to the Numpy array format.
        arr = numpy.array(image)

        # Transforms the image into squares of up to 10 pixels.
        if filter == 'QUADRICULATE':
            arr[::10] = 255
            arr[:,::10] = 255
            return Image.fromarray(arr)

        # Transforms an image to grayscale.
        elif filter == 'DECOLORIZE':
            aux = numpy.zeros(arr.shape, dtype=numpy.uint8)
            aux[...,:] = arr>128
            return Image.fromarray(aux)

        # Crops the image trimming the edges that are only black.
        elif filter == 'CROP':
            # Checks which rows and columns have a value other than zero.
            m,n,p = arr.nonzero()
            # Determines the rows and columns to limit the standard sought.
            mmin = m.min()
            mmax = m.max()
            nmin = n.min()
            nmax = n.max()
            # Sets the size of the resulting cutting matrix.
            H,W = mmax - mmin + 1, nmax - nmin + 1
            aux = numpy.empty((H,W))
            # Makes a copy of the row and columns desired data.
            aux = arr[mmin : mmax + 1, nmin : nmax + 1]
            return aux
    except:
        raise
        return None


if __name__=='__main__':
    img = load_image('teste.jpg')

    '''
    cp1 = resize_image(img, width=50)
    cp2 = resize_image(img, height=100)
    cp3 = resize_image(img, 50, 50)
    cp4 = resize_image(img)

    print save_image(cp1, 'cp1.jpg')
    print save_image(cp2, 'cp2.jpg')
    print save_image(cp3, 'cp3.jpg')
    print save_image(cp4, 'cp4.jpg')

    cp5 = rotate_image(img,90)
    cp6 = rotate_image(img,180)
    cp7 = rotate_image(img,270)

    print save_image(cp5, 'cp5.jpg')
    print save_image(cp6, 'cp6.jpg')
    print save_image(cp7, 'cp7.jpg')

    '''

    cp8 = apply_filter(img, 'QUADRICULATE')
    cp9 = apply_filter(img, 'DECOLORIZE')
    cp10 = apply_filter(img, 'CROP')
    
    print save_image(cp8, 'cp8.jpg')
    print save_image(cp9, 'cp9.jpg')
    print save_image(cp10, 'cp10.jpg')

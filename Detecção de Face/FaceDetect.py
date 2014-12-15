# -*- coding: utf-8 -*-
import cv2
import Image
import numpy

# Caminho padrão para o o haar cascade
CASC_PATH = 'haarcascade_frontalface_default.xml'

def desenha(entrada,saida, coordenadas, mode=None):
	try:
		img = numpy.array(Image.open(entrada))

		for c in coordenadas:
			if mode=='fill':
				# Red layer.
				img[c[1]:c[1]+c[2], c[0]:c[0]+c[2], 0] = 255
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

		Image.fromarray(img).save(saida)
	except:
		raise

def reconhecimento(imagePath, cascPath = CASC_PATH, sf = 1.1, mn = 5, ms = (30, 30), f = cv2.cv.CV_HAAR_SCALE_IMAGE):
    # Criando o haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Lendo a imagem
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectando as faces na imagem
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=sf,
    minNeighbors=mn,
    minSize=ms,
    flags=f
    )

    # Retorna uma mensagem com as coordenadas das faces encontradas
    return faces

if __name__=='__main__':
	l = reconhecimento('pessoas.jpeg','haarcascade_frontalface_default.xml')
	desenha('pessoas.jpeg', 'caras1.jpg', l)
	desenha('pessoas.jpeg', 'caras2.jpg', l, 'fill')

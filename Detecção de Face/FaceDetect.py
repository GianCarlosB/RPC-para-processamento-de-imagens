# -*- coding: utf-8 -*-
import cv2

# Caminho padrão para o o haar cascade
CASC_PATH = 'haarcascade_frontalface_default.xml'

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

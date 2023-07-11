import cv2
import pickle
import numpy as np

# me traigos los espacios del tablero que se guardaron
estacionamientos = []
with open('espacios.pkl', 'rb') as file:
    estacionamientos = pickle.load(file)

# leo el video
video = cv2.VideoCapture('video.mp4')

while True:
    # inicializo el valor de los espacios vacios
    spaces=0

    # leo el frame
    check, img = video.read()

    # verifico que se lea bien
    if not check:
        break

    # transformo el frame a escala de grises
    imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # aplico un threshold adaptativo para que se vea mejor
    imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # aplico un filtro de mediana para eliminar el ruido
    imgMedian = cv2.medianBlur(imgTH, 5)
    # aplico una dilatacion para que los espacios se vean mas grandes y eliminar pequeños espacios
    kernel = np.ones((5,5), np.int8)
    imgDil = cv2.dilate(imgMedian, kernel)

    # recorro los espacios y cuento los pixeles blancos
    for x, y, w, h in estacionamientos:
        # recorto el espacio que necesito y cuento los pixeles blancos
        espacio = imgDil[y:y+h, x:x+w]
        # cuento los pixeles blancos que me dice si esta vacio o no
        count = cv2.countNonZero(espacio)
        # pongo el numero de espacio en el frame
        cv2.putText(img, str(count), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        # si el espacio esta vacio lo pinto de verde y sumo
        if count < 1500:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            spaces+=1


    print("spaces", spaces)

    cv2.imshow('video', img)
    cv2.waitKey(10)

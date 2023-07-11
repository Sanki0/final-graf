# en este archivo se guardara las posiciones

import cv2
import pickle

# se lee la imagen del tablero de ajedrez
img = cv2.imread('frame_at_10s.jpg')

espacios = []

# veo la cantidad de espacios en las dos primeras filas del tablero de cada jugador
for x in range(32):
    # con esto puedo encuadrar el espacio que necesito
    espacio = cv2.selectROI('espacio', img, False)
    cv2.destroyWindow('espacio')
    espacios.append(espacio)
    print(len(espacios))

    # esto es para que siempre aparezcan los espacios en color azul
    for x, y, w, h in espacios:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

try:
    with open('espacios.pkl', 'wb') as file:
        pickle.dump(espacios, file)
    print("File saved successfully.")
except Exception as e:
    print("Error occurred while saving the file:", str(e))
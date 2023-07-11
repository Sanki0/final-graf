import cv2
import mediapipe as mp
import math
import time

# Cargar el video
video = cv2.VideoCapture('tenet.mp4')

# Inicializamos el facemesh de mediapipe
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
mpDraw = mp.solutions.drawing_utils

# Inicializamos algunas variables
estado = 'X'  # El estado
estado_actual = ''  # El estado que se actualizara
open_vowel_counter = 0  # contador para abiertas
close_vowel_counter = 0  # contador para cerradas

# Variables globales para el angulo de la boca
open_vowel_angle_threshold = 10
close_vowel_angle_threshold = 2

while True:
    # lee el frame
    check, img = video.read()

    # verifica que se lea bien
    if not check:
        break

    # se hace un resize del frame
    img = cv2.resize(img, (1000, 720))
    h, w, _ = img.shape

    # pasamos el facemesh model por el frame
    results = faceMesh.process(img)

    if results:
        if not results.multi_face_landmarks:
            continue

        for face in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, face, mpFaceMesh.FACEMESH_FACE_OVAL)
            # Tratamos de encontrar frames que nos sirvan para esta tarea
            l1x, l1y = int((face.landmark[61].x) * w), int((face.landmark[61].y) * h)
            l2x, l2y = int((face.landmark[291].x) * w), int((face.landmark[291].y) * h)
            l3x, l3y = int((face.landmark[14].x) * w), int((face.landmark[14].y) * h)

            # Calulo del angulo y de la distancia entre labio superioe e inferior
            distL = math.hypot(l1x - l2x, l1y - l2y)
            angle = math.degrees(math.atan2(l3y - l1y, l3x - l1x))

            # Ponemos condiciones para los casos de palabra abierta
            if angle > open_vowel_angle_threshold and distL > 5:
                print("angle", angle)
                print("distL", distL)
                estado = 'Open'

                # vemos si cambio el estado a cambiado y aumentamos el contador pata palabra abierta
                if estado != estado_actual:
                    open_vowel_counter += 1

            # Ponemos condiciones para los casos de palabra cerrada
            if angle < close_vowel_angle_threshold and distL > 5:
                estado = 'Close'

                # vemos si cambio el estado a cambiado y aumentamos el contador pata palabra cerrada
                if estado != estado_actual:
                    close_vowel_counter += 1

            estado_actual = estado

    # Display the image with the detected state
    cv2.imshow('Detector', img)
    cv2.waitKey(10)

# Print the total number of detected open and close vowels
print(f"Total Open Vowels: {open_vowel_counter}")
print(f"Total Close Vowels: {close_vowel_counter}")

# Close all windows
cv2.destroyAllWindows()

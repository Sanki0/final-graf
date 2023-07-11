# en este archivo estamos guardando el tablero de juego en una imagen

import cv2

video = cv2.VideoCapture('video.mp4')

# Señalo que quiero el frame que se encuentra en el segundo 10
target_time = 10

# calculo que frame se encuentra en ese segundo
frame_rate = video.get(cv2.CAP_PROP_FPS)
target_frame = int(target_time * frame_rate)

# pongo el video en el frame que calcule
video.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

# guardo el frame en una imagen
check, img = video.read()
cv2.imwrite('frame_at_10s.jpg', img)

# Release the video object and close any open windows
video.release()
cv2.destroyAllWindows()

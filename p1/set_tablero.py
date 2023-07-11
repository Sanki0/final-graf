import cv2

video = cv2.VideoCapture('video.mp4')

# Set the desired time frame in seconds
target_time = 10

# Calculate the frame number for the desired time frame
frame_rate = video.get(cv2.CAP_PROP_FPS)
target_frame = int(target_time * frame_rate)

# Set the video's current frame to the desired frame
video.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

# Read and save the frame
check, img = video.read()
cv2.imwrite('frame_at_10s.jpg', img)

# Release the video object and close any open windows
video.release()
cv2.destroyAllWindows()

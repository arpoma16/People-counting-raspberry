from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
 
# inicializa la cámara
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))

# espera un tiempo a aque la cámara esté lista
time.sleep(0.1)


writer= cv2.VideoWriter('/home/pi/people_counting.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 20, (camera.resolution[0],camera.resolution[1]))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # tomamos el array de numpy que reprsenta la image
    image = frame.array
	# muestra el frame
    cv2.imshow("Frame", image)
    np_img = np.array(image)

    writer.write(np_img)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == 27:
        break

print(np_img.shape)
writer.release()
camera.close()
cv2.destroyAllWindows()

#if __name__ == '__main__':
    


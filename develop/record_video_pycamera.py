# revisar esto https://stackoverflow.com/questions/29583533/videocapture-open0-wont-recognize-pi-cam/37530016#37530016
#para ver como configurar la raspberry pi.
# we can use this https://stackoverflow.com/questions/41991097/live-image-processing-with-opencv-and-raspberry-pi
# for readinfd
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
# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0
 


writer= cv2.VideoWriter('/home/pi/people_counting.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (camera.resolution[0],camera.resolution[1]))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # tomamos el array de numpy que reprsenta la image
    image = frame.array
	# muestra el frame
    cv2.imshow("Frame", image)
    np_img = np.array(image)
    
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    print("fps:"+str(int(fps)))
    writer.write(np_img)

    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == 27:
        break

print(np_img.shape)
writer.release()
camera.close()
cv2.destroyAllWindows()

#if __name__ == '__main__':
    


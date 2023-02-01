# revisar esto https://stackoverflow.com/questions/29583533/videocapture-open0-wont-recognize-pi-cam/37530016#37530016
#para ver como configurar la raspberry pi.
# we can use this https://stackoverflow.com/questions/41991097/live-image-processing-with-opencv-and-raspberry-pi
# for readinfd
from picamera.array import PiRGBArray
from picamera import PiCamera
from flask import Flask
from flask import render_template
from flask import Response
import numpy as np
import time
import cv2

app = Flask(__name__)
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
 
def generate():
    global new_frame_time,prev_frame_time
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # tomamos el array de numpy que reprsenta la image
        np_img = np.array(frame.array)
        
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        print("fps:"+str(int(fps)))

        rawCapture.truncate(0)

        (flag, encodedImage) = cv2.imencode(".jpg", np_img)
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encodedImage) + b'\r\n')


@app.route("/")
def index():
     return render_template("index.html")
@app.route("/video_feed")
def video_feed():
     return Response(generate(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
if __name__ == "__main__":
     app.run(host="0.0.0.0",debug=False)



camera.close()

    


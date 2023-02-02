# revisar esto https://stackoverflow.com/questions/29583533/videocapture-open0-wont-recognize-pi-cam/37530016#37530016
#para ver como configurar la raspberry pi.
# we can use this https://stackoverflow.com/questions/41991097/live-image-processing-with-opencv-and-raspberry-pi
# for readinfd
from picamera2 import Picamera2
from flask import Flask
from flask import render_template
from flask import Response
import numpy as np
import time
import cv2

app = Flask(__name__)
# inicializa la cámara
camera = Picamera2()
camera.preview_configuration.main.size=(640,720)
camera.preview_configuration.main.format="RGB888"
camera.preview_configuration.Transform(hflip=1, vflip=1)
camera.preview_configuration.align()
camera.configure("preview")
camera.start()

# espera un tiempo a aque la cámara esté lista
time.sleep(0.1)
# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0
 


writer= cv2.VideoWriter('/home/pi/people_counting.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (640,480))


def generate():
    global new_frame_time,prev_frame_time
    # capture frames from the camera
    while True:
        # tomamos el array de numpy que reprsenta la image
        np_img = camera.capture_array()        
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        print("fps:"+str(int(fps)))
        writer.write(np_img)
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


writer.release()
camera.close()

    


from flask import Flask
from flask import render_template
from flask import Response
import cv2
from threading import Thread

app = Flask(__name__)
img_stream_send = None

def generate():
     global img_stream_send
     while True:
          if img_stream_send != None:
               (flag, encodedImage) = cv2.imencode(".jpg", img_stream_send)
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

def setframeflask(img):
     global img_stream_send
     img_stream_send= img

def flaskThread():     
     app.run(host="0.0.0.0",debug=False)
     


if __name__ == "__main__":
     Thread.start_new_thread(flaskThread, ())
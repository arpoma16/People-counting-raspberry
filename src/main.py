from threading import Thread
import numpy as np
import cv2
import time
import os

from Argparser import Argparser
from PeopleCounting import Peoplecount

from flask import Flask
from flask import render_template
from flask import Response



defaults = {
		"platform": os.name,
		"path": os.getcwd(),
		"file_in":"../data/Video_example01.mp4"
}

#--------------------
peopleobj = None
app = Flask(__name__)

def generate():
     global peopleobj
     while True:
          if peopleobj is not None:
               (flag, encodedImage) = cv2.imencode(".jpg", peopleobj.getimage())
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

def flaskThread():     
     app.run(host="0.0.0.0",debug=False)

def main():
     global peopleobj
     args = Argparser(defaults)
     print(args)
     print(args["source"])
     peopleobj = Peoplecount(args)
     peopleobj.start()
     app.run(host="0.0.0.0",debug=False)

if __name__ == "__main__":
	main()
	


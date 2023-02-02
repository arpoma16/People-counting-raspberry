import cv2
import os

from argparser import Argparser
from PeopleCounting import Peoplecount

from flask import Flask
from flask import render_template
from flask import Response
from flask import request,jsonify,make_response



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


@app.route('/getdata/B', methods=['GET','POST'])
def data_get1():
    global peopleobj
    if request.method == 'GET': # POST 
        if peopleobj is not None:
            input_count,output_count = peopleobj.getcount()
        else:
            input_count = 0
            output_count = 0
        return  make_response(jsonify({"entrada":input_count,"salida": output_count}),200)


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
	


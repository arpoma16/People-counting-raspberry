from threading import Thread
import cv2,time

class VideoStream:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src, usePiCamera=False, resolution=(320, 240),framerate=32):
        self.picamera = usePiCamera
        self.stopped = False
        self.grabbed = None
        self.camera = None
        if usePiCamera:
            from picamera2 import Picamera2
            from libcamera import Transform

            self.camera = Picamera2()
            self.camera.preview_configuration.main.size=(800,600)
            self.camera.preview_configuration.main.format="RGB888"
            self.camera.preview_configuration.transform =Transform(hflip=1, vflip=1)
            self.camera.preview_configuration.align()
            self.camera.configure("preview")
            self.camera.start()
            self.grabbed =True
            self.frame = self.camera.capture_array() 
        else:
			#self.stream = WebcamVideoStream(src=src)
            self.stream = cv2.VideoCapture(src)
            (self.grabbed, self.frame) = self.stream.read()

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        if self.usePiCamera:
            return ( True , self.camera.capture_array())
        else:
            return self.stream.read()
    def update(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                time.sleep(.02)
        self.stream.release()

    def getframe(self):
        return (self.grabbed, self.frame)


    def stop(self):
        self.stopped = True
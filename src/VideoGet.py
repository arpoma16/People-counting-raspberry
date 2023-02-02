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
        if usePiCamera:
            from pivideostream import PiVideoStream
            self.stream = PiVideoStream(resolution=resolution,framerate=framerate)
        else:
			#self.stream = WebcamVideoStream(src=src)
            self.stream = cv2.VideoCapture(src)
            (self.grabbed, self.frame) = self.stream.read()

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

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
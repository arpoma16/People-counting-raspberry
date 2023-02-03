from random import randint
import time
import cv2
import numpy as np

# crea  el objeto de traking con junto a la de la clase persona 
# se actualiza  cada vez la imagen de la persona 
# se compara  la posicio del tracking con el del algoritmo de deteccion.
# tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
"""        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()"""
class MyPerson:
    #self.tracks = []
    #init  se inicializara los valores de  (x,y,w,h,) o bbox ,imagen  lo cual se necesitara para el tracking 
    def __init__(self, i, xi, yi, max_age):
        #self.tracker = cv2.TrackerKCF_create()
        #self.tracker.init(image, bbox)
        self.distx = 0
        self.disty = 0
        self.kfObj = KalmanFilter()
        self.predictedCoords = np.array([[xi],[yi]],dtype=np.float32)
        self.kfObj.first_detected(xi, yi)
        self.kfObj.predic()
        self.kfObj.correct(self.predictedCoords)
        self.predictedCoords = self.kfObj.Estimate(xi, yi)
        self.tracker =cv2.TrackerMIL_create()
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
    def init_opencv_traker(self,frame,bbox):
        self.tracker.init(frame, bbox)
    def update_opencv_traker(self,frame):
        return self.tracker.update(frame)
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getState(self):#significa que cruzo l cualquiera de las dos lineas
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
        self.predictedCoords = self.kfObj.Estimate(xn, yn)
        if len(self.tracks) >= 2:
            self.distx = self.tracks[-1][0] - self.tracks[-2][0] + self.distx 
            self.disty = - self.tracks[-1][1] + self.tracks[-2][1] + self.disty
            #print("id:" + str(self.i) + " disty : "+ str(self.disty))
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done

    def getUp(self,ref,option=True):
        if option:
            if self.distx > ref :
                return True
            else: 
                return False
        else:
            if self.disty <(- ref):
                return True      
            else:
                return False
        

    def getDown(self,ref,option=True):
        if option:
            if self.distx < (- ref):
                return True
            else:
                return False
        else:
            if self.disty > ( ref):
                return True
            else:
                return False            

    def getAge(self):
        return self.age


    def going_UP(self,mid_start,mid_end):# averigua si cruzo la linea y la linea 2 en la misma  direccion
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][0] > mid_end and self.tracks[-2][0] <= mid_end: #cruzo la linea
                    self.state = '1'
                    self.dir = 'up'
                    print('up')
                    return True
            else:
                return False
        else:
            return False
    
    def going_DOWN(self,mid_start,mid_end):#averigua si cruzo la linea  
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][0] > mid_start and self.tracks[-2][0] <= mid_start: #cruzo la linea
                    self.state = '1'
                    self.dir = 'down'
                    print('down')
                    return True
            else:
                return False
        else:
            return False

    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
            #print('done')
        return True
    """def prediction(self, image):
        self.ok, self.newbox = self.tracker.update(image)
        return self.newbox"""
    def prediction(self):
        return self.predictedCoords

    def predict(self):
        self.predictedCoords = self.kfObj.predic()
        return self.predictedCoords

class MultiPerson:
    def __init__(self, persons, xi, yi):
        self.persons = persons
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        
# Instantiate OCV kalman filter
class KalmanFilter:
    def __init__(self):
        q = 1e-5   #  process noise covariance
        r = 0.01 #  measurement noise covariance, r = 1
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.processNoiseCov     = q* np.eye(4, dtype=np.float32)   # Q         
        self.kf.measurementNoiseCov = r* np.eye(2, dtype=np.float32)   # R
        self.kf.errorCovPost  = np.eye(4, dtype=np.float32)            # P0 = I
        #self.kf.errorCovPost = np.ones((1, 1))
        #self.kf.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03
    def Estimate(self, coordX, coordY):
        ''' This function estimates the position of the object'''
        self.kf.correct(np.array([[coordX],[coordY]],dtype=np.float32))
        return self.kf.predict()

    def correct(self, cordenate):
        self.kf.correct(cordenate)

    def predic(self):
        return self.kf.predict()
    def first_detected(self, coordX, coordY):
        self.kf.statePost=np.array([[coordX],[coordY],[0.],[0.]],dtype=np.float32)
        #self.kf.statePost =  np.array([[np.float32(coordX)], [np.float32(coordY)]])    
        

class backproyection:
    def __init__(self, imgf):
        self.hsv = cv2.cvtColor(imgf,cv2.COLOR_BGR2HSV)
        self.roihist = cv2.calcHist([self.hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
        cv2.normalize(self.roihist,self.roihist,0,255,cv.NORM_MINMAX)
    def busqueda(self, img0):
        self.hsvt = cv2.cvtColor(img0,cv2.COLOR_BGR2HSV)
        self.dst = cv2.calcBackProject([self.hsvt],[0,1],self.roihist,[0,180,0,256],1)
        disc = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
        cv.filter2D(dst,-1,disc,dst)
        # threshold and binary AND
        ret,thresh = cv.threshold(dst,50,255,0)

class blobles:
    def __init__(self,bid, x, y, w, h,color):
        self.i = bid
        self.x = x
        self.y = y
        self.w = w
        self.h = h 
        self.people = 0
        self.color = color
        self.tracks = []
        self.tracks.append([self.x,self.y,self.w,self.h])

    def setpeople(self, p):
        self.people = p

    def updateCoords(self, x, y, w, h):
        self.tracks.append([self.x,self.y,self.w,self.h])
        self.x = xn
        self.y = yn

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getW(self):
        return self.w
    def getH(self):
        return self.h

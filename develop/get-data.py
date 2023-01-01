import numpy as np
import cv2
import os
import time
from generate_xml import write_xml


image_folder = 'database'
image_folder1 = 'database1'
savedir = 'anotation' 
obj = 'persona'
num_img = 1
img = None
tl_list = []
br_list = []
object_list = []



def nothing(x):
	pass

def write_imagen():
	global img
	bbox = cv2.selectROI("canny",image)
	yb = int(bbox[1])
	hb = int(bbox[3])
	xb = int(bbox[0])
	wb = int(bbox[2])
	rectanglebox(xb , yb, wb, hb)
	autoxml()
	#crop_img = gray[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
	#cv2.imshow("cropped", crop_img)
	#resized_image = cv2.resize(crop_img, (50, 50))


def rectanglebox(xi ,yi, wi, hi):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(xi), int(yi)))
    br_list.append((int(xi + wi), int(yi + hi)))
    object_list.append(obj)

def autoxml():
	global object_list
	global tl_list
	global br_list
	global image
	global img
	global num_img
	global height
	global width
	global depth 
	cv2.imwrite(image_folder+"/"+str(num_img)+".jpg",img)
	cv2.imwrite(image_folder1+"/"+str(num_img)+".jpg",image)
	write_xml(image_folder, str(num_img), object_list, tl_list, br_list, savedir,height, width, depth)
	num_img +=1
	tl_list = []
	br_list = []
	object_list = []


if __name__ == '__main__':

	face_cascade = cv2.CascadeClassifier('cascade-13.xml')
	cv2.namedWindow('canny')
	cv2.createTrackbar('time', 'canny', int(500), int(1000), nothing)
	cap = cv2.VideoCapture('edit2.mp4')
	if not os.path.isdir(image_folder):
		os.makedirs(image_folder)
	while(True):
		mysleep = cv2.getTrackbarPos('time', 'canny')
		ret, image = cap.read()
		rets, img = cap.read()
		height, width, depth = image.shape
		#image = cv2.resize(image, (600, 600))
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 7,12)
		#mostar imagen
		#time.sleep(mysleep/1000.0)

		haard = False
		for (x,y,w,h) in faces:
			cx = int(x + w / 2)
			cy = int(y + h / 2)
			if w > 50:
				haard = True
				cv2.rectangle(image,(x,y),(x+w,y+h),(125,255,0),2)
				cv2.circle(image,(cx,cy), 5, (0,0,255), -1)
				rectanglebox(x , y, w, h)
		if haard:
			autoxml()

		cv2.imshow("canny",image)
		time.sleep(mysleep/1000.0)
		#captura dato
		k = cv2.waitKey(1) & 0xFF
		#pausa el video  la imagen positiva 
		if k == ord("w"):
			while(True):
				k1 = cv2.waitKey(1) & 0xFF
				if k1 == ord("r"):
					print("presionado R")
					break
				if k1 == ord("q"):
					print("presionado Q")
					write_imagen()
		if k == 27:
			break
	cap.release()
	cv2.destroyAllWindows()
import numpy as np
import cv2
import os
import time
 


image_foldel = 'pos'
num_img = 840

#image_foldel = 'negative'
#num_img = 148


def nothing(x):
	pass

def write_imagen():
	global image
	global gray
	global num_img
	bbox = cv2.selectROI("canny",image)
	crop_img = gray[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
	cv2.imshow("cropped", crop_img)
	resized_image = cv2.resize(crop_img, (50, 50))
	cv2.imwrite(image_foldel+"/"+str(num_img)+".jpg",resized_image)
	num_img +=1


if __name__ == '__main__':

	face_cascade = cv2.CascadeClassifier('cascade-9.xml')
	cv2.namedWindow('canny')
	cv2.createTrackbar('time', 'canny', int(500), int(1000), nothing)
	cap = cv2.VideoCapture('edit2.mp4')
	if not os.path.isdir(image_foldel):
		os.makedirs(image_foldel)
	while(True):
		mysleep = cv2.getTrackbarPos('time', 'canny')
		ret, image = cap.read()
		#image = cv2.resize(image, (600, 600))
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 7,12)
		#mostar imagen
		#time.sleep(mysleep/1000.0)

		for (x,y,w,h) in faces:
			cv2.rectangle(image,(x,y),(x+w,y+h),(125,255,0),2)
			cx = int(x + w / 2)
			cy = int(y + h / 2)
			cv2.circle(image,(cx,cy), 5, (0,0,255), -1)
			#mysleep = 100

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
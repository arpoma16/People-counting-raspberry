#https://www.youtube.com/watch?v=Zm_fAm4cUPY
import numpy as np
import cv2
import time
import PersonMod1
from matplotlib import pyplot as plt

#Contadores de entrada y salida
cnt_up   = 0
cnt_down = 0
areaTH = 1000
countup = 0
countdown = 0
frame = 0
bid =0
color = ('b','g','r')

#Variables
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
burbles = []
max_p_age = 5
pid = 1 #id de la persona 
predictedCoords = np.zeros((2, 1), np.float32)
#function for createTrackbar
def nothing(x):
	pass

colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]


#background sustraction
fgbg = cv2.createBackgroundSubtractorMOG2(history = 3000, varThreshold = 60,detectShadows = True)
#fgbg = cv2.createBackgroundSubtractorKNN(history = 1000,dist2Threshold = 800.0,detectShadows = True)

kernelOp = np.ones((5,5),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((20,20),np.uint8)

overpeople_cascade = cv2.CascadeClassifier('cascade-14.xml')
cap = cv2.VideoCapture('edit2.mp4')
cv2.namedWindow('Counter-people')
# propiedades de vi
w = cap.get(3)
h = cap.get(4)
imgArea = h*w
areaTH = imgArea/250
line_down_color = (255,0,0)
line_up_color = (0,0,255)

# creacion de trackbar
cv2.createTrackbar('time', 'Counter-people', int(500), int(1000), nothing)
cv2.createTrackbar('downer', 'Counter-people', int(w/2), int(w), nothing)
cv2.createTrackbar('upper', 'Counter-people', int(5*w/8), int(w), nothing)


while(cap.isOpened()):
	frame += 1
	print(' ')
	print(' ')
	print('frame : ' + str(frame) + '   DOWN: '+ str(countdown) +'   UP: '+ str(countup))
	print(' ')
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#img = cv2.equalizeHist(img)

	for i in persons:
		i.age_one()# edad de la persona en un img  age = 1

	line_down = cv2.getTrackbarPos('downer','Counter-people')
	line_up = cv2.getTrackbarPos('upper','Counter-people')
	mysleep = cv2.getTrackbarPos('time', 'Counter-people')

	if line_down > line_up:
		cv2.setTrackbarPos('downer', 'Counter-people', line_up -1)

	#aplicacion del background sustraction
	fgmask2 = fgbg.apply(img)
	#backGnd = fgbg.getBackgroundImage() # fondo
	#Binariazcion para eliminar sombras (color gris)
	try:
		ret,imBin2 = cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
		#Opening (erode->dilate) para quitar ruido.
		mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
		#Closing (dilate -> erode) para juntar regiones blancas.
		mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
	except:
		print('EOF')
		print('UP:',cnt_up)
		print('DOWN:',cnt_down)
		break

	_, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	thresh = cv2.merge((mask2,mask2,mask2))
	res = cv2.bitwise_and(img,thresh)

	exist = True
	for cnt in contours0:
		area = cv2.contourArea(cnt)
		x,y,w,h = cv2.boundingRect(cnt)

		#cx = int(x + w / 2)
		#cy = int(y + h / 2)
		#bbox = (x, y, w, h)

		if area > areaTH and w > 50 and h > 50:
			"""contorno = res[y:y+h, x:x+w]
			mascara = mask2[y:y+h, x:x+w]
			cv2.imshow('contour',contorno)
			for i,col in enumerate(color):
				histr = cv2.calcHist([contorno],[i],mascara,[256],[0,256])
				plt.plot(histr,color = col)
				plt.xlim([0,256])
			plt.show()"""

			newblob = True 
			for blob in burbles:
				#if  
				newblob = False


			if newblob == True:
				b = PersonMod1.blobles(bid,x,y,w,h,10)
				burbles.append(b)# pone  en la ultima posicion
				bid += 1 

			# si dos borbujas estan cerca y tienen el mismo color 
			# tomar encuanta burbujar con un ancho >50 h>50

			exist = False
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.circle(img,(int(x+w/2),int(y+h/2)), 5, (0,255,0), -1)
		else:
			cv2.rectangle(mask2,(x,y),(x+w,y+h),(0),-1)
	if exist:
		print('NO CONTORNO')
		for blob in burbles:
			index = burbles.index(blob) #devielve la posicion del objeto
			burbles.pop(index) #Elimina el objeto de la  index 
			#print('timedOut1:  ',i.getId())
			del blob




	results = overpeople_cascade.detectMultiScale(gray, 8, 5)
	if ret:
		for (color, result) in zip(colors, results):#obtiene la poscicion de los haarcascade encontrados 
			(x,y,w,h) = result
			cx = int(x + w / 2)
			cy = int(y + h / 2)
			bbox = (x, y, w, h) 
			#box = (x-10, y-10, w+20, h+20) 


			if w > 50:
				new = True
				if cx in  range (line_down-200,line_up+100):
					for i in persons:
						if  i.getX()  in range(x, x+w) and i.getY()  in range(y, y+h):
							print("actualiza cordenadas id: " ,i.getId(),"bbox", bbox)
							new = False
							i.updateCoords(cx,cy)# age = 0
							predictedCoords = i.prediction()
							cv2.circle(img, (predictedCoords[0], predictedCoords[1]), 20, [0,255,255], 2, 8)
							break
						if len(i.getTracks()) >= 2:
							if (i.getX() > line_up) and  i.getUp(30) and (i.getTracks()[0][0])<line_up:
								countup +=1
								i.setDone()
							if (i.getX() < line_down) and  i.getDown(30) and (i.getTracks()[0][0])>line_down :
								countdown +=1
								i.setDone()
						if i.timedOut():#return done 
							index = persons.index(i) #devielve la posicion del objeto
							persons.pop(index) #Elimina el objeto de la  index 
							print('timedOut1:  ',i.getId())
							del i
					if new == True:
						p = PersonMod1.MyPerson(pid,cx,cy, max_p_age)
						persons.append(p)# pone  en la ultima posicion
						pid += 1 
				# muestra las detecciones por el  haar cascade
				cv2.circle(img,(cx,cy), 5, (0,0,255), -1)
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				# persona dentro de la zona de interez





	for i in persons:
		if len(i.getTracks()) >= 2:
			pts = np.array(i.getTracks(), np.int32)
			pts = pts.reshape((-1,1,2))
			img = cv2.polylines(img,[pts],False,i.getRGB())
		cv2.putText(img, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
		if i.getAge() > 0 :# buscar la  burbuja que lo pueda contener y actualizar su punto con tracking  con el movimiento relativo de la burbuja
			predictedCoords = i.predict()
			cv2.circle(img, (predictedCoords[0], predictedCoords[1]), 20, [255,0,255], 2, 8)
			#i.updateCoords(predictedCoords[0], predictedCoords[1])
			posi = True
			for cnt in contours0:
				area = cv2.contourArea(cnt)
				x,y,w,h = cv2.boundingRect(cnt)
				if  i.getX()  in range(x, x+w) and i.getY()  in range(y, y+h):
					posi = False

			if exist or posi:
				if len(i.getTracks()) >= 2:
					if (i.getX() > line_up) and  i.getUp(30) and (i.getTracks()[0][0])<line_up:
						countup +=1
						i.setDone()
					if (i.getX() < line_down) and  i.getDown(30) and (i.getTracks()[0][0])>line_down :
						countdown +=1
						i.setDone()
				index = persons.index(i) #devielve la posicion del objeto
				persons.pop(index) #Elimina el objeto de la  index 
				print('timedOut2:  ',i.getId())
				del i



	#  creacion de las lineas
	pt1 =  [ line_down, 0];
	pt2 =  [ line_down, h];
	pts_L1 = np.array([pt1,pt2], np.int32)
	pts_L1 = pts_L1.reshape((-1,1,2))

	pt3 =  [ line_up, 0];
	pt4 =  [ line_up, h];
	pts_L2 = np.array([pt3,pt4], np.int32)
	pts_L2 = pts_L2.reshape((-1,1,2))
	img = cv2.polylines(img,[pts_L1],False,line_down_color,thickness=2)
	img = cv2.polylines(img,[pts_L2],False,line_up_color,thickness=2)


# mostrar valores
	str_up = 'UP: '+ str(countup)
	str_down = 'DOWN: '+ str(countdown)
	cv2.putText(img, str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
	cv2.putText(img, str_up ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
	cv2.putText(img, str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
	cv2.putText(img, str_down ,(10,90),font,0.5,(255,0,0),1,cv2.LINE_AA)





	#Mostrar o actualizar pantallas	
	cv2.imshow('Counter-people',img)
	#cv2.imshow('Mask',mask2)   
	#cv2.imshow('backGnd',backGnd) 
	cv2.imshow('res',res) 
    #preisonar ESC para salir
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

	#DELAY
	time.sleep(mysleep/1000.0)

#END while(cap.isOpened())
    
#################
#   LIMPIEZA    #
#################
cap.release()
cv2.destroyAllWindows()


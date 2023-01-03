# Entrenamiento de haar cascade

## how use haar cascade

[Example of haar cascade OpenCV](https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html)

## Get data

### Positive imge 

We can get data from a dictionary online or prepare it yourself.
we take a video  with pycamera and  use the  program  __get-image.py__ .

that get the  frame form video and allow to cut the interest objet for after conver to gray-scale  y resize to 50x50 px.

### Negative image

for obtain the positive data we use  the  program  __download-image-link.py__ que descarga images del sitio web __image-net.org__  after conver to gray-scale  y resize to 50x50 px.

## Trainig

[Other way using a external tool](https://www.youtube.com/watch?v=v_cwOq06g9E&t=329s)

[Cascade Classifier Training documentation OpenCV3.4](https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html)

De estas imágenes positivas y negativas se deben obtener un archivo de texto plano(bg.txt) en el cual   tenga la ruta de cada una de las imágenes en el caso de las imágenes negativas

En el caso de las imágenes positivas un archivo (info.dat) en el cual tiene la ruta   de cada una de las imágenes y luego el número de objetos a clasificar que se encuentran en la imagen y luego la posición inicial del rectángulo donde se encuentra el objeto de interés seguido de su ancho y de su alto.Para nuestro caso se recortó la imagen de interés por lo cual el cuadrado es del tamaño de toda la imagen recortada. 

para un conjunto de imagenes positivas
se requiere un archivo info.dat el cual contiene la información de cada uno de las imágenes positivaspor lo cual se procede a ejecutar la siguiente línea de código para crear el archivo vectorial con todas las imágenes positivas juntas.


images positive:

        opencv_createsamples -info info/info.lst -num 24 -w 20 -h 20 -vec positives.vec
where:


info contiene el archive creado por el programa realizado en python llamado download-image-link.py 

bg  contiene el conjunto de imágenes negativas ,

num  contiene el número de imágenes positivas  

w , h  las dimensiones que van ha tener las imágenes 

vec la dirección de donde se va a crear el archivo vectorial que contiene las imágenes positivas.


training:

        opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 300 -numNeg 280 -numStages 10 -w 20 -h 20


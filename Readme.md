# [Counting people with raspberry pi](https://github.com/arpoma16/People-counting-raspberry)

## About

This project is developed like a project of Sistemas Digitales Avanzados of MIERA in Universidad de Sevilla.

This project uses a raspberry py for counting people across a door and sent this data to the internet to TAGOIO using MQTT to send data about counting and alarm in TELEGRAM chat group for when the place is full and the device is turned on and turned off.

This proyect is based on  [People counting HOG + Linear SVM](https://pyimagesearch.com/2018/08/13/opencv-people-counter/) and  [People counting using blob](https://blogs.wcode.org/2015/04/footfall-a-camera-based-people-counting-system-for-under-60/)


This is based on a two-step

    - Object detector ( hard cascade )
    - Object tracker (background subtraction, distance between frames, and Kalman filter)

## Structure

    Project \
        - data      # Videos, images, and sources
        - src       # Scritps & local project modules
        - develop   # for exploratory, tools that help to develop the project
        - deliver   # presentations

## how to use 

Before implementing this project change the .env.example and copy as .env and change it with your data.
Change the values in .env  for your TAGOIO count and token of telegram.

you have to run commands in the src folder like:

    python .\main.py --source picamera

if you want to run it without the web server  you can run the command:

    python .\PeopleCounting.py 


## Dependecies

- python3
- numpy
- opencv [please install in raspberry py like this](https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html)
- flask
- requests
- os
- threading
- random
- time
- dotenv
- argparse
- paho.mqtt
- json
- picamera2 ( only for run in raspberry pi )

you can use requirements.txt

    python3 -m venv venv/
    pip install -r requirements.txt

how use virtualenv

    \venv\Scripts\activate.bat
    \env\Scripts\deactivate.bat
    pip freeze > requirements.txt




## Referents

1. [People counting HOG + Linear SVM](https://pyimagesearch.com/2018/08/13/opencv-people-counter/) - [github proyect](https://github.com/saimj7/People-Counting-in-Real-Time)
1. [People counting using blob](https://blogs.wcode.org/2015/04/footfall-a-camera-based-people-counting-system-for-under-60/) -  [github proyect](https://github.com/WatershedArts/Footfall)
1. [other project](https://github.com/jeffskinnerbox/people-counter)
1. [Haar cascade counting](http://funvision.blogspot.com/2017/01/lbp-cascade-for-head-and-people.html)
1. [Training Hard cascade](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/)
1. [Python with MQTT ]( https://www.emqx.com/en/blog/how-to-use-mqtt-in-python )
1. [Python with Telegram API]( https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/ )
1. [We use virtualenv if you want know more about it](https://realpython.com/python-virtual-environments-a-primer/)
1. [get data for train IA](https://www.youtube.com/watch?v=z_6fPS5tDNU)
1. [unifique picamera and opencv](https://pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/)
1. [py camera work with opencv](https://stackoverflow.com/questions/27950013/i-am-trying-make-the-raspberry-pi-camera-work-with-opencv)

## Crazy ideas for feature

We can use a flask [like this tutorial](https://omes-va.com/videostreaming-flask-opencv-python/) for minimizing the grafical interfaz or disable the graphycal in raspberry py and sett value for feature.
and this [flask with thread](https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/)
## Authors

- [Alvaro Poma.](https://github.com/arpoma16)

- Nelson Molina.
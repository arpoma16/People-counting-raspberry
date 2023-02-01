# Counting people with raspbery pi

## About

This project is developed like a project of Sistemas Digitales Avanzados of MIERA in US.

This project use a rapsbery py for counting-people across a door and sent this data to internet to tago io using mqtt and send a alarm to telegram chat group for  when the place is full and the device is turn on and turn off.

This proyect is based on  [People counting HOG + Linear SVM](https://pyimagesearch.com/2018/08/13/opencv-people-counter/) and  [People counting using blob](https://blogs.wcode.org/2015/04/footfall-a-camera-based-people-counting-system-for-under-60/)

This is based in two step

- Object detector (HOG with SVM, hard cascade)
- Object tracker (corelational filter and distance betwen frames)

## Structure

    Project \
        - data      # Videos, images and sources
        - src       # Scritps & local project modules
        - develop   # for exploratory analysis
        - deliver   # presentations, analisis
        - test

## Usage

Change the values in .env  for your tago count and tocken of telegram.

you have to run command in the root of proyect like:

        python .\src\main.py --source file --file-in data/Video_example01.avi

## Dependecies

- python3
- numpy
- opencv [please install in raspberry py like this](https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html)

you can use requirements.txt

    python3 -m venv venv/
    pip install -r requirements.txt

how use virtualenv

    \venv\Scripts\activate.bat
    \env\Scripts\deactivate.bat
    pip freeze > requirements.txt

## Build

Using rapsbery pi  and pycamera

    python3 people-counting.py 

using a pc and ip camera

    python3 people-counting.py  -souce:ipcamera

the direction of ipcamera have to set in .env
using a pc and video recored .mp4

    python3 people-counting.py  -source:video -path:D:\Master\video.mp4

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

- Alvaro Poma.

- Nelson Molina.
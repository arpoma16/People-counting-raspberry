import os
import argparse

""" This funtion is a parsing mechanism for all types of command
    line argument, switches, and options. """

def Argparser(defaults):

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description='This is  a \
                                 Raspberry Pi + OpenCV people counter')
    
    ap.add_argument("-s", "--source",
                    help="si es camara ip o video.mp4 , no colocar en caso de usar con la pi camera ",
                    nargs=1,
                    required=False,
                    choices=["file","ipcamera","usbcamera", "picamera"],
                    default=["file"])

    ap.add_argument("-i", "--file-in",
                    help="ubicacion del archivo o direccion en caso de camara ip",
                    required=False,
                    default= "..//data//one_people_walking.mp4")
                    #default=defaults["path"] + '/' + defaults["file_in"])

    return vars(ap.parse_args())


if __name__ == '__main__':
    defaults = {
         "platform": os.name,
         "path": os.getcwd(),
         "file_in":"../data/Video_example01.mp4"
    }
    print("defaults values :")
    print(defaults)
    print("Argparser result:")
    print(Argparser(defaults))
    
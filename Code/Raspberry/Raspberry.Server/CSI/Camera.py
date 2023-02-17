#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from threading import Thread
import sys,time,_thread
import datetime
import socket
import asyncio
import picamera
import io
from PIL import Image
import asyncio
from Utils.Event import *

class Camera:
    """
    CSI Camera
    """
    def __init__(self) -> None:
        self.capured_event = Event()

    def start(self):
        with picamera.PiCamera() as camera:
                camera.vflip = True
                camera.hflip = True
                # camera.resolution = (300,200)
                camera.resolution = (640,480)
                camera.framerate = 15
                #camera.start_preview()
                time.sleep(2)
                while True:
                    stream = io.BytesIO()
                    for foo in camera.capture_continuous(stream,format='jpeg',use_video_port=True):
                        time.sleep(0.2)
                        # Truncate the stream to the current position (in case
                        # prior iterations output a longer image)
                        stream.seek(0)
                        data = stream.read()
                        
                        self.connected_event(self,data)
                        '''
                        n = stream.tell()
                        n = len(data)
                        image = Image.open(stream)
                        print('Image is %dx%d' % image.size)
                        image.verify() # Image is verified
                        image = Image.open(image_stream) # open --> verify --> open --> save
                        image.save('a1.jpeg',format('JPEG'))
                        '''
                        stream.seek(0)
                        stream.truncate()
          
      
if __name__ == "__main__":
    camera =  Camera()
    camera.start()
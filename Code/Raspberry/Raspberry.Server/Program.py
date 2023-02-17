#!/usr/bin/python3
# -*- coding:UTF-8 -*-
from TCP.socketcom import *
from L298N.MotorWheel import *
from SG90.CameraTerrace import *
from CSI.Camera import *
from threading import Thread
import sys,time,_thread
import datetime
import socket
import asyncio
import RPi.GPIO as GPIO
import picamera
import io
from PIL import Image
import asyncio

P_BUTTON = 20 # key button pin
api_btn_state = "/api/btn/state"
server = TcpServer("192.168.0.9",32769)
wheel = MotorWheel()
terrace = CameraTerrace()
camera =  Camera()


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(P_BUTTON,GPIO.FALLING,button_state_changed,200)

def button_state_changed(args):
    state = "Button pressed"
    data = f"Push current state: {state}"
    if GPIO.input(P_BUTTON) == GPIO.LOW:
        pass
    for h in list(server._clients.keys()): # dictionary changed size during iteration
        server.send_data(h,data)


def handle_client_connected(sender:TcpServer,host:str):
    print ("√ connected with client at %s" % host)

def handle_client_disconnected(sender:TcpServer,host:str):
    print ("× disConnected with client at %s" % host)

def handle_client_received(sender:TcpServer,host:str,msg:str):
    print(">> %s len: %s from [%s] %s" % (msg, str(len(msg)),host,
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    #wheel.SendCommand(msg)
    terrace.SendCmd(msg)

def handle_exception(sender:TcpServer,exp:str):
    print (exp)


def handle_camera_capured(sender:Camera,data:bytes):
    for h in list(server._clients.keys()):
        # camera.capture(stream, format='jpeg')
        server.send_data(h,data)
        print('data len = %d' % len(data))
    

def TestCamera():
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
                for h in list(server._clients.keys()):
                    # camera.capture(stream, format='jpeg')
                    server.send_data(h,data)
                    print('data len = %d' % len(data))
                    '''
                    n = stream.tell()
                    n = len(data)
                    image = Image.open(stream)
                    print('Image is %dx%d' % image.size)
                    image.verify() # Image is verified
                    image = Image.open(image_stream) # open --> verify --> open --> save
                    image.save('a1.jpeg',format('JPEG'))
                    '''
                # stream.truncate()
                # stream.seek(0)

                stream.seek(0)
                stream.truncate()
          
           


async def main():
    server.connected_event += handle_client_connected
    server.disconnected_event += handle_client_disconnected
    server.received_event += handle_client_received
    server.exception_event += handle_exception
    #_thread.start_new_thread(TestCamera,())
    _thread.start_new_thread(camera.start(),())
    
    camera.capured_event +=handle_camera_capured
    await server.start()

    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
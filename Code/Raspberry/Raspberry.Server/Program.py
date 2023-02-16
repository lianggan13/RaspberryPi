#!/usr/bin/python3
# -*- coding:UTF-8 -*-
from TCP.socketcom import *
from L298N.MotorWheel import *
from SG90.CameraTerrace import *
from threading import Thread
import sys,time,_thread
import datetime
import socket
import asyncio
import RPi.GPIO as GPIO
import picamera

P_BUTTON = 20 # key button pin
api_btn_state = "/api/btn/state"
server = TcpServer("192.168.0.9",32769)
wheel = MotorWheel()
terrace = CameraTerrace()

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

def TestCamera():
    camera = picamera.PiCamera()
    camera.resolution = (300, 200)
    camera.vflip = True
    camera.hflip = True
    #os.system("raspistill -o imgCSI.jpg -t 50 -w 300 -h 200 -rot 180")
    #with picamera.PiCamera() as camera:
    camera.capture("imgCSI.jpg")
    #fhead=os.path.getsize('imgCSI.jpg')
    #with open('imgCSI.jpg','rb') as fp:
    #	for data in fp:
    #		connfd.send(data)
    #time.sleep(0.05)

async def main():
    TestCamera()
    server.connected_event += handle_client_connected
    server.disconnected_event += handle_client_disconnected
    server.received_event += handle_client_received
    server.exception_event += handle_exception
    #await server.start()

    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
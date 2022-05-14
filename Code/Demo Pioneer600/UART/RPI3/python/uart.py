#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import RPi.GPIO as GPIO
import time

M0 = 35
M1 = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(M0,GPIO.OUT)
GPIO.setup(M1,GPIO.OUT)

GPIO.output(M0,GPIO.LOW)
GPIO.output(M1,GPIO.LOW)

#ser = serial.Serial("/dev/ttyAMA0",115200)
ser = serial.Serial("/dev/ttyS0",115200,timeout=2)

print("serial test start ...")
ser.write("Hello Wrold !!!\n".encode("utf-8"))
try:
    while True:
        time.sleep(0.1)
        ser.write(ser.read())
        print(".........")
except KeyboardInterrupt:
    if ser != None:
        ser.close()

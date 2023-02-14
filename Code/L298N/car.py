#!/usr/bin/python
# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
INT1 = 29
INT2 = 31
INT3 = 33
INT4 = 35
B1 = 37
B2 = 39   #GND

# GPIO.cleanup()
GPIO.setwarnings(False)
#M1 左电机 INT1 INT2 TOU1 TOU2
#M2 右电机 INT3 INT4 TOU3 TOU4

class MotorCar:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(INT1,GPIO.OUT)
		GPIO.setup(INT2,GPIO.OUT)
		GPIO.setup(INT3,GPIO.OUT)
		GPIO.setup(INT4,GPIO.OUT)
		GPIO.setup(B1,GPIO.OUT)
		self.stop()
	
	def Forward(self):#M1 M2 正转
		GPIO.output(INT1,GPIO.HIGH)
		GPIO.output(INT2,GPIO.LOW)
		GPIO.output(INT3,GPIO.HIGH)
		GPIO.output(INT4,GPIO.LOW)

	def Back(self):#M1 M2 反转
		GPIO.output(INT1,GPIO.LOW)
		GPIO.output(INT2,GPIO.HIGHw)
		GPIO.output(INT3,GPIO.LOW)
		GPIO.output(INT4,GPIO.HIGH)

	def Right(self):# M1 正转   
		GPIO.output(INT1,GPIO.HIGH)
		GPIO.output(INT2,GPIO.LOW)
		GPIO.output(INT3,GPIO.LOW)
		GPIO.output(INT4,GPIO.LOW)

	def Left(self):#M2 正转    
		GPIO.output(INT1,GPIO.LOW)
		GPIO.output(INT2,GPIO.LOW)
		GPIO.output(INT3,GPIO.HIGH)
		GPIO.output(INT4,GPIO.LOW)

	def Stop(self):
		GPIO.output(INT1,GPIO.LOW)
		GPIO.output(INT2,GPIO.LOW)
		GPIO.output(INT3,GPIO.LOW)
		GPIO.output(INT4,GPIO.LOW)

	def SendCommand(self,cmd):
		try:
			if(cmd == 'w' or cmd == 'W'):
				self.Forward()
			elif(cmd == 's' or cmd == 'S'):
				self.Back()
			elif(cmd == 'a' or cmd == 'A'):
				self.Left()
			elif(cmd == 'd' or cmd == 'D'):
				self.Right()
			elif(cmd == 'f' or cmd == 'F'):
				self.light()
			elif(cmd == '0'):
				self.Stop()
		except KeyboardInterrupt: 
			pass
			GPIO.cleanup()

if __name__ == "__main__":
	try:
		car = MotorCar()
		while True:
			data = input(">>")# raw_input(">>")
			car.SendCommand(data)
	except KeyboardInterrupt: 
		GPIO.cleanup()

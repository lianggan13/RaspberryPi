class Eventsample(object): 
	def __init__(self): 
		self.__eventhandlersample = [] 
	
	def __iadd__(self, Ehandler): 
		self.__eventhandlersample.append(Ehandler) 
		return self
	
	def __isub__(self, Ehandler): 
		self.__eventhandlersample.remove(Ehandler) 
		return self

	def __call__(self, *args, **keywargs): 
		for eventhandlersample in self.__eventhandlersample: 
			eventhandlersample(*args, **keywargs) 
				
class MessToDisplay(object): 
	def __init__(self, Mess): 
		self._tele = Mess 
	
	def PrintM(self): 
		print ("Simple Message for an Event...mess:%s" % self._tele)

class sampleclass(object) : 
	
	def __init__(self) : 
		self.OnEH = Eventsample()  # new --> __init__
		
	def Ehnew(self) : # --> . __call__
		self.OnEH() 
		
	def anotherevent(self,objMeth): # += --> _iadd__
		self.OnEH += objMeth 
		
	def nexteven(self,objMeth) : # -= --> __isub__
		self.OnEH -= objMeth 

def Simulation() : 
	newsample = sampleclass() 
	displayamess = MessToDisplay(100) 
	newsample.anotherevent(displayamess.PrintM) 
	newsample.Ehnew() 	
if __name__ == "__main__":		 
	Simulation()
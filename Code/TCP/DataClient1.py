# DataClient1.py

from builtins import print
from threading import Thread
import sys,time,_thread
import datetime
import socket
import asyncio
import uuid

api_btn_state = "/api/btn/state"

def str2bytes(source):
    return bytes(source, encoding = "utf-8")

def bytes2str(source):
    return str(source, encoding ='utf-8')


class Event(object): 
	def __init__(self): 
		self.__eventhandlers = [] 
	
	def __iadd__(self, Ehandler): 
		self.__eventhandlers.append(Ehandler) 
		return self
	
	def __isub__(self, Ehandler): 
		self.__eventhandlers.remove(Ehandler) 
		return self

	def __call__(self, *args, **keywargs): 
		for handler in self.__eventhandlers: 
			handler(*args, **keywargs) 

class TcpClient:
    """
    Tcp Client

    """    
    def __init__(self,ip="127.0.0.1",port=1918):
        self._id = uuid.uuid4()
        self._ip = ip
        self._port = port
        self.connected_event = Event()
        self.disconnected_event = []
        self.received_event = []

    def start(self):
        time.sleep(2)
        self._isconnected = self.connect()
        if self._isconnected:
            self.start_recv()
        else: 
            self.start()

    def restart(self):
        self.close()
        self.start()

    def connect(self) -> bool:
        time.sleep(2)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._sock.settimeout(5.0)
        print("Connecting...")
        try:
            self._sock.connect((self._ip, self._port))
            # sock.connect_ex()
        except Exception as ex:
            print("Connection failed: %s" % ex)
            return False
        print("Connection successed.")
        # Client_Connected()
        # for e in self.connected_event: 
        #     e(self._id,self._ip,self._port)
        self.connected_event(self._id,self._ip,self._port)
        return True  

    def start_recv(self):
        _thread.start_new_thread(self.handle_recv,())
    
    def handle_recv(self):
        while True:
            try:
                data = self.recv_data()
                print("Received data: %s len: %s %s" % 
                        (data, 
                        str(len(data)),
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                if(len(data) == 0):
                    break
            except Exception as ex:
                print("%s" % ex)
                break
        print("Receiver thread terminated")
        self.restart()
    
    def recv_data(self) -> str:
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            buffer = self._sock.recv(bufSize)
            if len(buffer) == 0:
                    break; 
            data += bytes2str(buffer)
        return data

    def start_send(self):
        _thread.start_new_thread(self.handle_send,())

    def handle_send(self):
        while True:
            if(self._isconnected == False):
                break
            self.send_data(api_btn_state)
            time.sleep(2)

    def send_data(self,data):
        print("send_data() with data = " + data)
        try:
            # append \0 as end-of-message indicator
            self._sock.sendall(str2bytes(data + "\0"))
        except Exception as ex:
            print("Exception in send_data() %s" % ex)

    def close(self):
        print("Closing socket")
        self._sock.close()
        self._isconnected = False
        print("Closed socket")



def handle_client_connected(id:str,ip:str,port:int):
    print(f"√ client [{id}] {ip}:{port} connected.")

def handle_client_disconnected(id:str,ip:str,port:int):
    print(f"× client [{id}] {ip}:{port} diconnected.")

def handle_client_received(id:str,ip:str,port:int,msg:str):
    print(f"client [{id}] {ip}:{port} received: {msg}")

if __name__ == "__main__":
    client = TcpClient("127.0.0.1",1918)
    # client.Client_Connected = handle_client_connected
    client.connected_event += handle_client_connected
    client.disconnected_event.append(handle_client_disconnected)
    client.received_event.append(handle_client_received)
    client.start()
    client.start_send()
    asyncio.get_event_loop().run_forever()





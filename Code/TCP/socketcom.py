from threading import Thread
import sys,time,_thread
import datetime
import socket
import asyncio
import uuid

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

class  TcpServer: 
    """
    Tcp Server

    """
    def __init__(self,ip="127.0.0.1",port=1918):
        self._ip = ip
        self._port = port
        self._clients = {}
        self._listenSock = None
        self.connected_event = Event()
        self.disconnected_event = Event()
        self.received_event = Event()
        self.exception_event = Event()
    
    async def start(self):
        self._listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        try:
            self._listenSock.bind((self._ip, self._port))
        except Exception as ex:
            self.exception_event(self,f"Bind failed: {str(ex)}")
        self._listenSock.listen(13)
        print ("Waiting for a connecting client...")
        self.start_listen()
        await self.start_recv()

    def start_listen(self):
        _thread.start_new_thread(self.handle_listen,())

    def handle_listen(self):
        while True:
            sock, addr = self._listenSock.accept()
            host = "{0}:{1}".format(addr[0],addr[1])
            # sock.settimeout(5.0) # timeout 5s
            self._clients[host] = sock
            self.connected_event(self,host)

    async def start_recv(self):
        # _thread.start_new_thread(await self.handle_recv,())
        # await asyncio.gather(self.handle_recv())
        await self.handle_recv()

    async def handle_recv(self):
        while True:
            publish_tasks = []

            if len(self._clients) > 0:
                for h in list(self._clients.keys()): # dictionary changed size during iteration
                    publish_tasks.append(
                        asyncio.Task(
                            self.recv_data(h)
                        )
                    )

            if publish_tasks:
                # await asyncio.wait(publish_tasks)
                result = await asyncio.gather(*publish_tasks)
                for r in list(result):
                    h = r[0]
                    d = r[1]
                    if(len(d) == 0):
                        self.close_client(h)
                    else:
                        self.received_event(self,h,d)
            else:
                await asyncio.sleep(2)
    
    async def recv_data(self,host) -> (str,str):
        bufSize = 4096
        data = ""
        sock = self._clients[host]
        while data[-1:] != "\0": # reply with end-of-message indicator
            buffer = sock.recv(bufSize)
            if len(buffer) == 0:
                    break; 
            data += bytes2str(buffer)
        return (host,data)

    def start_send(self):
        _thread.start_new_thread(self.handle_send,())
    
    def handle_send(self):
        while True:
            if len(self._clients) > 0:
                for h in list(self._clients.keys()): # dictionary changed size during iteration
                    self.send_data(h,"plc data")
            time.sleep(2)

    def send_data(self,host,data):
        sock = self._clients[host]
        try:
            # append \0 as end-of-message indicator
            sock.sendall(str2bytes(data + "\0"))
        except Exception as ex:
            self.exception_event(self,f"Send failed: {str(ex)}")
            self.close_client(host)

    def close_client(self,host):
        sock = self._clients[host]
        del self._clients[host]
        sock.close()
        self.disconnected_event(self,host)

class TcpClient:
    """
    Tcp Client

    """    
    def __init__(self,ip="127.0.0.1",port=1918):
        # self._id = uuid.uuid4()
        self._ip = ip
        self._port = port
        self.connected_event = Event()
        self.disconnected_event = Event()
        self.received_event = Event()
        self.exception_event = Event()

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
            self.exception_event(self,f"Connection failed: {str(ex)}")
            return False
        self.connected_event(self)
        return True  

    def start_recv(self):
        _thread.start_new_thread(self.handle_recv,())
    
    def handle_recv(self):
        while True:
            try:
                data = self.recv_data()
                self.received_event(self,data)
                if(len(data) == 0):
                    break
            except Exception as ex:
                print("%s" % ex)
                break
        self.exception_event(self,f"Receiver thread terminated")
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

    def send_data(self,data):
        try:
            # append \0 as end-of-message indicator
            self._sock.sendall(str2bytes(data + "\0"))
        except Exception as ex:
            self.exception_event(self,f"Send failed: {str(ex)}")

    def close(self):
        self._sock.close()
        self._isconnected = False
        self.disconnected_event(self)

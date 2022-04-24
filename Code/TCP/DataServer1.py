# DataServer1.py

from threading import Thread
import sys,time,_thread
import datetime
import socket
import asyncio
import RPi.GPIO as GPIO

P_BUTTON = 20 # adapt to your wiring
api_btn_state = "/api/btn/state"

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(P_BUTTON,GPIO.FALLING,PushButtonSatete,200)
    
def PushButtonSatete(args):
    state = "Button pressed"
    print ("Push current state:", state)
    # sock.sendall(str2bytes(state + "\0"))

def str2bytes(source):
    return bytes(source, encoding = "utf-8")

def bytes2str(source):
    return str(source, encoding ='utf-8')

class  TcpServer:
    """
    Tcp Server

    """
    def __init__(self,ip="127.0.0.1",port=1918):
        self._ip = ip
        self._port = port
        self._clients = {}
        self._listenSock = None
    
    def start(self):
        self._listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # close port when process exits:
        self._listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        print("Listen socket created")
        try:
            self._listenSock.bind((self._ip, self._port))
        except Exception as ex:
            print ("Bind failed", str(ex))
            sys.exit()
        self._listenSock.listen(13)
        print ("Waiting for a connecting client...")
        self.start_listen()
      

    def start_listen(self):
        _thread.start_new_thread(self.handle_listen,())

    def handle_listen(self):
        while True:
            print("Calling blocking accept()...")
            sock, addr = self._listenSock.accept()
            host = "{0}:{1}".format(addr[0],addr[1])
            # sock.settimeout(5.0) # timeout 5s
            print ("Connected with client at %s" % host)
            self._clients[host] = sock

    async def start_recv(self):
        # _thread.start_new_thread(await self.handle_recv,())
        await self.handle_recv()
        # await asyncio.gather(self.handle_recv())

    async def handle_recv(self):
        while True:
            publish_tasks = []

            if len(self._clients) > 0:
                for h in list(self._clients.keys()): # dictionary changed size during iteration
                    a = self._clients[h]
                    publish_tasks.append(
                        asyncio.Task(
                            self.recv_data(h,a)
                        )
                    )

            if publish_tasks:
                # await asyncio.wait(publish_tasks)
                result = await asyncio.gather(*publish_tasks)
                for r in list(result):
                    h = r[0]
                    a = r[1]
                    if(len(a) == 0):
                        self.close_client(h)
                    else:
                        print(f">> requset {h}:{a}")
                        self.execute_api(h,a)
            else:
                await asyncio.sleep(2)
    
    async def recv_data(self,host,sock) -> (str,str):
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            buffer = sock.recv(bufSize)
            if len(buffer) == 0:
                    break; 
            data += bytes2str(buffer)
        return (host,data)

    def execute_api(self,host,api):
        if api[:-1]== api_btn_state:  # remove trailing "\0"
            sock = self._clients[host]
            if GPIO.input(P_BUTTON) == GPIO.LOW:
                data = "Button pressed"
            else:
                data = "Button released"
            self.send_data(host,sock,data)
    
    def start_send(self):
        _thread.start_new_thread(self.handle_send,())
    
    def handle_send(self):
        while True:
            if len(self._clients) > 0:
                for h in list(self._clients.keys()): # dictionary changed size during iteration
                    s = self._clients[h]
                    # TODO: async send data
                    self.send_data(h,s,"plc data")
            time.sleep(2)

    def send_data(self,host,sock,data):
        print("send_data() with data = %s to %s %s" % 
                (data,
                host,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        try:
            # append \0 as end-of-message indicator
            sock.sendall(str2bytes(data + "\0"))
        except Exception as ex:
            print("Exception in send_data() %s" % ex)
            self.close_client(host)

    def close_client(self,host):
        print("Closing %s socket" % host)
        sock = self._clients[host]
        del self._clients[host]
        sock.close()
        print("Closed %s socket" % host)

async def main():
    setup()
    server = TcpServer("127.0.0.1",1918)
    server.start()
    # server.start_send()
    await server.start_recv()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
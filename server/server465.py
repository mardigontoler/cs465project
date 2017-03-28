import socket
import threading
import logging
import logging.handlers


MAXBYTESCAPTURE = 100000
MAXBYTESLOGGER = 100000000
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cs465serverLog')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler('capture.txt', 'a', MAXBYTESLOGGER, 1)
logger.addHandler(handler)

class Server465:
    def __init__(self):
        print('Server starting up...\n')
        self.serversocket = socket.socket()
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(('', 1024))
        self.runningthreads = []
        try:
            self.serve()
        except KeyboardInterrupt as kbi:
            self.serversocket.close()
            exit(0)


    def serve(self):
        self.serversocket.listen(10) # refuse connection if more than 10 waiting
        while True:
            (client, addr) = self.serversocket.accept()
            func = lambda:self.clientInstance(client)
            newthread = threading.Thread(None, func)
            self.runningthreads.append(newthread)
            newthread.start()




    def clientInstance(self, clientSock):
        """
        The function which runs in a thread per client
        """
        logger.info('New client')
        byteslist = [] # a list that will be populated 1 byte at a time
        clientSock.settimeout(None)

        # handshake the client
        handshaking = True
        while handshaking:
            b = clientSock.recv(1)
            if b == b'\xFE':
                clientSock.send(b'\xFE')
                handshaking = False


        # Make sure not to read too much data. Cut off the connection 
        # after a maximum size, 0 length data,  or timeout is reached

        # the timeout clock starts ticking once 
        # that first correct byte is sent
        clientSock.settimeout(3)

        try:
            nextbyte = clientSock.recv(1)
            byteslist.append(nextbyte)
            while(nextbyte != b'\xFF'
                    and nextbyte != b''
                    and len(byteslist) <= MAXBYTESCAPTURE + 1):
                nextbyte = clientSock.recv(1)
                byteslist.append(nextbyte)
        except socket.timeout as to:
            pass

        if byteslist[-1] == b'\xFF':
            byteslist = byteslist[0:-1] # strip off last element
        
        # now, try to log the result
        result = ""
        try:
            result += b''.join(byteslist).decode('utf8')
        except TypeError as te:
            logger.error("Could not encode reults. Bad bytes.")

        logger.info(result)

        # clean up time
        clientSock.shutdown(socket.SHUT_RDWR)
        clientSock.close()






if __name__ == '__main__':
    Server465()


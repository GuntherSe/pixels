#!/usr/bin/env python3

import time
import threading
import array
from pythonosc import dispatcher
from pythonosc import osc_server

OLAOSCSTRING = "/ola2screen"

class OscOla:
    """ class OscOla 
    
    Ein DMX-Universum wird per OSC eingelesen. 
    Die einzelnen Werte können weiter verwendet werden.
    """
    
    def __init__(self):
        self.__dmx  = [0 for i in range (512)] 
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map(OLAOSCSTRING , self.get_dmx)  # reads dmx values
        
        self.server = osc_server.BlockingOSCUDPServer \
                    (("0.0.0.0", 8000), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.setDaemon (True)
        self.server_thread.start()


    def get_chanval(self, chan):
        """ DMX-Wert von Kanal 'chan' liefern
        
        chan: Wert von 1-512
        """
        if 1 <= chan <= 512:
            return self.__dmx[chan-1]
        else:
            return 0
        
    def get_channels (self, start, range):
        """ Einen Berich an Kanalwerten einlesen 
        
        chan: Start, Zähler ab 1
        range: Anzahl der Werte
        """
        if 1 <= start <= 512 and 1 <= start+range <= 512:
            #val = array.array ('B',self.__dmx).tolist()
            data = self.__dmx[start-1 : start+range-1]
            return array.array ('B', data).tolist ()
        else:
            return [0]



    def get_dmx (self, arg1, arg2): 
        """ dmx von ola empfangen 
        """
        self.__dmx = arg2

    def loop (self):
        """ Server starten, Ausgabe der relevanten Daten """
        while True:
            print (f"   \r{self.get_channels (1,3)}", end='')
            time.sleep(0.05)

    def shutdown (self):
        """ Server stoppen """
        print ("exit OSC Server...")
        self.server.shutdown()


# ------------------------------------------------------------------------------
        
if __name__ == "__main__":

    ola = OscOla ()

    try:
        ola.loop()
    except KeyboardInterrupt: 
        ola.shutdown()

from prometheus_client import Gauge

import logging

from ..config.config import CONFIG_APP


class WPSession(object):
    __instance = None
     
    def __init__(self):
        if WPSession.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super()
            self.name="cant session"
            self.contents={}
            self.metrics = CONFIG_APP["app"]["metrics"]
            WPSession.__instance = self
    
    @staticmethod
    def getInstance():
        """ Static access method. """
        if WPSession.__instance == None:
            WPSession()
        return WPSession.__instance
        
    def addMetric(self,name):
        self.contents[name]=Gauge(name, 'counter', ['app'])
        
    def updateValue(self,name,values):
        if (self.getValue(name) is None):
            return False
        
        metric = self.getValue(name)
    
        metric.labels(app=str(self.metrics[0])).set(values[0])
        metric.labels(app=str(self.metrics[1])).set(values[1])
        
       
        return True
    
    def getValue(self,name):
        try:
            if (self.contents[name]):
                return self.contents[name]
        except KeyError:
            return None
        except Exception as e:
            logging.debug(e.errno)
            raise Exception("Error al recuperar objeto de memoria") 
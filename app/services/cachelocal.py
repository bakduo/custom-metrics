import logging

class CacheLocal(object):
    __instance = None
    
    def __init__(self):
        
        if CacheLocal.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super()
            self.value={}
            CacheLocal.__instance = self
        
    @staticmethod
    def getInstance():
        """ Static access method. """
        if CacheLocal.__instance == None:
            CacheLocal()
        return CacheLocal.__instance
    
    def getValue(self,key):
        try:
            if (self.value[key]):
                return self.value[key]
        except KeyError:
            return None
        except Exception as e:
            logging.debug(e.errno)
            raise Exception("Error al recuperar objeti de memoria") 
        
    
    def setValue(self,key,value):
        self.value[key]=value
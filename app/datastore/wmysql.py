from .connector import Connector

import mysql.connector
import subprocess

from ..config.config import CONFIG_APP

import logging
import json

class Wmysql(Connector):
    def __init__(self):
        super()
        self.user = CONFIG_APP["app"]["user"]
        self.passwd = CONFIG_APP["app"]["passwd"]
        self.host = CONFIG_APP["app"]["host"]
        self.port = CONFIG_APP["app"]["port"]
        self.database = CONFIG_APP["app"]["database"]
        
    
    def execCommand(self,statusDB):
        try:
            f = open("/tmp/salida.txt","w")
            f.writelines("\n".join(map(str, statusDB)))
            f.close()
            # ORIG = | sed -e 's|\\n|\n|g'
            p1 = subprocess.Popen("cat /tmp/salida.txt",shell=True,stdout=subprocess.PIPE)
            p2 = subprocess.Popen("sed -e 's|\\\\n|\\n|g'", shell=True,stdin=p1.stdout,stdout=subprocess.PIPE)
            stdout, stderr = p2.communicate()
            logging.debug(stdout)
            return stdout
        except Exception as e:
            print(e)
            raise Exception("Error al ejecutar proceso")
        finally:
            logging.info("OK")
            
    def query(self,sql):
        con = mysql.connector.connect(user=self.user,password=self.passwd,host=self.host,database=self.database, connection_timeout=280)
        try:
            logging.debug("Acceso a LA DB OK")
            cursor = con.cursor()
            #global_connect_timeout = 'SET GLOBAL connect_timeout=280'
            #global_wait_timeout = 'SET GLOBAL connect_timeout=280'
            #global_interactive_timeout = 'SET GLOBAL connect_timeout=280'
            #cursor.execute(global_connect_timeout)
            #cursor.execute(global_wait_timeout)
            #cursor.execute(global_interactive_timeout)
            cursor.execute(sql)
            result = cursor.fetchall()
            #self.execCommand(result)
            return result
        except Exception as e:
            logging.debug(e)
            raise Exception("FALLA conexion hacia DB")
        finally:
             if con.is_connected():
                 cursor.close()
                 con.close()
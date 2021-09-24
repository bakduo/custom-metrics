from ..config.config import CONFIG_APP
import logging
from subprocess import run
import json
import xmltodict
from bs4 import BeautifulSoup

class CommandLocal(object):
    def __init__(self):
        self.name=""
        self.query=""
        self.config={}
        self.usersql =""
        self.passwdsql = ""
        self.hostsql = ""
        self.portsql = ""
        self.databasesql = ""
        
    def set_command_mysql(self):
        self.usersql = CONFIG_APP["app"]["user"]
        self.passwdsql = CONFIG_APP["app"]["passwd"]
        self.hostsql = CONFIG_APP["app"]["host"]
        self.portsql = CONFIG_APP["app"]["port"]
        self.databasesql = CONFIG_APP["app"]["database"]
        self.columns = CONFIG_APP["app"]["columns"]
        
    def exec_query_sql(self,query,format):
        
        if format=='HTML':
            output = run(['mysql', '-u'+self.usersql,'-p'+self.passwdsql,'-h'+self.hostsql,'--connect-timeout=180','-s',
              '--reconnect','-L','--database='+self.databasesql,'-H','-ne',query], text=True, capture_output=True)
        elif format == 'xml':
            output = run(['mysql', '-u'+self.usersql,'-p'+self.passwdsql,'-h'+self.hostsql,'--connect-timeout=180','-s',
              '--reconnect','-L','--database='+self.databasesql,'-X','-ne',query], text=True, capture_output=True)
        elif format == 'json':
            output = run(['mysql', '-u'+self.usersql,'-p'+self.passwdsql,'-h'+self.hostsql,'--connect-timeout=180','-s',
              '--reconnect','-L','--database='+self.databasesql,'-X','-ne',query], text=True, capture_output=True)
        
        logging.debug("exit status: {}".format(output.returncode))
        
        if output.returncode == 0:
            if format == 'json':
                data_dict = xmltodict.parse(output.stdout.strip())
                vector = []
                resultado = dict(data_dict["resultset"])
                try:
                    for item in resultado['row']:
                        objtemp = {}
                        for campos in item['field']:
                            for column in self.columns:
                                print(column)
                                if campos['@name']==column:
                                    objtemp[column] = campos['#text']
                        vector.append(objtemp)
                            
                    
                except Exception as e:
                    logging.debug("Error al realizar comando exec_query_sql {}".format(e))
                    return {'ERROR':'Error al realizar exec_query_sql'}
    
                return vector
            else:
                return output.stdout.strip()
        else:
            return output.stderr.strip()
        
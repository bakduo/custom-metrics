from app import app

from .services.command import CommandLocal
from .services.cachelocal import CacheLocal
from .config.config import CONFIG_APP
from prometheus_client import generate_latest
from .metrics.wpsession import WPSession

from flask import request
import json
import logging

metrics_session = WPSession.getInstance()

def checkParameter(year,month,day):
    
    checkContinue = True

    if ((year is None) or (month is None) or (day is None)):
        checkContinue=False
        
    if (checkContinue):
        logging.debug("Pasa 1º check")
        try:
            if ((isinstance(year, int)) and (isinstance(month, int)) and (isinstance(day, int))):
                logging.debug("Pasa 2º check")
                if (year<=2021 and year>2018) and (month<=12 and month>=1) and (day<=31 and day >=1):
                    logging.debug("Pasa 3º check")
                    return True
        except Exception as e:
            logging.debug("Error checkParameter {}".format(e))
            return False
            
    
    return False

def run_task(year,month,day,update):
    ##check injection
    try:
        if (checkParameter(int(year),int(month),int(day))):
            #Only number valid paratemter. The string to number doesn't injection.
            logging.debug("build query")
            query_remote = CONFIG_APP['app']['query']
            query_session = query_remote.format(int(year),int(month),int(day))
        else:
            return {"ERROR":'Parameter not valid'}
    except Exception as e:
        logging.debug("Error {}".format(e))
        return {'ERROR:':'Parameter for query not valid.'}
    
    try:
        cache = CacheLocal.getInstance()
        fecha = str(year)+"-"+str(month)+"-"+str(day)
        valor=cache.getValue(fecha)
    
        if valor is None:
            logging.debug("Update need it")
            if not update:
                return {"ERROR":'Require update for OPS'}
            com = CommandLocal()
            com.set_command_mysql()
            valor = com.exec_query_sql(query_session,'json')
            cache.setValue(fecha,valor)
        else:
            if (update):
                com = CommandLocal()
                com.set_command_mysql()
                valor = com.exec_query_sql(query_session,'json')
                cache.setValue(fecha,valor)
                
        return valor
    except Exception as e:
        logging.debug("Error al realizar comando {}".format(e))
        return {'ERROR':'Error when generate commmand'}
    
def processMetrics(jsondata):
    
    for item in jsondata:
        
        print(item)
        
        if (metrics_session.getValue(item[str(CONFIG_APP["app"]["columns"][0])]) is None):
            
            metrics_session.addMetric(item[str(CONFIG_APP["app"]["columns"][0])])
            
            metrics_session.updateValue(item[str(CONFIG_APP["app"]["columns"][0])],
                                        [
                item[str(CONFIG_APP["app"]["columns"][1])],
                item[str(CONFIG_APP["app"]["columns"][2])]
                ]
                                        )
        else:
            metrics_session.updateValue(item[str(CONFIG_APP["app"]["columns"][0])],
                                        [item[
                                            str(CONFIG_APP["app"]["columns"][1])
                                            ]
                                        ,
                                          item[
                                            str(CONFIG_APP["app"]["columns"][2])
                                            ]
                                        ])
        

@app.route('/metrics',methods=['GET'])
@app.route('/api/v1/metrics',methods=['GET'])
def metricssession():
    return generate_latest()

@app.route('/api/v1/updatecache',methods=['POST'])
def udpatesession():
    app.logger.debug('accesso update cache')
    year = request.json.get('year')
    month = request.json.get('month')
    day = request.json.get('day')
    token = request.json.get('token')
    if (token!=CONFIG_APP['app']['token']):
        return {'ERROR':'Acceso no auth'}
    logging.debug("update year: {} month:{} day:{}".format(year,month,day))
    valor = run_task(year,month,day,True)
    processMetrics(valor)
    return json.dumps(valor), 200
 
@app.route('/api/v1/session',methods=['POST'])
def getsession():
    app.logger.debug('accesso index')
    year = request.json.get('year')
    month = request.json.get('month')
    day = request.json.get('day')
    logging.debug("year: {} month:{} day:{}".format(year,month,day)) 
    valor = run_task(year,month,day,False)
    return json.dumps(valor), 200

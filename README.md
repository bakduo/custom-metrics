Metrics by SQL
===============================

# ROADMAP
- [x] acceso a la db de recursos secundarios como solo lectura.
- [x] generar bypass para metricas respecto a la cantidad de sessiones.
- [x] preparar grafana y prometheus
- [x] generar imagen de docker. Así se puede usar como una api de servicio.
- [x] timeout after 30s.
- [x] uso de prometheus_client
- [ ] refactor

# Overview 

En este caso necesite implementer un servicio que me permita extraer datos para metricas, con la particularidad de que no es posible acceder a atravez de los servicios que corresponden y tampoco por medio otros servicios externos ya sea por que no esta disponible o porque no estan implementados. Por lo tanto como una alternativa es posible consumir recursos de datos secundarios en los cuales los almacena y construir un servicio sobre este. No es la mejor practica, sin embargo puede servir ante la falta de recursos para observar determinados eventos.

## Check API

by rest:

```
http POST localhost:5000/api/v1/aname year=year month=mes day=dia --timeout 180 --pretty all
```

return JSON.

## Como instalar dependencias en el entorno local

Es necesario generar las depedencias del proyecto:
```
pipenv lock -r > deploy-requirements.txt

```

Y luego dentro del entorno virtual

```
pip install -r deploy-requirements.txt

```

## Como ejecutarlo dentro del entorno

```
pipenv shell

./run-dev.sh
```
Recomendación es usar pipenv en lugar del clasico pip porque con pipenv ya nos genera todo un entorno sin mezclar las apps ni las dependecias de la maquina local.

## Como ejecutar en un container:

1. es necesario construir la imagen

make clean && make build

2. ejecutarlo

```
Sample deployment.json

Config

{
    "app":{
        "port":3306,
        "user":"user",
        "passwd":"pass",
        "database":"dbname",
        "host":"server",
        "token":"str token",
        "query":"query SQL",
        "columns": ["pedidos_app","cantidad"],
        "metrics":["cantidad_entregas"]
    }
}

docker run --rm -p 5000:5000 -v $(pwd)/development.json:/home/uapi/app/config/development.json testapi:1.0.0

http POST https://api-service.domain.tld:port/api/v1/aname year=2021 month=[1-12] day=[1-31] --timeout 180 --pretty all

Salida:

[
    {
        "service": "A",
        "count_cantidad_entregas": "12",
    },
    {
        "service": "D",
        "count_cantidad_entregas": "565",
    },
    {
       ...
    },
    {
]
```

Para poder graficarlo en grafana + prometheus es necesario aplicar regla de transform en la query desde grafana, en mi caso use **rename by regex** y aplique la correspondiente expresion regular, así al final dejas solo aquellos campos que te interesan. De lo contrario prometheus trae un string completo que ocupa un poco mas de lugar.

# Bigdata

# Configuración del proyecto

Se debe crear un entorno virtual e intalar las dependencias requeridas. Utiliza los siguiente comandos:

- Crear entorno virtual.

```
python -m venv venv
```

- Activar entorno virtual

```
./venv/Scripts/activate
```

- Instalar dependencias

```
pip install -e .
```

# Ingesta de datos

El archivo `Ingesta.py` se encarga de crear la bases de datos, las tablas de la bases de datos y poblarlas, adicional crea un archivo .txt que es la auditoria e información de lo datos.

Para realizar la ingesta de datos se ejecuta el comando

```
python src/Ingesta.py
```

El archivo `script.py` crea el archivo .json y un archivo .xlx, para ejecutarlo se utiliza el comando:

```
python script.py
```

# Limpieza de Datos

El archivo `cleaning.py`, se conecta a la bases de datos para crear un dataframe y realizar la limpieza necesaria como borrar los datos nulos, datos duplicados y validación de tipo de datos para la fecha.
Adicional genera los siguientes archivos:

- cleaned_data_laureates.csv, cleaned_data_nobel_prizes.csv, para mostrar el resultado final de la limpieza del dataframe.

- auditoria_laureates.txt, auditoria_nobel_prizes.txt, para auditorias y muestra un resumen y el impacto de la limpieza.

para ejecutar este archivo se necesita el comando:

````
python src/cleaning.py
```
````

<h1 align='center'>Credenciales UAG</h1>
<h3 align='center'>Extracción e validación</h1>

En este [Colab](https://colab.research.google.com/drive/1fNgV-kOV78WTfJpHRH98-ArWTNuAvNDX?usp=sharing) se clona el repositorio para correr los métodos necesarios de extracción y transformación/limpieza de datos. Pruébalo!

# Índice
- [x] [Repositorio](#Repositorio)
- [x] [Extracción](#Extracción)
- [x] [Transformación](#Transformación)
- [ ] [Modelos](#Modelos)
- [ ] [Puesta en producción](#Puesta-en-producción) (En progreso ...)

<br>
- - - -
<br>

# Repositorio:
    .
    ├── __init__.py             # Para que el directorio se trabaje de forma modular
    │
    ├── main.py                 # Hereda GetEmailData y TransformData para obtener y limpiar las imágenes
    ├── get_email_data.py       # Permite iniciar sesión en @edu.uag.mx para importar todas las imágenes adjuntas en la bandeja de entrada de un rango específico de fechas
    ├── transform.py            # Limpia los datos y crea variables de utilidad
    │
    └── requirements.txt        # Instalar las librerías necesarias con el comando: pip install -r requirements.txt

<br>


# Extracción

El método`CredencialesUAG.get_data()`
ejecuta estos pasos:
    1. `self.login()` que solicita la contraseña al usuario (no se muestra)
    2. `self.filter_msg_dates(filter_from='INBOX')` para seleccionar la bandeja de entrada y el rango de fechas indicado
    3. `self.create_files_dir(create_user_folder=False)` crea el folder con nombre: *"fecha inicial a fecha final"*
    4. `self.get_files()` descarga todos los archivos adjuntos en la carpeta y fechas indicadas, además de guardar información relevante en una lista de diccionarios
    5. `self.finish_session()` cierra la sesión del correo electrónico


<br><br>


# Transformación

El método`CredencialesUAG.transform_data()`
ejecuta estos pasos:
1. `self.get_email(col_from='from')` convierte la lista de información relevante en un DataFrame y crea una columna con sólo el email del remitente
2. `self.date_vars(date_col='date', timezone='America/Mexico_City')` crea variables implícitas a la fecha como año, mes, día, semana, etc
3. `self.just_img(valid_ext=['png','jpg','jpeg'])` filtra los registros con extensión válida en el nombre del archivo adjunto
4. `self.last_email()` se queda únicamente con el último correo de cada email
5. `self.last_img()` elimina las imágenes que no corresponden al último correo por email recibido
6. `self.convert_png()` si hay imágenes con extensión *".png"* las convierte a *".jpg"*
    
El resultado de este método es:
|    |   id | date                      | from                                    | subject                    | filename             | file_dir                                                 | email                    |   date_year |   date_month |   date_day |   date_dayofweek |   date_hour |   date_minute |   date_second | file_ext   | is_jpg   |
|---:|-----:|:--------------------------|:----------------------------------------|:---------------------------|:---------------------|:---------------------------------------------------------|:-------------------------|------------:|-------------:|-----------:|-----------------:|------------:|--------------:|--------------:|:-----------|:---------|
|  0 |  002 | 2022-09-14 11:46:01-05:00 | Diego Flores <floresca.diego@gmail.com> | foto                       | 002DataRoles.jpg     | /content/08-sep-2022 to 14-sep-2022/002DataRoles.jpg     | floresca.diego@gmail.com |        2022 |            9 |         14 |                2 |          11 |            46 |             1 | png        | False    |
|  3 |  005 | 2022-09-09 13:26:44-05:00 | Efra Flores <efraisma.ef7@gmail.com>    | Re: TEST CON FOTO CORRECTA | 005EF_credencial.jpg | /content/08-sep-2022 to 14-sep-2022/005EF_credencial.jpg | efraisma.ef7@gmail.com   |        2022 |            9 |          9 |                4 |          13 |            26 |            44 | png        | False    |

<br><br>


6. Se utilizará el shapefile de los [Códigos Postales CDMX](https://datos.cdmx.gob.mx/dataset/7abff432-81a0-4956-8691-0865e2722423/resource/8ee17d1b-2d65-4f23-873e-fefc9e418977) para definir los límites en el mapa

![](media/for_readme/cdmx.png?raw=true "Mexico City by zipcodes") 

<br><br>


7. Al unir ambos mapas, utilizando las coordenadas y disponibilidad de las estaciones, este es el resultado:
```python
ebm.plot_map(
    data=ebm.df,
    col_to_plot='slots_proportion',
    padding=0.006,
    color='#ffffff',
    edgecolor='#00acee', 
    points_palette='Blues')
```

<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/full_map.jpeg" width=50% height=50%>

<br><br>


# Interacción

8. Al [iniciar un chat con Ecobici TelegramBot](t.me/EcobicimapBot) te muestra las instrucciones del chat
<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/01_start.png" width=50% height=50%>
Todas las opciones que comienzan con "\" pueden ser presionadas y son inmediatamente enviadas.

<br><br>

9. Tal como en [Ecobici TwitterBot](https://twitter.com/EcobiciMapBot), este bot puede mostrar la disponibilidad total de CDMX mandando el comando `\todo`
<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/02_todo.png" width=50% height=50%>

<br><br>

10. Incluso puedes actualizar los datos en cualquier momento mandando `\update`
<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/03_update.png" width=50% height=50%>

<br><br>

11. Ahora, veamos las opciones que filtran una zona en el mapa. En primer lugar está la consulta por código postal, sólo basta con ocupar la palabra `zipcode XXXX` para filtrar en el mapa la zona con código postal `XXXX`
<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/04_zipcode.png" width=50% height=50%>

<br><br>

12. Por otro lado, es posible filtrar zonas más específicas indicando la colonia. La manera de hacerlo es mandando `colonia XXXX` o bien la abreviatura `col XXXX`. Si el texto recibido se parece a más de una colonia, te mostrará máx 5 opciones para que elijas cuál consultar.
<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/05_options.jpeg" width=50% height=50%>

<br>

<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/06_answered.jpeg" width=50% height=50%>

<br><br>

13. Incluso, dado que utiliza [difflib.SequenceMatcher](https://docs.python.org/2/library/difflib.html#sequencematcher-objects) para comparar el texto recibido vs las opciones de colonias válidas, también "corrige" las faltas de ortografía, por ejemplo:
<img src="https://github.com/Afroefras/ecobici_telegram_bot/blob/main/media/for_readme/07_typo.png" width=50% height=50%>

<br><br>

# Puesta en producción 

La investigación preliminar apunta que el script debe instanciarse en un servidor, cómo hacerlo está en progreso, espérenlo ...

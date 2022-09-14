<h1 align='center'>Credenciales UAG</h1>
<h3 align='center'>Extracción y validación</h3>

En este [notebook en Google Colab](https://colab.research.google.com/drive/1fNgV-kOV78WTfJpHRH98-ArWTNuAvNDX?usp=sharing) se clona el repositorio para correr los métodos necesarios de extracción y transformación/limpieza de datos. Pruébalo!

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
|   id | date                      | from                                    | subject                    | filename             | file_dir                                                 | email                    |   date_year |   date_month |   date_day |   date_dayofweek |   date_hour |   date_minute |   date_second | file_ext   | is_jpg   |
|-----:|:--------------------------|:----------------------------------------|:---------------------------|:---------------------|:---------------------------------------------------------|:-------------------------|------------:|-------------:|-----------:|-----------------:|------------:|--------------:|--------------:|:-----------|:---------|
|  002 | 2022-09-14 11:46:01-05:00 | Diego Flores <floresca.diego@gmail.com> | foto                       | 002DataRoles.jpg     | /content/08-sep-2022 to 14-sep-2022/002DataRoles.jpg     | floresca.diego@gmail.com |        2022 |            9 |         14 |                2 |          11 |            46 |             1 | png        | False    |
|  005 | 2022-09-09 13:26:44-05:00 | Efra Flores <efraisma.ef7@gmail.com>    | Re: TEST CON FOTO CORRECTA | 005EF_credencial.jpg | /content/08-sep-2022 to 14-sep-2022/005EF_credencial.jpg | efraisma.ef7@gmail.com   |        2022 |            9 |          9 |                4 |          13 |            26 |            44 | png        | False    |

<br><br>

# Modelos
***(EN PROGRESO...)***

La idea es entrenar y aplicar 3 modelos que respondan:
1. ¿La persona trae lentes?
2. ¿Está mirando al frente (no selfies)?
3. ¿Tiene fondo blanco?

<br><br>

# Puesta en producción 
***(EN PROGRESO...)***

La idea es que en el [notebook en Google Colab](https://colab.research.google.com/drive/1fNgV-kOV78WTfJpHRH98-ArWTNuAvNDX?usp=sharing) la cuenta credenciales@edu.uag.mx pueda:
1. Obtener las fotos que cumplan con las características correctas
2. Mandar respuesta a los correos con imágenes que no cumplan con las características

<h1 align='center'>Credenciales UAG</h1>
<h3 align='center'>Extracción y validación</h3>

En este [notebook en Google Colab](https://colab.research.google.com/drive/1fNgV-kOV78WTfJpHRH98-ArWTNuAvNDX?usp=sharing) se clona el repositorio para correr los métodos necesarios de extracción, transformación, limpieza y predicción. 
¡Pruébalo!

# Índice
- [x] [Repositorio](#Repositorio)
- [x] [Extracción](#Extracción)
- [x] [Transformación](#Transformación)
- [ ] [Modelos](#Modelos)
- [x] ---- ¿La persona NO trae lentes?
- [ ] ---- Aplicar fondo blanco (en progreso ... )
- [ ] [Puesta en producción](#Puesta-en-producción) (en progreso ... )

<br>

---

<br>

# Repositorio:
    .
    ├── __init__.py         # Para que el directorio se trabaje de forma modular
    │
    ├── main.py             # Hereda GetEmailData, TransformData y GetModel para obtener, limpiar las imágenes y predecir si la persona NO tiene lentes
    ├── get_email_data.py   # Permite iniciar sesión en @edu.uag.mx para importar todas las imágenes adjuntas en la bandeja de entrada de un rango específico de fechas
    ├── transform.py        # Limpia los datos y crea variables de utilidad
    ├── get_model.py        # Extrae el ZIP desde GoogleDrive con el modelo entrenado (99.4% en val) para aplicarlo en las imágenes recibidas por correo
    │
    └── requirements.txt    # Instalar las librerías necesarias con el comando: pip install -r requirements.txt

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

|    |   id | date                      | from                                    | subject                  | filename            | file_dir                                                | email                    |   date_year |   date_month |   date_day |   date_dayofweek |   date_hour |   date_minute |   date_second | file_ext   | is_jpg   |
|---:|-----:|:--------------------------|:----------------------------------------|:-------------------------|:--------------------|:--------------------------------------------------------|:-------------------------|------------:|-------------:|-----------:|-----------------:|------------:|--------------:|--------------:|:-----------|:---------|
|  0 |  001 | 2022-09-21 16:18:38-05:00 | Diego Flores <floresca.diego@gmail.com> | .i.                      | 001Diego Flores.jpg | /content/08-sep-2022 to 21-sep-2022/001Diego Flores.jpg | floresca.diego@gmail.com |        2022 |            9 |         21 |                2 |          16 |            18 |            38 | png        | False    |
|  5 |  007 | 2022-09-21 16:09:51-05:00 | Efra Flores <efraisma.ef7@gmail.com>    | TEST CON FOTO INCORRECTA | 007lentes.jpeg      | /content/08-sep-2022 to 21-sep-2022/007lentes.jpeg      | efraisma.ef7@gmail.com   |        2022 |            9 |         21 |                2 |          16 |             9 |            51 | jpeg       | True     |

<br><br>

# Modelos

## ¿La persona NO trae lentes?

Se ocuparon [imágenes](https://www.kaggle.com/datasets/jorgebuenoperez/datacleaningglassesnoglasses) (creadas artificialmente) de personas con lentes y sin lentes, para poder replicar el transfer-learning de MobileNet-v2 (que es una Red Neuronal Convolucional profunda con 53 capas) para clasificar las imágenes, tal como lo explica [Jorge Bueno](https://www.kaggle.com/jorgebuenoperez) en su [notebook](https://www.kaggle.com/code/jorgebuenoperez/computer-vision-application-of-cnn/notebook).

El modelo con [99.41%](https://colab.research.google.com/drive/1umulctdWTtWoVvkoNSEqk5pd4Be4eL8A?usp=sharing) en el conjunto de validación, se exporta a Google Drive y se comprime para que a través del método heredado en la Clase principal, el modelo se pueda importar al [notebook](https://colab.research.google.com/drive/1fNgV-kOV78WTfJpHRH98-ArWTNuAvNDX?usp=sharing) en Google Colab y aplicarse para cada una de las imágenes adjuntas en los correos recibidos.

Así, el DataFrame ahora tiene dos columnas adicionales, que indican:
1. La probabilidad de que la persona NO tenga lentes y 
2. La transformación binaria redondeando dicha probabilidad

|    |   id |...|   no_glasses_proba |   no_glasses |
|---:|-----:|--:|-------------------:|-------------:|
|  0 |  001 |...|           0.842446 |            1 |
|  5 |  007 |...|           0.204064 |            0 |

<br>

No glasses proba: 84.24%             |  No glasses proba: 20.40% 
:-------------------------:|:-------------------------:
![](https://github.com/Afroefras/uag_badges/blob/main/media/Diego%20Flores.png)  |  ![](https://github.com/Afroefras/uag_badges/blob/main/media/lentes.jpeg)

<br><br>

## Aplicar fondo blanco 
***(EN PROGRESO...)***

<br><br>

# Puesta en producción 
***(EN PROGRESO...)***

La idea es que en el [notebook](https://colab.research.google.com/drive/1fNgV-kOV78WTfJpHRH98-ArWTNuAvNDX?usp=sharing) en Google Colab la cuenta credenciales@edu.uag.mx pueda:
1. Obtener las fotos que cumplan con las características correctas
2. Mandar respuesta a los correos con imágenes que no cumplan con las características

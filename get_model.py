from pathlib import Path
from zipfile import ZipFile
from requests import Session

from numpy import asarray
from PIL.Image import open as open_img

from keras.models import load_model

class GetModel:
    def __init__(self) -> None:
        pass
    
    def set_model_env(self, google_drive_file_id: str, model_name: str, base_dir: str=None) -> None:
        '''
        Sólo recibe el identificador en Google Drive y la clase cuenta con los métodos suficientes para:
            - entrenamiento
            - predicción
        '''
        self.zip_id = google_drive_file_id
        # Define el directorio como objeto Path para manejar eficientemente los archivos y directorios
        if base_dir is not None: self.base_dir = Path(base_dir)
        else: self.base_dir = Path().cwd()

        self.model_name = model_name
        self.model_dir = self.base_dir.joinpath('models')
        self.model_dir.mkdir(exist_ok=True)

    def get_model_zip(self) -> None:
        '''
        Extrae los archivos del ZIP que fue compartido via Google Drive
        '''
        # Hace la solicitud a la URL y guarda la respuesta
        session = Session()
        URL = "https://docs.google.com/uc?export=download"
        response = session.get(URL, params={'id':self.zip_id, 'confirm':'t'}, stream=True)

        # Guarda el archivo ZIP en el directorio descrito
        model_zip_dir = self.model_dir.joinpath(f'model_{self.model_name}.zip')
        with open(model_zip_dir, "wb") as f:
            for chunk in response.iter_content(32768):
                f.write(chunk)
        
        # Extrae todos los archivos del ZIP en el directorio
        for zip_file in self.model_dir.glob('*.zip'):
            with ZipFile(zip_file) as z:
                z.extractall(self.model_dir)


    def import_model(self) -> None:
        self.model = load_model(self.model_dir.joinpath(self.model_name))


    def model_predict(self, img_dir: str) -> float:
        img = open_img(img_dir)
        img = img.resize((160,160))

        to_predict = asarray(img)
        to_predict = to_predict.reshape((-1,160,160,3))

        prediction = self.model.predict(to_predict)
        return prediction

from smtplib import SMTP
from shutil import make_archive

class ExportData:
    def __init__(self) -> None:
        pass

    def split_imgs(self, prediction_col: str) -> None:
        for img, prediction in zip(self.df['file_dir'], self.df[prediction_col]):
            to_dir = f'{prediction_col}_{prediction}'

            prev_path = img.parent
            new_path = prev_path.joinpath(to_dir)
            new_path.mkdir(exist_ok=True)

            img.rename(new_path.joinpath(img.name))
        
        self.prediction_col = prediction_col


    def zip_dir(self) -> None:
        make_archive(self.dates_range, 'zip', self.files_dir)
        self.zip_dir = self.base_dir.joinpath(self.dates_range + '.zip')

    
    def write_msg(self, options_send_to: list) -> None:
        incorrect_imgs = self.df[self.prediction_col].isin(options_send_to)
        incorrect_imgs = self.df['email'][incorrect_imgs]
        
        self.send_to = incorrect_imgs.dropna()
        self.send_to = ", ".join(self.send_to)
        
        self.msg = f'From: {self.user_email}\r\n'
        self.msg += f'To: {self.send_to}\r\n'
        self.msg += 'Subject: Foto para credencial incorrecta\r\n\r\n'
        self.msg += '''
Hola!

Estás recibiendo este correo porque nuestro modelo detectó que la foto enviada no cumple con todos los requisitos.

Los requisitos para la foto de credencial UAG son:
    1. No uso de lentes
    2. La fotografía debe ser Digital y a color en un fondo blanco (no se permiten fotografías de fotos o escáner de fotos anteriores)  
    3. Uso de uniforme (Medicina, Odontología, Terapia Física, Educación Básica desde kínder hasta preparatoria) .
        - si no eres de las carreras anteriores usa vestimenta formal o casual (mujeres no escotes ni transparencias)
    4. Fotografía de frente (no selfie, no perfil)  

En caso haber enviado la foto correcta, mandar un nuevo correo adjuntando la imagen y escribiendo en el asunto: FOTO CORRECTA

Gracias, quedamos a sus órdenes.
Credeciales UAG
        '''


    def send_response(self) -> None:
        smtp_server = SMTP('smtp.office365.com', port=587)
        smtp_server.starttls()
        smtp_server.login(self.user_email, self.random_var)
        smtp_server.sendmail(self.user_email, self.send_to, self.msg.encode('utf-8').strip())
        smtp_server.quit()
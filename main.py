try: 
    from .get_email_data import GetEmailData
    from .transform_data import TransformData
    from .get_model import GetModel
    from .export_data import ExportData
except ImportError: 
    from get_email_data import GetEmailData
    from transform_data import TransformData
    from get_model import GetModel
    from export_data import ExportData


class CredencialesUAG(GetEmailData, TransformData, GetModel, ExportData):
    def __init__(self, test: bool=False, domain: str = '@edu.uag.mx', server: str = 'outlook.office365.com') -> None:
        if test:
            self.date_from = '21-sep-2022'
            self.date_to = '21-sep-2022'
            self.username = 'efrain.flores'
        else:
            self.date_from = input('\n(En formato dd-mmm-yyyy, ej: 22-sep-2022)\nFecha inicial: ').lower()
            self.date_to = input('Fecha final: ').lower()
            self.username = input('\n\nSólo nombre de usuario, sin @edu.uag.mx, ej: efrain.flores\nUsuario: ').lower()
        super().__init__(domain, server)

    def get_data(self) -> None:
        self.login()        
        self.filter_msg_dates(filter_from='INBOX')
        self.create_files_dir(create_user_folder=False)
        self.get_files()
        self.finish_session()

    def transform_data(self) -> None:
        self.get_email(col_from='from')
        self.date_vars(date_col='date', timezone='America/Mexico_City')
        self.just_img(valid_ext=['png','jpg','jpeg'])
        self.last_email()
        self.last_img()
        self.convert_png()
        
    def predict_glasses(self, threshold: float) -> None:
        self.df['no_glasses_proba'] = self.df['file_dir'].map(self.model_predict)
        self.df['no_glasses_proba'] = self.df['no_glasses_proba'].map(lambda x: x[0][0])
        self.df['no_glasses'] = self.df['no_glasses_proba'].map(lambda x: 1 if x >= threshold else 0)

    def get_model(self) -> None:
        self.set_model_env('1E2Ducc4YQmf_lrStZARZT4t-rr5UWVZj', model_name='CLoSL')
        self.get_model_zip()
        self.import_model()
        self.predict_glasses(threshold=0.5)

    def export_data(self) -> None:
        self.split_imgs(prediction_col='no_glasses')
        self.zip_dir()
        self.write_msg(options_send_to=[0])
        self.send_response()

    def run(self) -> None:
        self.get_data()
        print(f'\n\nObteniendo correos de {self.user_email} ...')
        print(f'Limpiando datos ...')
        self.transform_data()
        print(f'Importando modelos ...')
        self.get_model()
        print(f'Exportando resultados ...')
        self.export_data()
        print(f'Listo, {len(self.send_to)} ({len(self.send_to)/len(self.df):0%}%) correos han sido contestados.\nEn unos momentos se descargarán los resultados :)')

if __name__ == '__main__':
    uag = CredencialesUAG(test=True)
    uag.run()
    print(uag.df.head())

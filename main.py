try: 
    from .get_email_data import GetEmailData
    from .transform_data import TransformData
    from .get_model import GetModel
except ImportError: 
    from get_email_data import GetEmailData
    from transform_data import TransformData
    from get_model import GetModel


class CredencialesUAG(GetEmailData, TransformData, GetModel):
    def __init__(self, domain: str = '@edu.uag.mx', server: str = 'outlook.office365.com') -> None:
        self.date_from = input('En formato dd-mmm-yyyy\n\nFecha inicial: ').lower()
        self.date_to = input('Fecha final: ').lower()
        self.username = input('Usuario (sólo nombre de usuario, sin @edu.uag.mx, ej: efrain.flores: ').lower()
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

    def get_model(self) -> None:
        self.get_model_zip()
        self.import_model()
        
    def predict_glasses(self, threshold: float) -> None:
        self.df['no_glasses_proba'] = self.df['file_dir'].map(self.model_predict)
        self.df['no_glasses_proba'] = self.df['no_glasses_proba'].map(lambda x: x[0][0])
        self.df['no_glasses'] = self.df['no_glasses_proba'].map(lambda x: 1 if x >= threshold else 0)


    def run(self) -> None:
        self.get_data()
        self.transform_data()
        self.set_model_env('1E2Ducc4YQmf_lrStZARZT4t-rr5UWVZj', model_name='CLoSL')
        self.get_model()
        self.predict_glasses(threshold=0.5)

if __name__ == '__main__':
    uag = CredencialesUAG()
    uag.run()
    print(uag.df.head())

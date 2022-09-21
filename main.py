try: 
    from .get_email_data import GetEmailData
    from .transform_data import TransformData
    from .get_model import GetModel
except ImportError: 
    from get_email_data import GetEmailData
    from transform_data import TransformData
    from get_model import GetModel


class CredencialesUAG(GetEmailData, TransformData, GetModel):
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

if __name__ == '__main__':
    USER = input('Usuario: ')
    uag = CredencialesUAG(USER, date_from='9-sep-2022', date_to='21-sep-2022')
    uag.get_data()
    uag.transform_data()

    MODEL_ID = '1E2Ducc4YQmf_lrStZARZT4t-rr5UWVZj'
    uag.set_model_env(MODEL_ID, model_name='CLoSL')
    uag.get_model()
    uag.predict_glasses(threshold=0.5)

    print(uag.df.head())

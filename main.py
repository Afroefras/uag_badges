try: 
    from .get_email_data import GetEmailData
    from .transform_data import TransformData
except ImportError: 
    from get_email_data import GetEmailData
    from transform_data import TransformData


class CredencialesUAG(GetEmailData, TransformData):
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

if __name__ == '__main__':
    # user = input('Usuario: ')
    user = 'efrain.flores'
    cuag = CredencialesUAG(user, date_from='14-sep-2022', date_to='14-sep-2022')
    cuag.get_data()
    cuag.transform_data()
    print(cuag.df.head())

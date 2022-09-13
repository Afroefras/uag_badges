from get_email_data import GetEmailData
from transform_data import TransformData

class CredencialesUAG(GetEmailData, TransformData):
    def get_data(self, get_from: str, create_user_folder: bool) -> None:
        self.login()
        self.filter_msg_dates(filter_from=get_from)
        self.create_files_dir(create_user_folder=create_user_folder)
        self.get_files()
        self.finish_session()

    def transform_data(self, col_from: str, **kwargs) -> None:
        self.get_email(col_from=col_from)
        self.date_vars(**kwargs)
        self.last_email()
        self.last_picture()
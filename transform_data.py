from re import findall
from dateutil import tz
from pandas import DataFrame, to_datetime


class TransformData:
    def get_email(self, col_from: str) -> None:
        self.df = DataFrame(self.files_list)
        email_pattern = r'([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)>$'
        self.df['email'] = self.df[col_from].map(lambda x: findall(email_pattern, x)[-1])


    def date_vars(self, date_col: str, timezone: str) -> None:
        self.df[date_col] = to_datetime(self.df[date_col])
        self.df[date_col] = self.df[date_col].map(lambda x: x.astimezone(tz.gettz(timezone)))
        for date_var in ('year','month','day','dayofweek','hour','minute','second'):
            self.df[f'{date_col}_{date_var}'] = eval(f"self.df[date_col].dt.{date_var}")
        self.date_col = date_col


    def just_img(self, valid_ext: list) -> None:
        self.df['file_ext'] = self.df['filename'].str.split('.').str[-1]
        self.df = self.df[self.df['file_ext'].isin(valid_ext)].copy()


    def last_email(self) -> None:
        self.df.sort_values(self.date_col, ascending=False, inplace=True)
        self.df.drop_duplicates(subset=['email'], inplace=True)


    def last_img(self) -> None:
        valid_imgs = list(self.df['file_dir'])
        all_imgs = list(self.files_dir.glob('*'))
        for pic in all_imgs:
            if pic.is_file() and pic not in valid_imgs:
                pic.unlink()
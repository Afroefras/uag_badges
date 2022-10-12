from dateutil import tz
from re import findall, search
from pandas import DataFrame, to_datetime
from cv2 import imread, cvtColor, COLOR_BGR2RGB
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from PIL.Image import fromarray, open as open_img, new as new_img

from cvzone.SelfiSegmentationModule import SelfiSegmentation


class TransformData:
    def __init__(self) -> None:
        pass

    def just_img(self, valid_ext: list) -> None:
        self.df = DataFrame(self.files_list)

        self.df['file_ext'] = self.df['filename'].str.split('.').str[-1]
        self.df = self.df[self.df['file_ext'].isin(valid_ext)].copy()


    def date_vars(self, date_col: str, timezone: str) -> None:
        self.df[date_col] = to_datetime(self.df[date_col])
        self.df[date_col] = self.df[date_col].map(lambda x: x.astimezone(tz.gettz(timezone)))
        for date_var in ('year','month','day','dayofweek','hour','minute','second'):
            self.df[f'{date_col}_{date_var}'] = eval(f"self.df[date_col].dt.{date_var}")
        self.date_col = date_col


    def get_email(self, col_from: str) -> None:
        email_pattern = r'([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)>$'
        self.df['email'] = self.df[col_from].map(lambda x: findall(email_pattern, x)[-1])
        
        self.df['is_uag_email'] = self.df['email'].map(lambda x: search('@edu.uag.mx', x) is not None)


    def last_email(self) -> None:
        self.df.sort_values(self.date_col, ascending=False, inplace=True)
        self.df.drop_duplicates(subset=['email'], inplace=True)


    def last_img(self) -> None:
        valid_imgs = list(self.df['file_dir'])
        all_imgs = list(self.files_dir.glob('*'))
        for pic in all_imgs:
            if pic.is_file() and pic not in valid_imgs:
                pic.unlink()

    
    def png_to_jpg(self, img) -> None:
        png = img.convert('RGBA')
        png.load()

        jpg = new_img("RGB", png.size, (255, 255, 255))
        jpg.paste(png, mask=png.split()[3])
        return jpg


    def load_png_save_jpg(self, img_dir: str, img_name: str) -> None:
        png = open_img(img_dir.joinpath(img_name))
        
        jpg = self.png_to_jpg(png)

        jpg_name = ''.join(img_name.split('.')[:-1])+'.jpg'
        jpg.save(img_dir.joinpath(jpg_name), 'JPEG', quality=100)
        return jpg_name


    def convert_png(self) -> None:
        jpg_info = []
        for img_name, img_ext in zip(self.df['filename'], self.df['file_ext']):
            if img_ext=='png':
                jpg_name = self.load_png_save_jpg(self.files_dir, img_name)
                self.files_dir.joinpath(img_name).unlink()
                jpg_info.append((False, jpg_name, self.files_dir.joinpath(jpg_name)))
            else: 
                jpg_info.append((True, img_name, self.files_dir.joinpath(img_name)))
        
        self.df[['is_jpg','filename','file_dir']] = jpg_info


    def is_color(self, img_dir: str) -> bool:
        img = open_img(img_dir)
        w, h = img.size
        for i in range(w):
            for j in range(h):
                r, g, b = img.getpixel((i,j))
                if r != g != b: 
                    return True
        return False

    
    def remove_background(self, img_dir: str) -> None:
        img = imread(str(img_dir))
        segm = SelfiSegmentation()

        new_img = segm.removeBG(img, (255,255,255), threshold=0.6)
        new_img = cvtColor(new_img, COLOR_BGR2RGB)
        new_img = fromarray(new_img)

        new_img = self.png_to_jpg(new_img)
        new_img.save(img_dir, 'JPEG', quality=100)

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

    def zip_dir(self) -> None:
        make_archive(self.dates_range, 'zip', self.base_dir)
        self.zip_dir = self.base_dir.joinpath(self.dates_range + '.zip')

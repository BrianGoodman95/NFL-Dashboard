import pathlib
import os

class Create_Directories():
    def __init__(self):
        dir_path = pathlib.Path().absolute()
        if 'home/BGoodman95' in str(dir_path): #The Python Anywhere Dashboard
            Data_Path = "NFL-Dashboard/data"
        else:
            Data_Path = "data"
        self.project_path = f'{str(dir_path)}/{Data_Path}'
        try:
            os.mkdir(Data_Path)
        except FileExistsError:
            pass
        self.Data_folders = ['raw data', 'compiled', 'compiled/evaluations']
        for folder_path in self.Data_folders:
            try:
                os.mkdir(f'{Data_Path}/{folder_path}')
                print(f'Created Directory {folder_path}')
            except FileExistsError:
                pass

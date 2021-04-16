from tqdm import tqdm
import time
import os


class Deleting:
    def __init__(self, path = '.'):
        self.path = path
        self.path_userdb = self.path + '/userdb/'
        
    def start_deleting(self):
        try:
            if os.path.exists(self.path_userdb): # 1. userdb 폴더가 존재하는 경우
                self.lst = os.listdir(self.path_userdb)
                if self.lst[0] == 'userDB.csv': # userdb 폴더가 있고, userdb.csv 파일이 있는 경우
                    for file in tqdm(os.scandir(self.path_userdb)):
                        os.remove(file.path)
                else: # userdb 폴더가 있지만, userdb.csv 파일이 없는 경우
                    pass
            else: # 2. userdb 폴더가 존재하지 않는 경우
                pass
        except:
            pass

    def run(self):
        self.start_deleting()
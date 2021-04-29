from tqdm import tqdm
import pandas as pd
import chardet
import os

class Course:
    def __init__(self, path = '.'):
        self.path = path
        self.path_sg_course_lst = self.path + '/data/sg_course_lst/'
    
    def make_course_lst(self):
        data_lst = os.listdir(self.path_sg_course_lst)
        # 1. 결과 변수 생성
        self.year = [16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21]
        self.semester = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
        self.course_lst = []
        # 2. 전처리 시작
        for data, year, semester in tqdm(zip(data_lst, self.year, self.semester)):
            save_data = list(pd.read_csv(self.path_sg_course_lst + data, encoding = 'UTF-8-SIG')['과목명'])
            save_data = pd.DataFrame(save_data, columns = ['과목명'])
            save_data.drop_duplicates(inplace = True)
            save_data.reset_index(inplace = True, drop = True)
            (save_data.과목명).to_csv(self.path_sg_course_lst + 'course_lst_' + str(year) + '_' + str(semester) + '.txt', sep = ',', index = False)
        # 3. 전체 과목 생성
        for name in data_lst:
            if name != 'courses_2021_1.csv':
                self.courses = pd.read_csv(self.path_sg_course_lst + name, encoding = 'UTF-8-SIG')
                self.course_lst += list(self.courses['과목명'])
            else:
                self.courses = pd.read_csv(self.path_sg_course_lst + name, encoding = 'UTF-8-SIG')
                self.course_lst += list(self.courses['과목명'])
                self.course_lst = sorted(list(set(self.course_lst)))
        self.course_lst = pd.DataFrame(self.course_lst, columns = ['과목명'])
        (self.course_lst.과목명).to_csv(self.path_sg_course_lst + 'course_lst_total.txt', sep = ',', index = False, encoding = 'UTF-8-SIG')
    
    def run(self):
        self.make_course_lst()

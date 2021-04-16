from functools import reduce
from tqdm import tqdm
import pandas as pd
import chardet
import os

pd.options.mode.chained_assignment = None

class Competition:
    def __init__(self, path = '.'):
        self.path = path
        self.path_sg_competition_lst = self.path + '/data/sg_competition/'
        
    def make_competition_lst(self):
        data_lst = os.listdir(self.path_sg_competition_lst)
        for name in tqdm(data_lst):
            name_tmp = name[:6]
            # 1. 데이터 불러오기
            comp = pd.read_csv(self.path_sg_competition_lst + name, encoding = 'UTF-8-SIG')
            # 2. 데이터 컬럼 이름 재정의
            if name_tmp in ['2016_1', '2016_2', '2017_1']:
                comp.rename(columns = {'입력코드' : '과목코드-분반', '1학년' : name_tmp + '_1학년',
                                                               '2학년' : name_tmp + '_2학년', '3학년' : name_tmp + '_3학년',
                                                               '4학년' : name_tmp + '_4학년'}, inplace = True)
            elif name_tmp in ['2017_2', '2018_1']:
                comp.rename(columns = {'입력코드' : '과목코드-분반', '1학년' : name_tmp + '_1학년',
                                                               '2학년' : name_tmp + '_2학년', '3학년' : name_tmp + '_3학년',
                                                               '4학년' : name_tmp + '_4학년'}, inplace = True)
            elif name_tmp in ['2018_2', '2019_1']:
                comp.rename(columns = {'입력코드' : '과목코드-분반', '1학년' : name_tmp + '_1학년',
                                                               '2학년' : name_tmp + '_2학년', '3학년 ' : name_tmp + '_3학년',
                                                               '4학년' : name_tmp + '_4학년'}, inplace = True)
            elif name_tmp in ['2019_2']:
                comp.rename(columns = {'과목분반' : '과목코드-분반', '1학년' : name_tmp + '_1학년',
                                                               '2학년' : name_tmp + '_2학년', '3학년 ' : name_tmp + '_3학년',
                                                               '4학년' : name_tmp + '_4학년'}, inplace = True)
            else:
                comp.rename(columns = {'과목코드+분반코드' : '과목코드-분반', '1학년' : name_tmp + '_1학년',
                                                               '2학년' : name_tmp + '_2학년', '3학년' : name_tmp + '_3학년',
                                                               '4학년' : name_tmp + '_4학년'}, inplace = True)
            # 3. 데이터 인덱스 순서 재정의
            if name_tmp in ['2016_1', '2016_2', '2017_1']:
                comp = comp.reindex(columns = ['과목코드-분반', '과목명',name_tmp + '_1학년',
                                                                             name_tmp + '_2학년', name_tmp + '_3학년', name_tmp + '_4학년'])
            elif name_tmp in ['2017_2', '2018_1', '2018_2', '2019_1', '2019_2']:
                comp = comp.reindex(columns = ['과목코드-분반', '과목명', name_tmp + '_1학년',
                                                                             name_tmp + '_2학년', name_tmp + '_3학년', name_tmp + '_4학년'])
            else:
                comp = comp.reindex(columns = ['과목코드-분반', '과목명', name_tmp + '_1학년',
                                                                             name_tmp + '_2학년', name_tmp + '_3학년', name_tmp + '_4학년'])
            # 4. 데이터 인덱스 정의
            comp.set_index(['과목코드-분반'], inplace = True)
            # 5. 데이터 저장하기
            comp.to_csv(self.path_sg_competition_lst+ name, encoding = 'UTF-8-SIG', index = True)

    def merge_comp_data(self):
        data_lst = os.listdir(self.path_sg_competition_lst)
        for name in tqdm(data_lst):
            globals()['comp_' + name[:6]] = pd.read_csv(self.path_sg_competition_lst + name, encoding = 'UTF-8-SIG', index_col = 0)
        comp_lst = [comp_2016_1, comp_2016_2, comp_2017_1, comp_2017_2, comp_2018_1, comp_2018_2, comp_2019_1, 
                              comp_2019_2, comp_2020_1, comp_2020_2, comp_2021_1]
        comp_merged = reduce(lambda  left, right: pd.merge(left, right, on = ['과목코드-분반', '과목명'], how = 'outer'), comp_lst)
        comp_merged.to_csv(self.path_sg_competition_lst + 'competition.csv', encoding = 'UTF-8-SIG', index = True)
        
    def run(self):
        self.make_competition_lst()
        self.merge_comp_data()
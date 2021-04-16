import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')

from tqdm import tqdm
tqdm.pandas()

class Ratio:
    def __init__(self, path = '.'):
        self.path = path
        self.path_evaluation = self.path + '/data/et_evaluation/'
        self.path_schedule = self.path + '/data/et_schedule/'
        self.path_capa = self.path + '/data/sg_capacity/'
        self.path_competition = self.path + '/data/et_competition/'
        
    def make_ratio(self):
        def make_df(period):
            self.schedule = pd.read_csv(self.path_schedule + 'schedule_' + period + '.csv', encoding = 'UTF-8-SIG')
            self.capacity = pd.read_csv(self.path_capa +  'courses_' + period + '.csv', encoding = 'UTF-8-SIG')

            self.capacity['분반'] = self.capacity['분반'].astype(str).str.zfill(2)
            self.capacity['과목코드'] = self.capacity['과목번호'] + '-' + self.capacity['분반']
            self.capacity = self.capacity[['과목번호', '분반', '과목코드', '수강생수']]

            return pd.merge(self.schedule, self.capacity, left_on = '과목번호-분반', right_on = '과목코드')[['과목번호', '분반', '과목코드', '과목명', '교수', '담은 인원', '수강생수']]
        def make_exp(lst_stu):
            lst_stu = [stu for stu in lst_stu if stu != 0]
            if len(lst_stu) == 4:
                exp = lst_stu[0] * 0.4 + lst_stu[1] * 0.3 + lst_stu[2] * 0.2 + lst_stu[3] * 0.1
            elif len(lst_stu) == 3:
                exp = lst_stu[0] * 0.5 + lst_stu[1] * 0.3 + lst_stu[2] * 0.2
            else:
                exp = lst_stu[0] * 0.6 + lst_stu[1] * 0.4
            return np.ceil(exp)
        def expect_capacity(df, pre_df1, pre_df2, pre_df3, pre_df4):
            df = pd.merge(df, pre_df1, on = ['과목명', '교수'], how = 'left', suffixes = ('_0', '_1'))
            df = pd.merge(df, pre_df2, on = ['과목명', '교수'], how = 'left', suffixes = ('_1', '_2'))
            df = pd.merge(df, pre_df3, on = ['과목명', '교수'], how = 'left', suffixes = ('_2', '_3'))
            df = pd.merge(df, pre_df4, on = ['과목명', '교수'], how = 'left')

            df.drop(columns = ['과목번호_1', '분반_1', '과목코드_1', '담은 인원_1', '과목번호_2', '분반_2', '과목코드_2', '담은 인원_2', 
                               '과목번호_3', '분반_3', '과목코드_3', '담은 인원_3', '과목번호', '분반', '과목코드', '담은 인원'], inplace = True)
            df.rename(columns = {'수강생수' : '수강생수_전전전전', '과목번호_0' : '과목번호', '분반_0' : '분반', '과목코드_0' : '과목코드', '담은 인원_0' : '담은인원', '수강생수_0' : '수강생수', 
                                 '수강생수_1' : '수강생수_전', '수강생수_2' : '수강생수_전전', '수강생수_3' : '수강생수_전전전'}, inplace = True)
            df.drop_duplicates(['과목번호', '분반'], keep = 'first', inplace = True)

            df.dropna(thresh = 9, inplace = True)
            df.drop(df[df.과목코드 == 'PHIQ981-01'].index, inplace = True)
            df.reset_index(drop = True, inplace = True)

            df['count_null'] = df.apply(lambda x : x.isnull().sum(), axis = 1)
            df.fillna(0, inplace = True)
            df['exp_capa'] = 0

            for i in range(len(df)):
                lst_stu = df.loc[i, '수강생수_전':'수강생수_전전전전'].to_list()
                exp = make_exp(lst_stu)
                df['exp_capa'][i] = exp
            
            df.drop(columns = ['수강생수_전', '수강생수_전전', '수강생수_전전전', '수강생수_전전전전', 'count_null'], inplace = True)
            return df
        def count_reviews(df):
            # 강의평 개수 구하기
            self.evaluation = pd.read_csv(self.path_evaluation + 'evaluation.csv', encoding = 'UTF-8-SIG')
            self.evaluation.dropna(inplace = True)
            self.evaluation = (self.evaluation).groupby(['과목명', '교수명'])['수강평'].unique().to_frame().reset_index()
            self.evaluation['개수'] = self.evaluation['수강평'].progress_apply(lambda x : len(x))
            
            df = pd.merge(df, self.evaluation, left_on = ['과목명', '교수'], right_on = ['과목명', '교수명'], how = 'left')
            df.fillna(0, inplace = True)
            df.drop(columns = ['교수명', '수강평'], inplace = True)
            df.rename(columns = {'개수' : 'review'}, inplace = True)
            return df
        def ispopular(df):
            popular_lst = ['MGT', 'ECO']
            df['popular'] = 0
            idx = df[df.과목번호.str[:3].isin(popular_lst)].index
            df.loc[idx, 'popular'] = 1
            return df
        def make_score(df):
            df['score'] = 0
            idx1 = df[df['popular'] == 1].index
            idx2 = df[df['popular'] != 1].index
            df.loc[idx1, 'score'] = (df.loc[idx1, '담은인원'] * 1.3 / df.loc[idx1, 'exp_capa']) * (1 + df.loc[idx1, 'review'] / 1000) * 1.3
            df.loc[idx2, 'score'] = (df.loc[idx2, '담은인원'] * 1.3 / df.loc[idx2, 'exp_capa']) * (1 + df.loc[idx2, 'review'] / 1000)
            df.reset_index(drop = True, inplace = True)
            df = df.sort_values(by = 'score', ascending = False)
            return df
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.data_21_1 = make_df('2021_1')
        self.data_20_2 = make_df('2020_2')
        self.data_20_1 = make_df('2020_1')
        self.data_19_2 = make_df('2019_2')
        self.data_19_1 = make_df('2019_1')
        self.data = expect_capacity(self.data_21_1, self.data_20_2, self.data_20_1, self.data_19_2, self.data_19_1)
        self.data = count_reviews(self.data)
        self.data = ispopular(self.data)
        self.data = make_score(self.data)
        self.data.to_csv(self.path_competition + 'competition_ratio.csv', encoding = 'UTF-8-SIG', index = False)
        
    def run(self):
        self.make_ratio()
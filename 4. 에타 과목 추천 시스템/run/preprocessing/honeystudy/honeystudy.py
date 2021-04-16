import pandas as pd
import numpy as np
import os
import re

from konlpy.tag import *
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

tqdm.pandas()
okt = Okt()
pd.set_option('display.max_row', 100)

class HoneyStudy:
    def __init__(self, path = '.'):
        self.path = path
        self.path_evaluation = self.path + '/data/et_evaluation/'
        self.path_schedule = self.path + '/data/et_schedule/'
        self.path_hs = self.path + '/data/et_honeystudy/'
        
    def make_honeystudy(self):
        self.evaluation = pd.read_csv(self.path_evaluation + 'evaluation.csv', encoding = 'UTF-8-SIG')
        self.evaluation.dropna(inplace = True)
        self.evaluation.reset_index(inplace = True, drop = True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        def change_grade(x):
            if x == '학점느님':
                x = int(6)
            elif x == '비율 채워줌':
                x = int(2)
            elif x == '매우 깐깐함':
                x = int(-2)
            else:
                x = int(-6)
            return x
        def clean_string(text):
            recom = re.compile('[^ \.\,\?\!a-zA-Z0-9\u3131-\u3163\uac00-\ud7a3]+')
            text = recom.sub('', text)
            return text
        def change_homework(x):
            if x == '많음':
                x = int(-3)
            elif x == '보통':
                x = int(0)
            else:
                x = int(3)
            return x
        def change_teamwork(x):
            if x == '없음':
                x = int(3)
            else:
                x = int(-6)
            return x
        def change_count(x):
            if x == '없음':
                x = 0
            elif x == '한 번':
                x = 1
            elif x == '두 번':
                x = 2
            elif x == '세 번':
                x = 3
            else:
                x = 4
            return x
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.evaluation['학점비율'] = self.evaluation['학점비율'].apply(lambda x : change_grade(x))
        self.grade_score = (self.evaluation).groupby(['과목명', '교수명'])['학점비율'].mean().to_frame().reset_index().sort_values(by = '과목명')
        self.total_score = (self.evaluation).groupby(['과목명', '교수명'])['전체평점'].mean().to_frame().reset_index()
        self.total_score = self.total_score[self.total_score['전체평점'] != 0.0].reset_index(drop = True)
        self.evaluation_num = (self.evaluation).groupby(['과목명', '교수명'])['수강평'].unique().to_frame().reset_index()
        self.evaluation_num['강의평개수'] = self.evaluation_num['수강평'].apply(lambda x : len(x))
        self.evaluation['수강평'] = self.evaluation['수강평'].progress_apply(lambda x : clean_string(x))
        self.evaluation['토큰'] = self.evaluation['수강평'].progress_apply(lambda x : okt.morphs(x, stem = True))
        self.evaluation['토큰'] = self.evaluation['토큰'].str.join(sep = ' ')
        self.evaluation_frame1 = (self.evaluation).groupby(['과목명', '교수명'])['수강평'].unique().to_frame().reset_index()
        self.evaluation_frame1['수강평'] = self.evaluation_frame1['수강평'].str.join(sep = ' ')
        self.evaluation_frame2 = (self.evaluation).groupby(['과목명', '교수명'])['토큰'].unique().to_frame().reset_index()
        self.evaluation_frame2['토큰'] = self.evaluation_frame2['토큰'].str.join(sep = ' ')
        self.evaluation['과제'] = self.evaluation['과제'].apply(lambda x : change_homework(x))
        self.homework_score = (self.evaluation).groupby(['과목명', '교수명'])['과제'].mean().to_frame().reset_index()
        self.evaluation['조모임'] = self.evaluation['조모임'].apply(lambda x : change_teamwork(x))
        self.teamwork_score = (self.evaluation).groupby(['과목명', '교수명'])['조모임'].mean().to_frame().reset_index()
        self.evaluation['시험횟수'] = self.evaluation['시험횟수'].apply(lambda x : change_count(x))
        self.exam_num = (self.evaluation).groupby(['과목명', '교수명'])['시험횟수'].mean().to_frame().reset_index()
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.result = pd.concat([self.grade_score, self.total_score.iloc[:, 2], self.homework_score.iloc[:, 2], self.teamwork_score.iloc[:, 2],
                                                   self.exam_num.iloc[:, 2], self.evaluation_num.iloc[:, 3], self.evaluation_frame1.iloc[:, 2],
                                                   self.evaluation_frame2.iloc[:, 2]], axis = 1)
        self.result.dropna(inplace = True)
        self.result.reset_index(inplace = True, drop = True)
        self.result.to_csv(self.path_hs + 'result.csv', index = False, encoding = 'UTF-8-SIG')
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.result = pd.read_csv(self.path_hs + 'result.csv', encoding = 'UTF-8-SIG')
        self.result.dropna(inplace = True)
        self.result.reset_index(inplace = True, drop = True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.result['꿀수강'] = 0
        self.result['배움수강'] = 0
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.positive_honey_lst = ['God', 'HOnEy', 'honey', 'sofie', '갓', '갓향숙', '강추예욤', '개꿀', '개꿀강임',
                                                       '개꿀스피치', '개띵강', '꿀강', '꿀맛', '꿀잼일', '대천사그래도', '비쁠나옴쁠몰',
                                                       '빛신', '쁠몰같아', '쁠몰이셔', '쁠받', '수월하다쁠몰', '에쁠에제', '좋다천사이십',
                                                       '핵꿀', '꿀', '닥추임', '더꿀', '명강꿀', '빛빛빛', '안빡셉니', '에쁠에쁠', '초초강추',
                                                       '킹', '함꿀강', '후해짐', '힐링', '영접', '에이쁠', '학점느님', '퍼주실', '퍼줍니', '핵핵']
        self.positive_study_lst = ['배울', '빡셈', '빡세다', '개빡', '공부량', '질높', '꼽는', '명강', '노고', '빡공', '사례분석', '9학점이라', '9학점같은', '9학점짜리', '9학점입니다'
                                                      '9학점만큼', '9학점 수업', '아우라', '어려움', '어렵다', '어료워', '유의사항', '착취', '참뜻', '컨설턴트', '컨설팅계', '컨설팅쪽', '컨설팅펌'
                                                      '특효약', '헬', '배우는', '너무 어려']
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.hn = self.result[(self.result['학점비율'] == 6) & (self.result['조모임'] == 3) & (self.result['전체평점']  >= 4) & (self.result['시험횟수'] != 4) & (self.result['시험횟수'] != 3) & (self.result['강의평개수'] > 2)]
        self.hl = self.result[~((self.result['학점비율'] == 6) & (self.result['조모임'] == 3) & (self.result['전체평점']  >= 4) & (self.result['시험횟수'] != 4) & (self.result['시험횟수'] != 3) & (self.result['강의평개수'] > 2))]
        self.hn_final = ''
        self.hn_lst = list(self.hn['토큰'].values)
        self.hl_final = ''
        self.hl_lst = list(self.hl['토큰'].values)
        for i in tqdm(self.hn_lst):
            self.hn_final += i
        for i in tqdm(self.hl_lst):
            self.hl_final += i
        self.hn_final = self.hn_final.split(' ')
        self.hn_final = sorted(list(set(self.hn_final)))
        self.hl_final = self.hl_final.split(' ')
        self.hl_final = sorted(list(set(self.hl_final)))
        self.honey_final = sorted(list(set(self.hn_final) - set(self.hl_final)))
        self.honey_final = [re.compile('^[?!.,0123456789]+').sub('', i) for i in self.honey_final]
        self.honey_final = [re.compile('^[?!.,0123456789]+').sub('', i) for i in self.honey_final]
        self.honey_final = sorted(list(set(self.honey_final)))
        for i in tqdm(range(len(self.result))):
            self.cnt = 0
            for text in self.positive_honey_lst:
                self.cnt += self.result['토큰'][i].count(text)
                if text in ['개꿀', '힐링']:
                    self.cnt += 2
            self.result['꿀수강'][i] = self.cnt
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.lot_outcome = self.result[(self.result['전체평점']  >= 4) & (self.result['강의평개수'] > 3) & (self.result['시험횟수'] >= 2) & (self.result['과제'] == -3)]
        self.not_outcome = self.result[~((self.result['전체평점']  >= 4) & (self.result['강의평개수'] > 3) & (self.result['시험횟수'] >= 2) & (self.result['과제'] != 3))]
        self.lot_outcome_final = ''
        self.lot_outcome_lst = list(self.lot_outcome['토큰'].values)
        self.not_outcome_final = ''
        self.not_outcome_lst = list(self.not_outcome['토큰'].values)
        for i in self.lot_outcome_lst:
            self.lot_outcome_final += i
        for i in self.not_outcome_lst:
            self.not_outcome_final += i
        self.lot_outcome_final = self.lot_outcome_final.split(' ')
        self.lot_outcome_final = sorted(list(set(self.lot_outcome_final)))
        self.not_outcome_final = self.not_outcome_final.split(' ')
        self.not_outcome_final = sorted(list(set(self.not_outcome_final)))
        self.study_final = sorted(list(set(self.lot_outcome_final) - set(self.not_outcome_final)))
        self.study_final = [re.compile('^[?!.,0123456789]+').sub('', i) for i in self.study_final]
        self.study_final = [re.compile('^[?!.,0123456789]+').sub('', i) for i in self.study_final]
        self.study_final = sorted(list(set(self.study_final)))
        for i in tqdm(range(len(self.result))):
            self.cnt = 0
            for text in self.positive_study_lst:
                self.cnt += self.result['수강평'][i].count(text)
                self.cnt += self.result['토큰'][i].count(text)
                if text in ['명강',  '9학점이라', '9학점같은', '9학점짜리', '9학점입니다', '9학점만큼', '9학점 수업', '빡공']:
                    self.cnt += 1
            self.result['배움수강'][i] = self.cnt
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.result['honey_score'] = (1 + self.result['강의평개수']/100) * (self.result['전체평점'] + self.result['학점비율'] + self.result['과제'] + self.result['조모임'] + (self.result['꿀수강']/self.result['강의평개수'] ))
        self.result['study_score'] = (1 + self.result['강의평개수']/20) * (self.result['전체평점'] - self.result['과제'] + self.result['시험횟수'] + (self.result['배움수강']/self.result['강의평개수']))
        self.result.reset_index(drop = True, inplace = True)
        self.result.to_csv(self.path_hs + 'honeystudy.csv', index = False, encoding = 'UTF-8-SIG')
        
    def run(self):
        self.make_honeystudy()
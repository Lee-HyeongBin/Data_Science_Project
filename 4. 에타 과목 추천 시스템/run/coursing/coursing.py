from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import os
import re

import datetime
import warnings
 
from IPython.display import display
from IPython.display import clear_output

tqdm.pandas()
now = datetime.datetime.now()
warnings.filterwarnings(action='ignore')

class Coursing:
    def __init__(self, path = '.'):
        self.path = path
        self.path_db = self.path + '/userDB/'
        self.path_save = self.path + '/result/source/'
        self.path_answer = self.path + '/result/answer/'
        
    def make_coursing(self):
        self.tmp_result = pd.read_csv(self.path_save + 'tmp_result.csv', encoding = 'UTF-8-SIG')
        self.final_result = pd.read_csv(self.path_save + 'final_result.csv', encoding = 'UTF-8-SIG')
        self.userdb = pd.read_csv(self.path_db + 'userDB.csv', encoding = 'UTF-8-SIG')
        
        # 임의로 추가한 인공지능, 빅사, 융소 과목 추가
        self.final_result = self.final_result.append(self.tmp_result)
        self.final_result = self.final_result.drop_duplicates(subset = ['과목명', '교수명', '소속', '과목코드', '수업시간', '수업요일'], keep = 'last')
        self.final_result.reset_index(drop = True, inplace = True)

        
        # 1. 전처리
        self.final_result.학점 = self.final_result.학점.astype(int)
        self.final_result.꿀점수 = self.final_result.꿀점수.astype(int)
        self.final_result.배움점수 = self.final_result.배움점수.astype(int)
        self.final_result.권장학년 = self.final_result.권장학년.astype(str)
        self.stars = ['알바트로스세미나', '알바트로스세미나(경영)', '화공산업과기술경영-기업가정신', '모형설계제작', '특수연구', '전자회로실험', '기초전자공학실험',
                       '2DCAD', '분석화학실험', '생화학실험', '마이크로프로세서응용실험', '영어논리/논증적글쓰기의이론과실제', '제2언어습득론입문:이론과적용']
        self.final_result = self.final_result[~(self.final_result['과목명'].isin(self.stars))]
        self.final_result = self.final_result[~(self.final_result['소속'] == '한국사회문화')]
        self.final_result = self.final_result[~(self.final_result['수업요일'] == '토')]
        
        self.final_result.drop_duplicates(inplace = True, keep = 'last')
        self.final_result.reset_index(inplace = True, drop = True)
        
        for name in list(self.userdb.columns):
            if name in ['학번', '이름', '본전공', '복수전공', '필수과목1', '필수과목2', '필수과목3', '시간표테마', '공강', '시간표유형1', '시간표유형2']:
                self.userdb[name] = self.userdb[name].astype(str)
            else:
                self.userdb[name] = self.userdb[name].astype(int)
        self.recommend_answer = pd.DataFrame(columns = ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수'])
        
        # 2. 유저DB
        self.user1 = self.userdb
        
        # 3. 추천받고 싶은 학기 전처리 (중요!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 추후 수정!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
        def change_name(x):
            x = re.sub('Ⅵ', '6', x)
            x = re.sub('Ⅴ', '5', x)
            x = re.sub('Ⅳ', '4', x)

            x = re.sub('IV', '4', x)
            x = re.sub('IIII', '4', x)
            x = re.sub('III', '3', x)
            x = re.sub('II', '2', x)
            x = re.sub('I', '1', x)
            x = re.sub('Ⅱ', '2', x)
            x = re.sub('Ⅰ', '1', x)

            x = re.sub('1ntro', 'Intro', x)
            x = re.sub('1mmersive', 'Immersive', x)
            x = re.sub('A1', 'AI', x)
            x = re.sub('1nquiry', 'Inquiry', x)
            x = re.sub('1ntermediate', 'Intermediate', x)
            x = re.sub('1oT', 'IoT', x)
            x = re.sub('U1/UX', 'UI/UX', x)
            x = re.sub('VLS1', 'VLSI', x)
            x = re.sub('1MC', 'IMC', x)
            x = re.sub('·', '', x)
            return x
        
        self.year, self.semester = 2021, 1
        self.first_pre = pd.read_csv(self.path + '/data/sg_course_lst/courses_' + str(self.year) + '_' + str(self.semester) + '.csv').loc[:, ['과목번호', '분반', '과목명', '교수진', '수업시간/강의실']]
        
        def withdraw_day(x):
            result = []
            if x.count('월') != 0:
                result.append('월')
            if x.count('화') != 0:
                result.append('화')
            if x.count('수') != 0:
                result.append('수')
            if x.count('목') != 0:
                result.append('목')
            if x.count('금') != 0:
                result.append('금')
            if x.count('토') != 0:
                result.append('토')
            return result

        def withdraw_class(x):
            try:
                x = x.split('[')[1][:-1]
                return x
            except:
                return '없음'

        def withdraw_time(x):
            x = re.compile('^[월,화,수,목,금,토]+').sub('', x).lstrip()[:11]
            return x
        
        def change_day(x):
            x = str(x)
            x = ''.join(x)
            x = re.sub(",", "", x)
            x = re.sub(" ", "", x)
            x = re.sub("'", "", x)
            return x
        
        def change_day2(x):
            x = x.lstrip('[')
            x = x.rstrip(']')
            x = x.strip()
            return x
        
        self.first_pre.dropna(subset = ['수업시간/강의실'], inplace = True)
        self.first_pre.reset_index(drop = True, inplace = True)
        
        self.first_pre['수업요일'] = self.first_pre['수업시간/강의실'].apply(lambda x : withdraw_day(x))
        self.first_pre['수업요일'] = self.first_pre['수업요일'].apply(lambda x : change_day(x))
        self.first_pre['수업요일'] = self.first_pre['수업요일'].apply(lambda x : change_day2(x))
        self.first_pre['수업시간'] = self.first_pre['수업시간/강의실'].apply(lambda x : withdraw_time(x))
        self.first_pre['강의실'] = self.first_pre['수업시간/강의실'].apply(lambda x : withdraw_class(x))
        self.first_pre['과목명'] = self.first_pre['과목명'].apply(lambda x : change_name(x))
        self.first_pre.columns = ['과목번호', '분반', '과목명', '교수명', '수업시간/강의실', '수업요일', '수업시간', '강의실']
        self.first_pre.drop(['수업시간/강의실'], axis = 1, inplace = True)
        self.first_pre.drop(['과목번호', '분반'], axis = 1, inplace = True)
        self.first_pre.drop_duplicates(inplace = True, keep = 'last')
        self.first_pre.reset_index(inplace = True, drop = True)
        
        self.final_result = pd.merge(self.first_pre, self.final_result, how = 'left', on = ['과목명', '교수명', '수업시간', '수업요일', '강의실'])
        self.final_result.dropna(subset = ['수업시간'], inplace = True)
        self.final_result.dropna(subset = ['수업요일'], inplace = True)
        self.final_result.drop_duplicates(inplace = True, keep = 'last')
        self.final_result.reset_index(inplace = True, drop = True)
        
        # 임의로 일부 과목 권장학년 수정하기
        self.idx1 = self.final_result[self.final_result['과목명'].isin(['조직행동이론', '재무관리', '생산관리론', '선형대수학', '기초C언어', '기초java언어', '1T개론', 'IT개론', 'C언어기초', '거시경제학1', '고급공학수학1', '고급공학수학2', '자료구조', '컴퓨터공학설계및실험1', '마케팅원론'])].index
        self.idx2 = self.final_result[self.final_result['과목명'].isin(['중급회계2', '세무회계', '원가회계', '응용경영통계', '확률및랜덤변수'])].index
        self.idx3 = self.final_result[self.final_result['과목명'].isin(['Data&AI', '응용수학1', '응용수학2', '이산구조'])].index
        self.idx4 = self.final_result[self.final_result['과목명'].isin(['고급회계', '회계감사'])].index
        self.final_result.loc[self.idx1, '권장학년'] = '23'
        self.final_result.loc[self.idx2, '권장학년'] = '34'
        self.final_result.loc[self.idx2, '권장학년'] = '12'
        self.final_result.loc[self.idx2, '권장학년'] = '4'
        self.final_result.drop_duplicates(inplace = True, keep = 'last')
        self.final_result.reset_index(inplace = True, drop = True)
        
        # 인공지능, 빅데이터사이언스, 융합소프트웨어, 경영 겹치는 과목 처리
        if (self.userdb.loc[len(self.userdb)-1, '본전공'] in (['경영학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] not in (['빅데이터사이언스', '융합소프트웨어', '인공지능'])):
            self.not_by_idx = self.final_result[~((self.final_result['소속'] == '빅데이터사이언스') | (self.final_result['소속'] == '융합소프트웨어') | (self.final_result['소속'] == '인공지능'))].index
            self.final_result = self.final_result.loc[self.not_by_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] not in (['경영학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] in (['빅데이터사이언스', '융합소프트웨어', '인공지능'])):
            self.not_bu_idx = self.final_result[self.final_result['소속'] != '경영학'].index
            self.final_result = self.final_result.loc[self.not_bu_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] not in (['경영학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] in (['경영학'])):
            self.not_bi_idx = self.final_result[~((self.final_result['소속'] == '빅데이터사이언스') | (self.final_result['소속'] == '융합소프트웨어') | (self.final_result['소속'] == '인공지능'))].index
            self.final_result = self.final_result.loc[self.not_bi_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] in (['경영학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] in (['빅데이터사이언스', '융합소프트웨어', '인공지능'])):
            self.not_ab_idx = self.final_result[~(self.final_result['소속'] == '경제학')].index
            self.final_result = self.final_result.loc[self.not_ab_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] in (['경제학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] not in (['빅데이터사이언스', '융합소프트웨어', '인공지능'])):
            self.not_ey_idx = self.final_result[~((self.final_result['소속'] == '빅데이터사이언스') | (self.final_result['소속'] == '융합소프트웨어') | (self.final_result['소속'] == '인공지능'))].index
            self.final_result = self.final_result.loc[self.not_ey_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] not in (['경제학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] in (['빅데이터사이언스', '융합소프트웨어', '인공지능'])):
            self.not_eu_idx = self.final_result[self.final_result['소속'] != '경제학'].index
            self.final_result = self.final_result.loc[self.not_eu_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] not in (['경제학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] in (['경제학'])):
            self.not_ei_idx = self.final_result[~((self.final_result['소속'] == '빅데이터사이언스') | (self.final_result['소속'] == '융합소프트웨어') | (self.final_result['소속'] == '인공지능'))].index
            self.final_result = self.final_result.loc[self.not_ei_idx, :]
        elif (self.userdb.loc[len(self.userdb)-1, '본전공'] in (['경제학'])) & (self.userdb.loc[len(self.userdb)-1, '복수전공'] in (['빅데이터사이언스', '융합소프트웨어', '인공지능'])):
            self.not_cd_idx = self.final_result[~(self.final_result['소속'] == '경영')].index
            self.final_result = self.final_result.loc[self.not_cd_idx, :]
            
        self.final_result.drop_duplicates(inplace = True, keep = 'last')
        self.final_result.reset_index(inplace = True, drop = True)        
        
        # 4. 필수과목 추가
        def cut_must(user_data, final_data):
            must1 = user_data.loc[len(user_data)-1, '필수과목1']
            must2 = user_data.loc[len(user_data)-1, '필수과목2']
            must3 = user_data.loc[len(user_data)-1, '필수과목3']
            final_data = final_data[(final_data['과목명'] == must1) | (final_data['과목명'] == must2) | (final_data['과목명'] == must3)]
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            return final_data
        self.recommend_answer = self.recommend_answer.append(cut_must(self.userdb, self.final_result))
        
        ## 필수과목과 겹치는 시간 삭제하기
        self.lst1 = []
        for i in range(len(self.recommend_answer)):
            self.lst1.append([self.recommend_answer['수업요일'][i], self.recommend_answer['수업시간'][i]])
            
        self.lst2 = []
        for i in range(len(self.final_result)):
            self.lst2.append([self.final_result['수업요일'][i], self.final_result['수업시간'][i]])
            
        self.lst3 = []
        for i in range(len(self.lst2)):
            if self.lst2[i] in self.lst1:
                self.lst3.append(i)
                
        self.final_result = self.final_result.drop(self.lst3)
        self.final_result.drop_duplicates(inplace = True, keep = 'last')
        self.final_result.reset_index(drop = True, inplace = True)

        self.recommend_answer = self.recommend_answer.sample(frac=1).reset_index(drop=True)
        self.recommend_answer.drop_duplicates(subset = ['과목명'], keep = 'first', inplace = True)
        self.recommend_answer.drop_duplicates(subset = ['수업요일', '수업시간'], keep = 'first', inplace = True)
        self.recommend_answer.reset_index(inplace = True, drop = True)
        
        # 5. 전공 필터링
        def cut_major(user_data, final_data):
            main_m = user_data.loc[len(user_data)-1, '본전공']
            sub_m = user_data.loc[len(user_data)-1, '복수전공']
            if (user_data.loc[len(user_data)-1, '전공과목수'] != 0) & (user_data.loc[len(user_data)-1, '교양과목수'] != 0):
                final_data = final_data[(final_data['소속'] == main_m) | (final_data['소속'] == sub_m) | (final_data['소속'] == '전인교육원')]
            elif (user_data.loc[len(user_data)-1, '전공과목수'] != 0) & (user_data.loc[len(user_data)-1, '교양과목수'] == 0):
                final_data = final_data[(final_data['소속'] == main_m) | (final_data['소속'] == sub_m)]
            elif (user_data.loc[len(user_data)-1, '전공과목수'] == 0) & (user_data.loc[len(user_data)-1, '교양과목수'] != 0):
                final_data = final_data[final_data['소속'] == '전인교육원']
            elif (user_data.loc[len(user_data)-1, '전공과목수'] == 0) & (user_data.loc[len(user_data)-1, '교양과목수'] == 0):
                print("--------------------------------보여드릴 과목이 없습니다. 전공학점과 교양학점을 확인하시고, 다시 실행 시켜주세요.--------------------------------")
                return None
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            final_data = final_data.loc[:, ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']]
            return final_data
        self.final_result = cut_major(self.user1, self.final_result)
        
        # 6. 학기수 필터링
        def cut_semester(user_data, final_data):
            seme = user_data.loc[len(user_data)-1, '학기수']
            if seme in [8, 9, 10]:
                final_data = final_data[~(final_data['권장학년'].isin(['1', '2', '12', '23']))]
            elif seme in [7]:
                final_data = final_data[~(final_data['권장학년'].isin(['1', '2', '12', '23']))]
            elif seme in [6]:
                final_data = final_data[~(final_data['권장학년'].isin(['1', '2', '12']))]
            elif seme in [5]:
                final_data = final_data[~(final_data['권장학년'].isin(['4', '1']))]
            elif seme in [4]:
                final_data = final_data[~(final_data['권장학년'].isin(['4', '34', '1']))]
            elif seme in [3]:
                final_data = final_data[~(final_data['권장학년'].isin(['4', '34', '24', '3']))]
            elif seme in [2]:
                final_data = final_data[~(final_data['권장학년'].isin(['4', '34', '24', '3']))]
            elif seme in [1]:
                final_data = final_data[~(final_data['권장학년'].isin(['2', '23', '4', '34', '24', '3']))]
            else:
                clear_output()
                print('학기수를 잘못 입력하셨습니다. 커널을 재시작해주세요. (userDB 폴더 삭제 요망)')
                time.sleep(20)
                final_data = final_data[~(final_data['권장학년'].isin(['1', '2', '3', '4', '12', '23', '24', '34', '4']))]
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            final_data = final_data.loc[:, ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']]
            return final_data
        self.final_result = cut_semester(self.user1, self.final_result)
        
        # 7. 공강 필터링
        def cut_gong(user_data, final_data):
            gong = user_data.loc[len(user_data)-1, '공강']
            gong = re.compile('[^월화수목금]+').sub('', gong)
            if len(gong) == 0:
                return final_data
            elif gong == '월':
                final_data = final_data[~(final_data['수업요일'].isin(['월수', '월']))]
            elif gong == '화':
                final_data = final_data[~(final_data['수업요일'].isin(['화목', '화']))]
            elif gong == '수':
                final_data = final_data[~(final_data['수업요일'].isin(['월수', '수금', '수']))]
            elif gong == '목':
                final_data = final_data[~(final_data['수업요일'].isin(['화목', '목']))]
            elif gong == '금':
                final_data = final_data[~(final_data['수업요일'].isin(['수금', '금']))]
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            final_data = final_data.loc[:, ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']]
            return final_data
        self.final_result = cut_gong(self.user1, self.final_result)
        
        # 8. 시간표 유형 필터링
        def cut_type1(user_data, final_data):
            type1 = user_data.loc[len(user_data)-1, '시간표유형1']
            early_bird_lst = ['15:00~17:45', '15:00~18:00', '15:00~18:30', '15:00~18:50', '15:00~19:15', '15:00~19:45',
                                          '15:00~19:50', '15:00~20:50', '16:30~17:20', '16:30~17:45', '16:30~18:00', '16:30~18:10',
                                          '16:30~18:15', '16:30~18:20', '16:30~18:30', '16:30~19:00', '16:30~19:15', '16:30~22:15', '16:40~17:30', '16:40~19:10',
                                          '17:00~18:00', '17:00~18:50', '17:00~19:00', '17:00~19:45', '17:00~20:00', '17:30~19:20', '18:00~18:50', '18:00~19:00',
                                          '18:00~19:15', '18:00~19:20', '18:00~19:30', '18:00~19:45', '18:00~20:00', '18:00~20:45', '18:30~20:00', '18:30~21:15',
                                          '18:30~21:30', '19:30~20:45']
            late_wake_lst = ['09:00~10:15', '09:00~10:50', '09:00~11:45', '09:00~12:00', '10:00~13:00']
            if type1 == '늦잠형':
                final_data = final_data[~(final_data['수업시간'].isin(late_wake_lst))]
            elif type1 == '얼리버드형':
                final_data = final_data[~(final_data['수업시간'].isin(early_bird_lst))]
            else:
                return final_data
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            final_data = final_data.loc[:, ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']]
            return final_data
        self.final_result = cut_type1(self.user1, self.final_result)
        
        # 9. 꿀/배움 필터링
        def cut_honey(user_data, final_data):
            honey1 = user_data.loc[len(user_data)-1, '꿀강의']
            if honey1 == 0:
                return final_data
            elif honey1 == 1:
                pdata = final_data[final_data['꿀점수'] == 1]
                pdata = pdata.sample(n = int(len(pdata)/2))
                qdata = final_data[final_data['꿀점수'] == 0]
                qdata = qdata.sample(n = int(len(qdata)/2))
                pdata = pdata.append(qdata)
                pdata.drop_duplicates(inplace = True)
                pdata.reset_index(drop = True, inplace = True)
                final_data =pdata              
            elif honey1 == 2:
                final_data = final_data[final_data['꿀점수'] == 1]
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            final_data = final_data.loc[:, ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']]
            return final_data
        def cut_study(user_data, final_data):
            study1 = user_data.loc[len(user_data)-1, '배움강의']
            if study1 == 0:
                return final_data
            elif study1 == 1:
                pdata = final_data[final_data['배움점수'] == 1]
                pdata = pdata.sample(n = int(len(pdata)/2))
                qdata = final_data[final_data['배움점수'] == 0]
                qdata = qdata.sample(n = int(len(qdata)/2))
                pdata = pdata.append(qdata)
                pdata.drop_duplicates(inplace = True)
                pdata.reset_index(drop = True, inplace = True)
                final_data =pdata              
            elif study1 == 2:
                final_data = final_data[final_data['배움점수'] == 1]
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            final_data = final_data.loc[:, ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']]
            return final_data
        self.final_result_1 = cut_honey(self.user1, self.final_result)
        self.final_result_2 = cut_study(self.user1, self.final_result)
        self.final_result = self.final_result_1.append(self.final_result_2)
        self.final_result.drop_duplicates(inplace = True, keep = 'last')
        self.final_result.reset_index(inplace = True, drop = True)
        self.final_result = self.final_result.sort_values(by = '소속').reset_index(drop = True)
        
        # 10. 버그 체크
        def last_filter(recom_data, final_data):
            recom_lst = sorted(list(recom_data['과목명'].unique()))
            final_data = final_data[~(final_data['과목명'].isin(recom_lst))]
            final_data.drop_duplicates(inplace = True, keep = 'last')
            final_data.reset_index(inplace = True, drop = True)
            return final_data
        self.final_result = last_filter(self.recommend_answer, self.final_result)
        
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # 1. 과목 추천 기본 변수 설정
        self.user_main_major = self.userdb.loc[len(self.userdb)-1, '본전공']
        self.user_sub_major = self.userdb.loc[len(self.userdb)-1, '복수전공']

        self.main_number = self.userdb.loc[len(self.userdb)-1, '전공과목수']
        self.sub_number = self.userdb.loc[len(self.userdb)-1, '교양과목수']
        
        ## 필수과목안의 전공 과목 수
        self.major_in_recom = len(self.recommend_answer[(self.recommend_answer['소속'] == self.user_main_major) | (self.recommend_answer['소속'] == self.user_sub_major)]['과목명'].unique())

        ## 추가해야 할 전공 과목수
        self.must_plus_major = self.main_number - self.major_in_recom
        
        ## 필수과목안의 교양 과목 수
        self.jeon_in_recom = len(self.recommend_answer[(self.recommend_answer['소속'] != self.user_main_major) & (self.recommend_answer['소속'] != self.user_sub_major)])

        ## 추가해야 할 교양 과목수
        self.must_plus_jeon = self.sub_number - self.jeon_in_recom
        
        self.final_major_df = self.final_result[(self.final_result['소속'] == self.user_main_major) | (self.final_result['소속'] == self.user_sub_major)].reset_index(drop = True)
        self.final_not_major_df = self.final_result[~((self.final_result['소속'] == self.user_main_major) | (self.final_result['소속'] == self.user_sub_major))].reset_index(drop = True)    
        
        # 2. 과목 추천 알고리즘
        def check_plus(df, puzzle):
            tmp = puzzle.copy()
            day1, day2 = 0, 0
            time1, time2 = 0, 0
            df = df.reset_index(drop = True)

            if df.loc[:, '수업요일'].values[len(df)-1] == '월':
                day1 = 1
            elif df.loc[:, '수업요일'].values[len(df)-1] == '화':
                day1 = 2
            elif df.loc[:, '수업요일'].values[len(df)-1] == '수':
                day1 = 3
            elif df.loc[:, '수업요일'].values[len(df)-1] == '목':
                day1 = 4
            elif df.loc[:, '수업요일'].values[len(df)-1] == '금':
                day1 = 5
            elif df.loc[:, '수업요일'].values[len(df)-1] == '월수':
                day1, day2 = 1, 3
            elif df.loc[:, '수업요일'].values[len(df)-1] == '화목':
                day1, day2 = 2, 4
            elif df.loc[:, '수업요일'].values[len(df)-1] == '수금':
                day1, day2 = 3, 5
            else:
                day1, day2 = 0, 0

            if df.loc[:, '수업시간'].values[len(df)-1] == '09:00~10:15':
                time1 = 1
            elif df.loc[:, '수업시간'].values[len(df)-1] == '09:00~10:50':
                time1, time2 = 1, 2
            elif df.loc[:, '수업시간'].values[len(df)-1] == '09:00~11:45':
                time1, time2 = 1, 2
            elif df.loc[:, '수업시간'].values[len(df)-1] == '09:00~12:00':
                time1, time2 = 1, 2
            elif df.loc[:, '수업시간'].values[len(df)-1] == '10:30~11:20':
                time1 = 2
            elif df.loc[:, '수업시간'].values[len(df)-1] ==  '10:30~11:45':
                time1 = 2
            elif df.loc[:, '수업시간'].values[len(df)-1] == '10:30~12:20':
                time1, time2 = 2, 3
            elif df.loc[:, '수업시간'].values[len(df)-1] == '10:30~13:15':
                time1, time2 = 2, 3
            elif df.loc[:, '수업시간'].values[len(df)-1] == '12:00~12:50':
                time1 = 3
            elif df.loc[:, '수업시간'].values[len(df)-1] == '12:00~13:15':
                time1 = 3
            elif df.loc[:, '수업시간'].values[len(df)-1] == '12:00~13:50':
                time1, time2 = 3, 4
            elif df.loc[:, '수업시간'].values[len(df)-1] == '12:00~14:45':
                time1, time2 = 3, 4
            elif df.loc[:, '수업시간'].values[len(df)-1] == '13:30~14:20':
                time1 = 4
            elif df.loc[:, '수업시간'].values[len(df)-1] == '13:30~14:30':
                time1 = 4
            elif df.loc[:, '수업시간'].values[len(df)-1] == '13:30~14:45':
                time1 = 4
            elif df.loc[:, '수업시간'].values[len(df)-1] == '13:30~15:20':
                time1, time2 = 4, 5
            elif df.loc[:, '수업시간'].values[len(df)-1] == '13:30~16:15':
                time1, time2 = 4, 5
            elif df.loc[:, '수업시간'].values[len(df)-1] == '15:00~15:50':
                time1 = 5
            elif df.loc[:, '수업시간'].values[len(df)-1] == '15:00~16:15':
                time1 = 5
            elif df.loc[:, '수업시간'].values[len(df)-1] == '15:00~16:50':
                time1, time2 = 5, 6
            elif df.loc[:, '수업시간'].values[len(df)-1] == '15:00~17:45':
                time1, time2 = 5, 6
            elif df.loc[:, '수업시간'].values[len(df)-1] == '15:30~17:20':
                time1, time2 = 5, 6
            elif df.loc[:, '수업시간'].values[len(df)-1] == '16:30~17:20':
                time1 = 6
            elif df.loc[:, '수업시간'].values[len(df)-1] == '16:30~17:45':
                time1 = 6
            elif df.loc[:, '수업시간'].values[len(df)-1] == '16:30~18:10':
                time1 = 6
            elif df.loc[:, '수업시간'].values[len(df)-1] == '16:30~18:20':
                time1, time2 = 6, 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '16:30~18:30':
                time1, time2 = 6, 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '16:30~19:15':
                time1, time2 = 6, 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '17:00~18:50':
                time1, time2 = 6, 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '17:30~19:20':
                time1, time2 = 6, 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:00~19:15':
                time1 = 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:00~19:20':
                time1 = 7
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:00~19:30':
                time1, time2 = 7, 8
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:00~19:45':
                time1, time2 = 7, 8
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:00~20:00':
                time1, time2 = 7, 8
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:00~20:45':
                time1, time2 = 7, 8
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:30~21:15':
                time1, time2 = 7, 8
            elif df.loc[:, '수업시간'].values[len(df)-1] == '18:30~21:30':
                time1, time2 = 7, 8
            elif df.loc[:, '수업시간'].values[len(df)-1] == '19:30~20:45':
                time1 = 8
            else:
                time1, time2 = 0, 0

            tmp[time1, day1] += 1
            tmp[time2, day1] += 1
            tmp[time1, day2] += 1
            tmp[time2, day2] += 1

            for i in range(1, 9):
                for j in range(1, 6):
                    if tmp[i][j] == int(2):
                        return '에러'
            return tmp
        def choice_major(data, num): # data는 final_major_df, num은 must_plus_major 
            switch = 0
            cnt = 1
            while switch != num:
                data2 = data.copy()
                if cnt == 1000:
                    return pd.DataFrame(columns = list(data.columns))
                cnt += 1
                switch = 0 # 스위치 리셋
                puz = np.zeros((9, 6), dtype = int) # 퍼즐 리셋
                # 랜덤하게 숫자 must_plus_major개 뽑기
                lst = []
                lgth = len(data2)
                ran_num = np.random.randint(0, lgth)
                for i in range(num):
                    while ran_num in lst:
                        ran_num = np.random.randint(0, lgth)
                    lst.append(ran_num)
                lst = sorted(lst)
                # 랜덤한 데이터 프레임 (길이 num) 뽑기
                data2 = data2.iloc[lst, :]
                # 과목명 중복 제거
                data2.drop_duplicates(subset = ['과목명'], inplace = True)
                data2.reset_index(drop = True, inplace = True)
                if len(data2) != num:
                    continue        
                # 뽑힌 데이터 프레임이 퍼즐에 맞는지 확인
                for i in range(len(data2)):
                    if check_plus(data2.iloc[i, :].to_frame().T, puz) != '에러': # '에러'가 아니면 puzzle 결과 계속 유지하면서 다음것도 확인
                        puz = check_plus(data2.iloc[i, :].to_frame().T, puz)
                        switch += 1
                    else: # 에러'면 스위치 초기화
                        switch = 0
                        break
            return data2
        
        if self.must_plus_jeon == 0:
            self.final_result = self.final_result[(self.final_result['소속'] == self.user_main_major) | (self.final_result['소속'] == self.user_sub_major)].reset_index(drop = True)
        
        print("-------------------------------------------------------------------- Processing -------------------------------------------------------------------")
        self.lpoint = 0
        while True:
            self.boss = choice_major(self.final_result, self.must_plus_major + self.must_plus_jeon)
            self.c1 = len(self.boss[(self.boss['소속'] == self.user_main_major) | (self.boss['소속'] == self.user_sub_major)])
            self.c2 = len(self.boss[~((self.boss['소속'] == self.user_main_major) | (self.boss['소속'] == self.user_sub_major))])
            if (self.c1 == self.must_plus_major) and (self.c2 == self.must_plus_jeon):
                self.boss = self.boss.reset_index(drop = True)
                time.sleep(3)
                clear_output()
                break
            elif self.lpoint == 2100:
                clear_output()
                print("오래 기다려주셔서 감사합니다. 😉👍\n곧 결과가 표시됩니다!!!")
                time.sleep(3)
                clear_output()
                break     
            elif (self.lpoint % 100 == 0) & (self.lpoint != 0):
                print('-------------------------------------------------------- {0}번째 과목 선정 프로세스 진행중-------------------------------------------------------- '.\
                      format(self.lpoint))
            self.lpoint += 1
        self.boss = self.boss.append(self.recommend_answer)
        self.boss.drop_duplicates(subset = ['과목명'], inplace = True)
        self.boss.reset_index(drop = True, inplace = True)
        # 결과 저장
        self.now_save = now.strftime('%m%d_%H%M')
        self.student_name = self.userdb.loc[len(self.userdb)-1, ['이름']].values[0]
        self.student_id = self.userdb.loc[len(self.userdb)-1, ['학번']].values[0]
        self.boss = self.boss.sort_values(by = ['소속'], ascending = True).reset_index(drop = True)
        display(self.boss)
        time.sleep(3)
        self.boss.to_csv(self.path_answer + str(self.student_name) + '(' + str(self.student_id) + ')_' + str(self.now_save) +'.csv', encoding = 'UTF-8-SIG', index = False)

    def run(self):
        self.make_coursing()
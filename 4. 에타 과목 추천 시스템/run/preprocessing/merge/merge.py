from tqdm import tqdm
import pandas as pd
import numpy as np
import time
import ast
import re
import os

import warnings
warnings.filterwarnings(action='ignore')

tqdm.pandas()

class Merge:
    def __init__(self, path = '.'):
        self.path = path
        self.path_evaluation = self.path + '/data/et_evaluation/'
        self.path_schedule = self.path + '/data/et_schedule/'
        self.path_et_competition = self.path + '/data/et_competition/'
        self.path_honeystudy = self.path + '/data/et_honeystudy/'
        self.path_capa = self.path + '/data/sg_capacity/'
        self.path_sg_competition = self.path + '/data/sg_competition/'
        self.path_save = self.path + '/result/source/'
        
    def make_merge(self):
#----------------------------------------------------------------------------------------------------------------------------------------------------------        
        def make_property(data, column, quan_num = 0.97, round_num = 1):
            point = data[column].quantile(quan_num).round(round_num)
            def change(x):
                if x >= point:
                    return column
                else:
                    return str(0)
            data[column + str('결과')] = data[column].apply(lambda x : change(x))
            return data.iloc[:, -1].to_frame()
        
        def remove_change(x):
            x = [i for i in x if i != '0']
            return x
        
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

        def withdraw_grade(x):
            return re.findall("\d", x)
        
        def ban(x):
            if len(str(x)) == 1:
                x = '0' + str(x)
                return x
            else:
                return str(x)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.et_competition = pd.read_csv(self.path_et_competition + 'competition_ratio.csv', encoding = 'UTF-8-SIG')
        self.et_professor = pd.read_csv(self.path_evaluation + 'professor_evaluation.csv', encoding = 'UTF-8-SIG')
        self.et_honeystudy = pd.read_csv(self.path_honeystudy + 'honeystudy.csv', encoding = 'UTF-8-SIG')
        #------------------------------------------------------------------------------------------------------------------------------------
        self.et_schedule_2019_1 = pd.read_csv(self.path_schedule + 'schedule_2019_1.csv', encoding = 'UTF-8-SIG')
        self.et_schedule_2019_2 = pd.read_csv(self.path_schedule + 'schedule_2019_2.csv', encoding = 'UTF-8-SIG')
        self.et_schedule_2020_1 = pd.read_csv(self.path_schedule + 'schedule_2020_1.csv', encoding = 'UTF-8-SIG')
        self.et_schedule_2020_2 = pd.read_csv(self.path_schedule + 'schedule_2020_2.csv', encoding = 'UTF-8-SIG')
        self.et_schedule_2021_1 = pd.read_csv(self.path_schedule + 'schedule_2021_1.csv', encoding = 'UTF-8-SIG')
        #------------------------------------------------------------------------------------------------------------------------------------
        self.sg_courses_2019_1 = pd.read_csv(self.path_capa + 'courses_2019_1.csv', encoding = 'UTF-8-SIG')
        self.sg_courses_2019_2 = pd.read_csv(self.path_capa + 'courses_2019_2.csv', encoding = 'UTF-8-SIG')
        self.sg_courses_2020_1 = pd.read_csv(self.path_capa + 'courses_2020_1.csv', encoding = 'UTF-8-SIG')
        self.sg_courses_2020_2 = pd.read_csv(self.path_capa + 'courses_2020_2.csv', encoding = 'UTF-8-SIG')
        self.sg_courses_2021_1 = pd.read_csv(self.path_capa + 'courses_2021_1.csv', encoding = 'UTF-8-SIG')
        #------------------------------------------------------------------------------------------------------------------------------------
        self.sg_competition_2019_1 = pd.read_csv(self.path_sg_competition + '2019_1.csv', encoding = 'UTF-8-SIG')
        self.sg_competition_2019_2 = pd.read_csv(self.path_sg_competition + '2019_2.csv', encoding = 'UTF-8-SIG')
        self.sg_competition_2020_1 = pd.read_csv(self.path_sg_competition + '2020_1.csv', encoding = 'UTF-8-SIG')
        self.sg_competition_2020_2 = pd.read_csv(self.path_sg_competition + '2020_2.csv', encoding = 'UTF-8-SIG')
        self.sg_competition_2021_1 = pd.read_csv(self.path_sg_competition + '2021_1.csv', encoding = 'UTF-8-SIG')
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.et_competition = self.et_competition.iloc[:, [2, 3, 4, 10]]
        self.et_competition.columns = ['과목코드', '과목명', '교수명', '경쟁점수']
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.ep = self.et_professor.copy()
        for column in list(self.et_professor.columns)[3:]:
            self.ep = pd.concat([self.ep, make_property(self.et_professor, column)], axis = 1)

        self.ep['교수특징'] = 0
        for i in range(len(self.ep)):
            self.ep['교수특징'][i] = [self.ep['꼰대결과'][i], self.ep['귀요미결과'][i], self.ep['카리스마결과'][i], self.ep['시크결과'][i], self.ep['열정러결과'][i], self.ep['엔젤결과'][i], self.ep['월급루팡결과'][i]]

        self.ep['교수특징'] = self.ep['교수특징'].apply(lambda x: remove_change(x))
        self.et_professor = self.ep = self.ep.iloc[:, [0, 21]]
        self.et_professor.reset_index(drop = True, inplace = True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.et_honeystudy = self.et_honeystudy.iloc[:, [0, 1, 12, 13]]
        self.et_honeystudy.drop_duplicates(inplace = True)
        self.et_honeystudy.reset_index(drop = True, inplace = True)
        self.et_honeystudy.columns = ['과목명', '교수명', '꿀점수', '배움점수']
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.et_schedule_2019_1 = self.et_schedule_2019_1.iloc[:, [0, 1, 2, 3, 4, 5]]
        self.et_schedule_2019_2 = self.et_schedule_2019_2.iloc[:, [0, 1, 2, 3, 4, 5]]
        self.et_schedule_2020_1 = self.et_schedule_2020_1.iloc[:, [0, 1, 2, 3, 4, 5]]
        self.et_schedule_2020_2 = self.et_schedule_2020_2.iloc[:, [0, 1, 2, 3, 4, 5]]
        self.et_schedule_2021_1 = self.et_schedule_2021_1.iloc[:, [0, 1, 2, 3, 4, 5]]
        self.et_schedule_2019_1.columns = ['과목코드', '과목명', '교수명', '학점', '수업시간/강의실', '권장학년']
        self.et_schedule_2019_2.columns = ['과목코드', '과목명', '교수명', '학점', '수업시간/강의실', '권장학년']
        self.et_schedule_2020_1.columns = ['과목코드', '과목명', '교수명', '학점', '수업시간/강의실', '권장학년']
        self.et_schedule_2020_2.columns = ['과목코드', '과목명', '교수명', '학점', '수업시간/강의실', '권장학년']
        self.et_schedule_2021_1.columns = ['과목코드', '과목명', '교수명', '학점', '수업시간/강의실', '권장학년']
        self.et_schedule_2019_1.dropna(subset = ['수업시간/강의실', '권장학년'], inplace = True)
        self.et_schedule_2019_1.reset_index(drop = True, inplace = True)
        self.et_schedule_2019_2.dropna(subset = ['수업시간/강의실', '권장학년'], inplace = True)
        self.et_schedule_2019_2.reset_index(drop = True, inplace = True)
        self.et_schedule_2020_1.dropna(subset = ['수업시간/강의실', '권장학년'], inplace = True)
        self.et_schedule_2020_1.reset_index(drop = True, inplace = True)
        self.et_schedule_2020_2.dropna(subset = ['수업시간/강의실', '권장학년'], inplace = True)
        self.et_schedule_2020_2.reset_index(drop = True, inplace = True)
        self.et_schedule_2021_1.dropna(subset = ['수업시간/강의실', '권장학년'], inplace = True)
        self.et_schedule_2021_1.reset_index(drop = True, inplace = True)
        
        def change_day(x):
            x = str(x)
            x = ''.join(x)
            x = re.sub(",", "", x)
            x = re.sub(" ", "", x)
            x = re.sub("'", "", x)
            return x
        
        self.et_schedule_2019_1['수업요일'] = self.et_schedule_2019_1['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.et_schedule_2019_1['수업요일'] = self.et_schedule_2019_1['수업요일'].progress_apply(lambda x : change_day(x))
        self.et_schedule_2019_1['수업시간'] = self.et_schedule_2019_1['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.et_schedule_2019_1['강의실'] = self.et_schedule_2019_1['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.et_schedule_2019_1['권장학년'] = self.et_schedule_2019_1['권장학년'].progress_apply(lambda x : withdraw_grade(x))

        self.et_schedule_2019_2['수업요일'] = self.et_schedule_2019_2['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.et_schedule_2019_2['수업요일'] = self.et_schedule_2019_2['수업요일'].progress_apply(lambda x : change_day(x))
        self.et_schedule_2019_2['수업시간'] = self.et_schedule_2019_2['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.et_schedule_2019_2['강의실'] = self.et_schedule_2019_2['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.et_schedule_2019_2['권장학년'] = self.et_schedule_2019_2['권장학년'].progress_apply(lambda x : withdraw_grade(x))

        self.et_schedule_2020_1['수업요일'] = self.et_schedule_2020_1['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.et_schedule_2020_1['수업요일'] = self.et_schedule_2020_1['수업요일'].progress_apply(lambda x : change_day(x))
        self.et_schedule_2020_1['수업시간'] = self.et_schedule_2020_1['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.et_schedule_2020_1['강의실'] = self.et_schedule_2020_1['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.et_schedule_2020_1['권장학년'] = self.et_schedule_2020_1['권장학년'].progress_apply(lambda x : withdraw_grade(x))

        self.et_schedule_2020_2['수업요일'] = self.et_schedule_2020_2['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.et_schedule_2020_2['수업요일'] = self.et_schedule_2020_2['수업요일'].progress_apply(lambda x : change_day(x))
        self.et_schedule_2020_2['수업시간'] = self.et_schedule_2020_2['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.et_schedule_2020_2['강의실'] = self.et_schedule_2020_2['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.et_schedule_2020_2['권장학년'] = self.et_schedule_2020_2['권장학년'].progress_apply(lambda x : withdraw_grade(x))

        self.et_schedule_2021_1['수업요일'] = self.et_schedule_2021_1['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.et_schedule_2021_1['수업요일'] = self.et_schedule_2021_1['수업요일'].progress_apply(lambda x : change_day(x))
        self.et_schedule_2021_1['수업시간'] = self.et_schedule_2021_1['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.et_schedule_2021_1['강의실'] = self.et_schedule_2021_1['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.et_schedule_2021_1['권장학년'] = self.et_schedule_2021_1['권장학년'].progress_apply(lambda x : withdraw_grade(x))
        
        self.et_schedule_2019_1 = self.et_schedule_2019_1.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8]]
        self.et_schedule_2019_2 = self.et_schedule_2019_2.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8]]
        self.et_schedule_2020_1 = self.et_schedule_2020_1.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8]]
        self.et_schedule_2020_2 = self.et_schedule_2020_2.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8]]
        self.et_schedule_2021_1 = self.et_schedule_2021_1.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8]]
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.sg_courses_2019_1 = self.sg_courses_2019_1.iloc[:, [3, 6, 8, 10]]
        self.sg_courses_2019_1.dropna(subset = ['교수진'], inplace = True)
        self.sg_courses_2019_1.dropna(subset = ['수업시간/강의실'], inplace = True)
        self.sg_courses_2019_1['수업요일'] = self.sg_courses_2019_1['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.sg_courses_2019_1['수업요일'] = self.sg_courses_2019_1['수업요일'].progress_apply(lambda x : change_day(x))
        self.sg_courses_2019_1['수업시간'] = self.sg_courses_2019_1['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.sg_courses_2019_1['강의실'] = self.sg_courses_2019_1['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.sg_courses_2019_1.reset_index(drop = True, inplace = True)
        self.sg_courses_2019_1 = self.sg_courses_2019_1.iloc[:, [0, 1, 3, 4, 5, 6]]
        self.sg_courses_2019_1.columns = ['소속', '과목명', '교수명', '수업요일', '수업시간', '강의실']

        self.sg_courses_2019_2 = self.sg_courses_2019_2.iloc[:, [3, 6, 8, 10]]
        self.sg_courses_2019_2.dropna(subset = ['교수진'], inplace = True)
        self.sg_courses_2019_2.dropna(subset = ['수업시간/강의실'], inplace = True)
        self.sg_courses_2019_2['수업요일'] = self.sg_courses_2019_2['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.sg_courses_2019_2['수업요일'] = self.sg_courses_2019_2['수업요일'].progress_apply(lambda x : change_day(x))
        self.sg_courses_2019_2['수업시간'] = self.sg_courses_2019_2['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.sg_courses_2019_2['강의실'] = self.sg_courses_2019_2['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.sg_courses_2019_2.reset_index(drop = True, inplace = True)
        self.sg_courses_2019_2 = self.sg_courses_2019_2.iloc[:, [0, 1, 3, 4, 5, 6]]
        self.sg_courses_2019_2.columns = ['소속', '과목명', '교수명', '수업요일', '수업시간', '강의실']

        self.sg_courses_2020_1 = self.sg_courses_2020_1.iloc[:, [3, 6, 8, 10]]
        self.sg_courses_2020_1.dropna(subset = ['교수진'], inplace = True)
        self.sg_courses_2020_1.dropna(subset = ['수업시간/강의실'], inplace = True)
        self.sg_courses_2020_1['수업요일'] = self.sg_courses_2020_1['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.sg_courses_2020_1['수업요일'] = self.sg_courses_2020_1['수업요일'].progress_apply(lambda x : change_day(x))
        self.sg_courses_2020_1['수업시간'] = self.sg_courses_2020_1['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.sg_courses_2020_1['강의실'] = self.sg_courses_2020_1['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.sg_courses_2020_1.reset_index(drop = True, inplace = True)
        self.sg_courses_2020_1 = self.sg_courses_2020_1.iloc[:, [0, 1, 3, 4, 5, 6]]
        self.sg_courses_2020_1.columns  = ['소속', '과목명', '교수명', '수업요일', '수업시간', '강의실']

        self.sg_courses_2020_2 = self.sg_courses_2020_2.iloc[:, [3, 6, 8, 10]]
        self.sg_courses_2020_2.dropna(subset = ['교수진'], inplace = True)
        self.sg_courses_2020_2.dropna(subset = ['수업시간/강의실'], inplace = True)
        self.sg_courses_2020_2['수업요일'] = self.sg_courses_2020_2['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.sg_courses_2020_2['수업요일'] = self.sg_courses_2020_2['수업요일'].progress_apply(lambda x : change_day(x))
        self.sg_courses_2020_2['수업시간'] = self.sg_courses_2020_2['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.sg_courses_2020_2['강의실'] = self.sg_courses_2020_2['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.sg_courses_2020_2.reset_index(drop = True, inplace = True)
        self.sg_courses_2020_2 = self.sg_courses_2020_2.iloc[:, [0, 1, 3, 4, 5, 6]]
        self.sg_courses_2020_2.columns = ['소속', '과목명', '교수명', '수업요일', '수업시간', '강의실']

        self.sg_courses_2021_1 = self.sg_courses_2021_1.iloc[:, [3, 6, 8, 10]]
        self.sg_courses_2021_1.dropna(subset = ['교수진'], inplace = True)
        self.sg_courses_2021_1.dropna(subset = ['수업시간/강의실'], inplace = True)
        self.sg_courses_2021_1['수업요일'] = self.sg_courses_2021_1['수업시간/강의실'].progress_apply(lambda x : withdraw_day(x))
        self.sg_courses_2021_1['수업요일'] = self.sg_courses_2021_1['수업요일'].progress_apply(lambda x : change_day(x))
        self.sg_courses_2021_1['수업시간'] = self.sg_courses_2021_1['수업시간/강의실'].progress_apply(lambda x : withdraw_time(x))
        self.sg_courses_2021_1['강의실'] = self.sg_courses_2021_1['수업시간/강의실'].progress_apply(lambda x : withdraw_class(x))
        self.sg_courses_2021_1.reset_index(drop = True, inplace = True)
        self.sg_courses_2021_1 = self.sg_courses_2021_1.iloc[:, [0, 1, 3, 4, 5, 6]]
        self.sg_courses_2021_1.columns = ['소속', '과목명', '교수명', '수업요일', '수업시간', '강의실']

#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.et_schedule_total = pd.concat([self.et_schedule_2019_1, self.et_schedule_2019_2, self.et_schedule_2020_1, self.et_schedule_2020_2, self.et_schedule_2021_1], axis = 0).reset_index(drop = True)
        self.et_schedule_total.drop_duplicates(subset = ['과목명', '과목코드', '교수명', '수업요일', '수업시간'], inplace = True)
        self.et_schedule_total.reset_index(drop = True, inplace = True)

        self.sg_courses_total = pd.concat([self.sg_courses_2019_1, self.sg_courses_2019_2, self.sg_courses_2020_1, self.sg_courses_2020_2, self.sg_courses_2021_1], axis = 0).reset_index(drop = True)
        self.sg_courses_total.drop_duplicates(subset = ['과목명', '교수명', '소속', '수업요일', '수업시간'], inplace = True)
        self.sg_courses_total.reset_index(drop = True, inplace = True)
#---------------------------------------------------------------------------------------------------------------------------------------------------------- 여기서 사라짐
        self.final_result = pd.merge(self.et_schedule_total, self.sg_courses_total, how = 'left', on = ['과목명', '교수명', '수업요일', '수업시간'])
        self.final_result = self.final_result.iloc[:, [8, 0, 1, 2, 3, 5, 6, 7, 4]]

        self.final_result = pd.merge(self.final_result, self.et_professor, how = 'left', on =['교수명'])
        self.final_result = pd.merge(self.final_result, self.et_competition, how = 'left', on = ['과목명', '교수명', '과목코드'])
        self.final_result = pd.merge(self.final_result, self.et_honeystudy, how = 'left', on = ['과목명', '교수명'])

        self.com_score = self.final_result.groupby(['과목명', '교수명'])['경쟁점수'].mean().to_frame().reset_index()
        self.final_result.drop('경쟁점수', axis = 1, inplace = True)

        self.final_result = pd.merge(self.final_result, self.com_score, how = 'left', on = ['과목명', '교수명'])
        self.final_result.reset_index(drop = True, inplace = True)
        self.final_result = self.final_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 10, 11]]
#---------------------------------------------------------------------------------------------------------------------------------------------------------- 여기서 사라짐
        self.final_result.to_csv(self.path_save + 'mid_result.csv', encoding = 'UTF-8-SIG', index = False)
#----------------------------------------------------------------------------------------------------------------------------------------------------------

    def revise(self):
        def change_major(x):
            x = re.sub('전공', '', x)
            x = re.sub('연계', '', x)
            x = x.strip()
            return x

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
            x = re.sub('1T', 'IT', x)
            x = re.sub('A1', 'AI', x)
            x = re.sub('1nquiry', 'Inquiry', x)
            x = re.sub('1ntermediate', 'Intermediate', x)
            x = re.sub('1oT', 'IoT', x)
            x = re.sub('U1/UX', 'UI/UX', x)
            x = re.sub('VLS1', 'VLSI', x)
            x = re.sub('·', '', x)
            return x

        def change_prof(x):
            p1 = re.sub(' ', '', x)
            p2 = re.sub(',', '', p1)
            if (p2.isalpha() == False) and (',' in x):
                length = len(x.split(','))
                x = str(x.split(',')[0]) + ' 외 ' + str(length-1) + '명'
                return x
            elif p2.isalpha() == True:
                if x == 'Bailey, Andrew':
                    return 'Andrew'
                elif x == 'Barnard,Stephen John':
                    return 'Barnard'
                elif x == 'Barrie Michael Jonathan Mathew':
                    return 'Mathew'
                elif x == 'BonfiglioRichardPaul':
                    return 'Paul'
                elif x == 'Brose Iris':
                    return 'Brose Iris'
                elif x == 'Castagnes, Gilles Yves':
                    return 'Castagnes'
                elif x == 'De Fremery, Peter Wayne':
                    return 'Fremery'
                elif x == 'Disney, Daniel James Philip':
                    return 'Disney'
                elif x == 'Hantke, Steffen Horst':
                    return 'Hantke'
                elif x == 'He, Ya Wen':
                    return 'He, Ya Wen'
                elif x == 'Ho, Pak Tung':
                    return 'Ho, Pak Tung'
                elif x == 'Iris Haydar Doruk':
                    return 'Doruk'
                elif x == 'Jones, Ryan':
                    return 'Jones'
                elif x == 'Jungk, Erik-Joachim':
                    return 'Jungk'
                elif x == 'Kim, Halla':
                    return 'Kim, Halla'
                elif x == 'Kim, Jae Pil':
                    return '김재필'
                elif x == 'Lee, Hosuk Sean':
                    return '이호석'
                elif x == 'Lee, Hosuk Sean, 김도성':
                    return '이호석 외 1명'
                elif x == 'Malin, Franck':
                    return 'Malin'
                elif x == 'PlotchPhilip Mark':
                    return 'Mark'
                elif x == 'Riley, John Patrick':
                    return 'Riley'
                elif x == 'Scopel Stefano':
                    return 'Stefano'
                elif x == 'Swain, Nigel':
                    return 'Nigel'
                elif x == 'Thigpen, Byron Douglas':
                    return 'Byron'
                elif x == 'Unger, Michael Anthony':
                    return 'Anthony'
                elif x == 'Willers, Arthur Gregory':
                    return 'Gregory'
                elif x == 'YANG, JUAN':
                    return 'YANG, JUAN'
                elif x == 'Yoo Isaiah WonHo':
                    return '유원호'
                else:
                    try:
                        length = len(x.split(','))
                        check2 = x.split(',')[1]
                        x = str(x.split(',')[0]) + ' 외 ' + str(length-1) + '명'
                        return x
                    except:
                        return x
            return x

        def change_day(x):
            x = x.lstrip('[')
            x = x.rstrip(']')
            x = x.strip()
            return x

        def change_recom(x):
            x = sorted(ast.literal_eval(x))
            x = ''.join(x)
            return x

        def change_proper(x):
            try:
                x = re.sub('귀요미', '꿀귀', x)
                x = re.sub('시크', '도도', x)
                x = re.sub('엔젤', '천사', x)
                x = re.sub('열정러', '', x)
                x = re.sub('월급루팡', '악마', x)
                x = re.sub('카리스마', '', x)
                x = sorted(ast.literal_eval(x))
                x = ''.join(x)
                if (x == ''):
                    x = '없음'
                    return x
            except:
                x = '없음'
                return x
            return x

        def change_comp(x):
            if np.isnan(x) == True:
                return '알수없음'
            else:
                return x

        def change_round(x):
            if np.isnan(x) == True:
                return x
            else:
                return np.round(x, 3)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.revise = pd.read_csv(self.path_save + 'mid_result.csv', encoding = 'UTF-8-SIG')
        self.revise.dropna(subset = ['소속', '교수명'], inplace = True)
        self.revise.reset_index(drop = True, inplace = True)
        self.hst = self.revise['꿀점수'].min()
        self.sst = self.revise['배움점수'].min()
        
        self.revise['소속'] = self.revise['소속'].apply(lambda x : change_major(x))
        self.revise['과목명'] = self.revise['과목명'].apply(lambda x : change_name(x))
        self.revise['교수명'] = self.revise['교수명'].apply(lambda x : change_prof(x))
        self.revise['수업요일'] = self.revise['수업요일'].apply(lambda x : change_day(x))
        self.revise['권장학년'] = self.revise['권장학년'].apply(lambda x : change_recom(x))
        self.revise['교수특징'] = self.revise['교수특징'].apply(lambda x : change_proper(x))

        for name in list(self.revise.columns)[10:]:
            self.revise[name] = self.revise[name].apply(lambda x : change_round(x))

        self.revise['경쟁점수'] = self.revise['경쟁점수'].apply(lambda x : change_comp(x))
        self.revise.drop_duplicates(subset = ['과목명', '교수명', '과목코드', '수업시간', '수업요일'], inplace = True)
        self.revise['꿀점수'] = self.revise['꿀점수'].fillna(self.hst)
        self.revise['배움점수'] = self.revise['배움점수'].fillna(self.sst)
        self.revise.reset_index(drop = True, inplace = True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.major_lst = sorted(list(self.revise['소속'].unique()))

        self.revise['꿀점수'] = self.revise['꿀점수'].astype(float)
        self.revise['배움점수'] = self.revise['배움점수'].astype(float)

        for major in self.major_lst:
            self.hnd = self.revise.groupby(['소속','과목명','교수명'])['꿀점수'].mean().to_frame().reset_index()
            # 전공별 상위10% 꿀점수 추출
            self.ten1 = self.hnd[self.hnd['소속'] == major]
            self.ten1 = self.ten1['꿀점수'].quantile(0.9)
            # 해당 전공 index 추출
            self.idx = self.revise[self.revise['소속'] == major].index
            self.revise.loc[self.idx, '꿀점수'] = self.revise.loc[self.idx, '꿀점수'].apply(lambda x : 1 if x >= self.ten1 else 0)

        for major in self.major_lst:
            self.stud = self.revise.groupby(['소속','과목명','교수명'])['배움점수'].mean().to_frame().reset_index()
            # 전공별 상위10% 배움점수 추출
            self.ten2 = self.stud[self.stud['소속'] == major]
            self.ten2 = self.ten2['배움점수'].quantile(0.9)
            # 해당 전공 index 추출
            self.idx = self.revise[self.revise['소속'] == major].index
            self.revise.loc[self.idx, '배움점수'] = self.revise.loc[self.idx, '배움점수'].apply(lambda x : 1 if x >= self.ten2 else 0)        
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.revise.columns = ['소속', '과목코드', '과목명', '교수명', '학점', '수업요일', '수업시간', '강의실', '권장학년', '교수특징', '경쟁점수', '꿀점수', '배움점수']
        self.revise.reset_index(drop = True, inplace = True)
        self.revise.to_csv(self.path_save + 'final_result.csv', encoding = 'UTF-8-SIG', index = False)
    
    def run(self):
        self.make_merge()
        self.revise()
import os
import re
import time
import textwrap
import numpy as np
import pandas as pd
import datetime as dt

import ipywidgets as widgets
from ipywidgets import interact
from ipywidgets import TwoByTwoLayout, AppLayout, Layout, ButtonStyle

from IPython.display import display
from IPython.display import clear_output
from IPython.display import Image as disImage
from PIL import Image, ImageFont, ImageDraw

import warnings
warnings.filterwarnings('ignore')

from .preprocessing.competition import Competition
from .preprocessing.course import Course
from .crawling.schedule import Schedule
from .crawling.evaluation import Evaluation
from .preprocessing.honeystudy import HoneyStudy
from .preprocessing.proeval import ProEval
from .preprocessing.ratio import Ratio
from .preprocessing.merge import Merge
from .coursing import Coursing
from .deleting import Deleting
#---------------------------------------------------------------------------------------------------------------------------------------------------------

class Everytime:
    def __init__(self):
        ''' 기본 실행 부분(1) '''
        if str(os.getcwd())[-9:] != 'Everytime':
            new_path = os.getcwd().split('run')[0].replace('\\', '/')[:-1]
            os.chdir(new_path)
            self.path = new_path
        else:
            self.path = '.'
        
        start_img1 = Image.open(self.path + "/data/interface/image/start/event1.png")
        start_img2 = Image.open(self.path + "/data/interface/image/start/event2.png")
        start_img3 = Image.open(self.path + "/data/interface/image/start/event3.png")
        start_img4 = Image.open(self.path + "/data/interface/image/start/event4.png")
        start_img5 = Image.open(self.path + "/data/interface/image/start/event5.png")
        start_img6 = Image.open(self.path + "/data/interface/image/start/event6.png")
        start_img7 = Image.open(self.path + "/data/interface/image/start/event7.png")
        start_img8 = Image.open(self.path + "/data/interface/image/start/event8.png")
        start_img9 = Image.open(self.path + "/data/interface/image/start/event9.png")
        start_img10 = Image.open(self.path + "/data/interface/image/start/event10.png")
        start_img11 = Image.open(self.path + "/data/interface/image/start/event11.png")
        start_img12 = Image.open(self.path + "/data/interface/image/start/event12.png")
        start_img13 = Image.open(self.path + "/data/interface/image/start/event13.png")
        start_img14 = Image.open(self.path + "/data/interface/image/start/event14.png")
        start_img15 = Image.open(self.path + "/data/interface/image/start/event15.png")
        start_img16 = Image.open(self.path + "/data/interface/image/start/event16.png")
        start_img17 = Image.open(self.path + "/data/interface/image/start/event17.png")
        start_img18 = Image.open(self.path + "/data/interface/image/start/event18.png")
        display(start_img1)
        time.sleep(0.3)
        clear_output()
        display(start_img2)
        time.sleep(0.3)
        clear_output()
        display(start_img3)
        time.sleep(0.3)
        clear_output()
        display(start_img4)
        time.sleep(0.3)
        clear_output()
        display(start_img5)
        time.sleep(0.3)
        clear_output()
        display(start_img6)
        time.sleep(0.3)
        clear_output()
        display(start_img7)
        time.sleep(0.3)
        clear_output()
        display(start_img8)
        time.sleep(0.3)
        clear_output()
        display(start_img9)
        time.sleep(0.3)
        clear_output()
        display(start_img10)
        time.sleep(0.3)
        clear_output()
        display(start_img11)
        time.sleep(0.3)
        clear_output()
        display(start_img12)
        time.sleep(0.3)
        clear_output()
        display(start_img13)
        time.sleep(0.3)
        clear_output()
        display(start_img14)
        time.sleep(0.3)
        clear_output()
        display(start_img15)
        time.sleep(0.3)
        clear_output()
        display(start_img16)
        time.sleep(0.3)
        clear_output()
        display(start_img17)
        time.sleep(0.3)
        clear_output()
        
        self.path_data = self.path + '/data/'
        self.path_run = self.path + '/run/'

        self.path_et_competition = self.path + '/data/et_competition/'
        self.path_et_evaluation = self.path + '/data/et_evaluation/'
        self.path_et_schedule = self.path + '/data/et_schedule/'
        self.path_et_honey_dict = self.path + '/data/et_dict/'
        self.path_et_study_dict = self.path + '/data/et_dict/'
        self.path_sg_competition = self.path + '/data/sg_competiton/'
        self.path_sg_course_lst = self.path + '/data/sg_course_lst/'
        self.path_image_bond = self.path + '/data/interface/image/bond/'
        self.path_image_course = self.path + '/data/interface/image/course/'
        self.path_font = self.path + '/data/interface/font/'

        self.path_user = self.path + '/userDB/'
        if not os.path.isdir(self.path_user):
            os.makedirs(self.path_user)
        try:
            self.total_info = pd.read_csv(self.path_user + "userDB.csv", encoding="UTF-8-SIG")
        except FileNotFoundError:
            self.make_to_db = Image.open(self.path + "/data/interface/image/start/make_to_db.png")
            display(self.make_to_db)
            time.sleep(2.3)
            clear_output()
            userdb = pd.DataFrame(columns=("학번", "이름", "본전공", "복수전공", "학기수", "전공과목수", "교양과목수",
                                                                           "필수과목1", "필수과목2", "필수과목3",
                                                                           "시간표테마", "공강", "시간표유형1", "시간표유형2", "꿀강의", "배움강의")) # "피드백과목", "최종시간표"
            userdb.drop_duplicates(inplace = True)
            userdb.reset_index(drop = True, inplace = True)
            userdb.to_csv(self.path_user + "userDB.csv", encoding = "UTF-8-SIG", index = False)
            self.total_info = pd.read_csv(self.path_user + "userDB.csv", encoding="UTF-8-SIG")
        
        display(start_img18)
        time.sleep(2)
        clear_output()
        
        self.warnings = Image.open(self.path + "/data/interface/image/start/warnings.png")
        display(self.warnings)
        time.sleep(5)
        clear_output()
        
        self.start = widgets.Button(description = "😝 에브리타임 과목 추천 시작", layout = Layout(width = 'auto', height = '100%'), style = ButtonStyle(button_color = '#FF848F'))
        self.crawl_setting = widgets.Button(description = "👩‍💻 기본 데이터 크롤링 시작", layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#FFBEBE'))
        self.preprocessing_bt = widgets.Button(description ="🛠 기본 데이터 전처리 시작", layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#FFBEBE'))
        self.save = widgets.Button(description = "🗂 결과 저장", layout = Layout(width = 'auto', height = 'auto'))
        self.hnst = widgets.Button(description = "🍯📗 전공별 꿀/배움 과목 추천", layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#FFD228'))
        self.to_over = widgets.Button(description = "✂ 종료", layout = Layout(width = 'auto', height = 'auto'), button_style = 'danger')
        self.copyright = widgets.Button(description = "ⓒ 2021 - 2022 INSIGHT 3 X 4 X 5 기", layout = Layout(width = '99.6%', height = 'auto'), style = ButtonStyle(button_color = '#dcdcdc'))
#---------------------------------------------------------------------------------------------------------------------------------------------------------
    ''' 기본 실행 부분(2) '''
    def run(self): # 인터페이스 및 프로그램 실행
        self.ttl = AppLayout(header = self.start, left_sidebar = self.crawl_setting, center = self.preprocessing_bt, right_sidebar = self.hnst, footer = self.to_over, pane_heights = [1, 1, 1], pane_widths = [1, 1, 1])
        display(self.ttl)
        display(self.copyright)
        self.start.on_click(self.main_event1)
        self.crawl_setting.on_click(self.data_setting)
        self.preprocessing_bt.on_click(self.data_preprocessing)
        self.hnst.on_click(self.plus_recommend)
        self.to_over.on_click(self.clear_all)
#---------------------------------------------------------------------------------------------------------------------------------------------------------                
    def plus_recommend(self, change):
        clear_output()
        self.tbtl = TwoByTwoLayout(top_left = self.hh1, top_right = self.mm1, bottom_left = self.ss1, bottom_right = self.nn1)
        display(self.tbtl)
        self.hh1.on_click(self.plus_honey)
        self.ss1.on_click(self.plus_study)
        self.mm1.on_click(self.plus_major)
        self.nn1.on_click(self.show_first)
        
    def plus_honey(self, change):
        clear_output()
        self.plush = pd.read_csv(self.path + '/result/source/final_result.csv', encoding = 'UTF-8-SIG')
        self.plus_tmp = pd.read_csv(self.path + '/result/source/tmp_result.csv', encoding = 'UTF-8-SIG')
        
        self.plush = self.plush.append(self.plus_tmp)
        self.plush = self.plush.drop_duplicates(subset = ['과목명', '교수명', '소속', '과목코드'])
        self.plush.reset_index(drop = True, inplace = True)
        
        display(self.plus_4)
        display(self.next_button1)
        self.next_button1.on_click(self.plus_next1)
      
    def plus_study(self, change):
        clear_output()
        self.plush = pd.read_csv(self.path + '/result/source/final_result.csv', encoding = 'UTF-8-SIG')
        self.plus_tmp = pd.read_csv(self.path + '/result/source/tmp_result.csv', encoding = 'UTF-8-SIG')
        
        self.plush = self.plush.append(self.plus_tmp)
        self.plush = self.plush.drop_duplicates(subset = ['과목명', '교수명', '소속', '과목코드'])
        self.plush.reset_index(drop = True, inplace = True)
        
        display(self.plus_5)
        display(self.next_button2)
        self.next_button2.on_click(self.plus_next2)
        
    def plus_next1(self, change):
        clear_output()
        pd.options.display.max_rows = 100
        self.honey_frame = self.plush[(self.plush['소속'] == Everytime.plus_4.value) & (self.plush['꿀점수'] == np.float(1.000))].iloc[:, [0, 2, 3]]
        self.honey_frame.drop_duplicates(inplace = True)
        self.honey_frame.reset_index(drop = True, inplace = True)
        display(self.honey_frame)
        display(self.back6)
        self.back6.on_click(self.show_first)
        pd.options.display.max_rows = 20
        
    def plus_next2(self, change):
        clear_output()
        pd.options.display.max_rows = 100
        self.study_frame = self.plush[(self.plush['소속'] == Everytime.plus_5.value) & (self.plush['배움점수'] == np.float(1.000))].iloc[:, [0, 2, 3]]
        self.study_frame.drop_duplicates(inplace = True)
        self.study_frame.reset_index(drop = True, inplace = True)
        display(self.study_frame)
        display(self.back7)
        self.back7.on_click(self.show_first)
        pd.options.display.max_rows = 20
    
    def plus_major(self, change):
        clear_output()
        self.plush = pd.read_csv(self.path + '/result/source/final_result.csv', encoding = 'UTF-8-SIG')
        self.plus_tmp = pd.read_csv(self.path + '/result/source/tmp_result.csv', encoding = 'UTF-8-SIG')
        self.plush = self.plush.append(self.plus_tmp)
        self.plush = self.plush.drop_duplicates(subset = ['과목명', '교수명', '소속', '과목코드'])
        self.plush.reset_index(drop = True, inplace = True)
        print("전공 과목 리스트는 다음과 같습니다.\n")
        print(sorted(list(self.plush['소속'].unique())))
        display(self.back5)
        self.back5.on_click(self.show_back)
#---------------------------------------------------------------------------------------------------------------------------------------------------------        
    ''' 종료 버튼 정의 부분 '''
    def clear_all(self, change): # 클릭시 인터페이스 종료
        print("에브리타임 과목 추천 시스템을 종료하겠습니다.")
        time.sleep(1.75)
        clear_output()
        
    def show_first(self, change): # 클릭시 인터페이스 처음으로 이동
        clear_output()
        self.run()
            
    def show_back(self, change):
        clear_output()
        self.run()
#---------------------------------------------------------------------------------------------------------------------------------------------------------    
    ''' 사용자 정보 수집 부분 '''
    def main_event1(self, change): # 사용자 기본 정보
        clear_output()
        self.how_to_use = Image.open(self.path + "/data/interface/image/start/how_to_use.png")
        display(self.how_to_use)
        time.sleep(5)
        clear_output()
        self.delete_information()
        clear_output()
        for bot in self.user_buttons1:
            display(bot)
        display(self.back0)
        display(self.event2)
        self.back0.on_click(self.reback)
        self.event2.on_click(self.main_event2)
        
    def main_event2(self, change): # 공강, 시간표 유형
        clear_output()
        for bot in self.user_buttons2:
            display(bot)
        display(self.back1)
        display(self.event3)
        self.back1.on_click(self.main_event1)
        self.event3.on_click(self.main_event3)
        
    def main_event3(self, change): # 강의 유형 (꿀)
        clear_output()
        for bot in self.user_buttons3:
            display(bot)
        display(self.back2)
        display(self.event4)
        self.back2.on_click(self.main_event2)
        self.event4.on_click(self.main_event4)
        
    def main_event4(self, change):
        clear_output()
        for bot in self.user_buttons4:
            display(bot)
        display(self.back3)
        display(self.event5)
        self.back3.on_click(self.main_event3)
        self.event5.on_click(self.main_event5)
        
    def main_event5(self, change):
        clear_output()
        self.user_info = [Everytime.student_id.value, Everytime.student_name.value, Everytime.main_major.value, Everytime.sub_major.value, Everytime.session.value,
                                      Everytime.main_many.value, Everytime.sub_many.value, 
                                      Everytime.essential_course1.value, Everytime.essential_course2.value, Everytime.essential_course3.value,
                                      Everytime.schedule_thema.value, Everytime.gap_class_day.value,
                                      Everytime.schedule_type1.value, Everytime.schedule_type2.value,
                                      Everytime.course_type1.value, Everytime.course_type2.value]
        
        self.tbtl = AppLayout(header = None, left_sidebar = self.save1, center = self.recom1, right_sidebar = self.callback, footer = None, pane_widths = [1, 1, 1])
        display(self.tbtl)
        self.save1.on_click(self.save_information)
        self.recom1.on_click(self.start_recommend)
        self.callback.on_click(self.reback2)
        
    def save_information(self, change):
        if int(self.user_info[4]) < 9:
            self.user_dict = {'학번' : self.user_info[0], '이름' : self.user_info[1], '본전공' : self.user_info[2], '복수전공' : self.user_info[3], '학기수' : self.user_info[4],
                                          '전공과목수' : self.user_info[5], '교양과목수' : self.user_info[6], 
                                          '필수과목1' : self.user_info[7], '필수과목2' : self.user_info[8], '필수과목3' : self.user_info[9],
                                          '시간표테마' : self.user_info[10], '공강' : self.user_info[11], '시간표유형1' : self.user_info[12], '시간표유형2' : self.user_info[13],
                                          '꿀강의' : self.user_info[14], '배움강의' : self.user_info[15]}
            self.total_info = self.total_info.append(self.user_dict, ignore_index = True)
            self.total_info.reset_index(inplace = True, drop = True)
            self.total_info.drop_duplicates(inplace = True)
            self.total_info.to_csv(self.path_user + 'userDB.csv', encoding = 'UTF-8-SIG', index = False)
            print('저장되었습니다')
        else:
            print('막학기생은 추천 시스템을 활용하지 않아도 괜찮습니다.')
            time.sleep(5)
            clear_output()
            print("언제까지 기다리실건가요? 쥬피터 노트북을 다시 실행시켜주세요. ㅎ__ㅎ")
            
    def delete_information(self):
        clear_output()
        deleting = Deleting()
        deleting.run()
        time.sleep(0.5)
        clear_output()
#---------------------------------------------------------------------------------------------------------------------------------------------------------
    def visualization(self):
        self.path = '.'
        self.answer_path = self.path + '/result/answer/'
        self.class_path = self.path + '/data/interface/image/course/'
        self.font_path = self.path + '/data/interface/font/'
        self.bond_path = self.path + '/data/interface/image/bond/'
        self.image_path = self.path + '/result/imageDB/'
        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        def get_filename(user, num):
            for i in sorted(os.listdir(self.answer_path), reverse = True):
                if user + '(' + str(num) + ')' in i:
                    return i
        def make_df(filename):
            df = pd.read_csv(self.answer_path + filename, encoding = 'UTF-8-SIG')
            df['수업길이'] = ''
            for i in range(len(df)):
                tmp = df['수업시간'][i].split('~')
                tmp = [tmp[x].split(':') for x in range(2)]        
                period = str(dt.datetime(2021, 3, 27, int(tmp[1][0]), int(tmp[1][1])) - dt.datetime(2021, 3, 27, int(tmp[0][0]), int(tmp[0][1]))).split(':')[:2]
                period[0] = '0' + period[0]
                period = ''.join(period)
                df['수업길이'][i] = period
                if df.isnull().sum().sum() != 0:
                    print("에러가 발생했습니다. ipynb파일을 재실행해주세요!!!")
                    time.sleep(120)
            return df
        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        def make_course(i):
            # 과목판 불러오기 및 기타 설정
            image = Image.open(self.class_path + self.answer['수업길이'][i] + '.jpg')

            back_im = image.copy()
            draw = ImageDraw.Draw(back_im)
            font_rt = ImageFont.truetype(font = self.font_path + 'NanumSquareB.ttf', size = 17)
            image_width, image_height = image.size

            # 과목판 색 수정
            draw.rectangle([(2.7, 2.7), (image_width-2.7, image_height-2.7)], fill=(np.random.randint(200,255), np.random.randint(200,255), np.random.randint(200,255)))

            # 과목 정보 넣기
            prof = self.answer['교수특징'][i] 
            prof_list = [prof[i:i+2] for i in range(0, len(prof), 2)]
            ratio = self.answer['경쟁점수'][i]
            honey = self.answer['꿀점수'][i]

            # 정보1 : 교수 특징 & 경쟁 점수
            prof_dict = {'꿀귀' : 'prof_cute.png', '천사' : 'prof_angel.png', '악마' : 'prof_devil.png', '도도' : 'prof_dodo.png', '꼰대' : 'prof_ggon.png'}
            if prof_list[0] == '없음':
                if ratio == '알수없음':
                    pass
                else:
                    ratio = round(float(ratio), 1)
                    ratio_im = Image.open(self.class_path + 'ratio.png').resize((60, 35))
                    ratio_mask = Image.open(self.class_path + 'ratio.png').resize(ratio_im.size)
                    back_im.paste(ratio_im, (image_width - 310, image_height - 43), ratio_mask)
                    draw.text((image_width - 304, image_height - 37), str(ratio), font = font_rt, fill = 'black')

            elif len(prof_list) == 1:
                prof1 = Image.open(self.class_path + prof_dict[prof_list[0]]).resize((50, 35))
                mask1 = Image.open(self.class_path + prof_dict[prof_list[0]]).resize(prof1.size)
                back_im.paste(prof1, (image_width - 310, image_height - 43), mask1)
                if ratio == '알수없음':
                    pass
                else:
                    ratio = round(float(ratio), 1)
                    ratio_im = Image.open(self.class_path + 'ratio.png').resize((60, 35))
                    ratio_mask = Image.open(self.class_path + 'ratio.png').resize(ratio_im.size)
                    back_im.paste(ratio_im, (image_width - 255, image_height - 43), ratio_mask)
                    draw.text((image_width - 249, image_height - 37), str(ratio), font=font_rt, fill = 'black')

            elif len(prof_list) == 2:
                prof1 = Image.open(self.class_path + prof_dict[prof_list[0]]).resize((50, 35))
                prof2 = Image.open(self.class_path + prof_dict[prof_list[1]]).resize((50, 35))
                mask1 = Image.open(self.class_path + prof_dict[prof_list[0]]).resize(prof1.size)
                mask2 = Image.open(self.class_path + prof_dict[prof_list[1]]).resize(prof2.size)
                back_im.paste(prof1, (image_width - 310, image_height - 43), mask1) 
                back_im.paste(prof2, (image_width - 255, image_height - 43), mask2)
                if ratio == '알수없음':
                    pass
                else:
                    ratio = round(float(ratio), 1)
                    ratio_im = Image.open(self.class_path + 'ratio.png').resize((60, 35))
                    ratio_mask = Image.open(self.class_path + 'ratio.png').resize(ratio_im.size)
                    back_im.paste(ratio_im, (image_width - 200, image_height - 43), ratio_mask)
                    draw.text((image_width - 194, image_height - 37), str(ratio), font=font_rt, fill = 'black')

            elif len(prof_list) == 3:
                prof1 = Image.open(self.class_path + prof_dict[prof_list[0]]).resize((50, 35))
                prof2 = Image.open(self.class_path + prof_dict[prof_list[1]]).resize((50, 35))
                prof3 = Image.open(self.class_path + prof_dict[prof_list[2]]).resize((50, 35))
                mask1 = Image.open(self.class_path + prof_dict[prof_list[0]]).resize(prof1.size)
                mask2 = Image.open(self.class_path + prof_dict[prof_list[1]]).resize(prof2.size)
                mask3 = Image.open(self.class_path + prof_dict[prof_list[2]]).resize(prof3.size)
                back_im.paste(prof1, (image_width - 310, image_height - 43), mask1) 
                back_im.paste(prof2, (image_width - 255, image_height - 43), mask2)
                back_im.paste(prof3, (image_width - 200, image_height - 43), mask3)
                if ratio == '알수없음':
                    pass
                else:
                    ratio = round(float(ratio), 1)
                    ratio_im = Image.open(self.class_path + 'ratio.png').resize((60, 35))
                    ratio_mask = Image.open(self.class_path + 'ratio.png').resize(ratio_im.size)
                    back_im.paste(ratio_im, (image_width - 145, image_height - 43), ratio_mask)
                    draw.text((image_width - 139, image_height - 37), str(ratio), font=font_rt, fill = 'black')

            # 정보2 : 꿀 여부
            if honey == 0:
                pass
            else:
                honey_im = Image.open(self.class_path + 'honey.png').resize((45, 42))
                honey_mask = Image.open(self.class_path + 'honey.png').resize(honey_im.size)
                back_im.paste(honey_im, (image_width - 53, image_height - 53), honey_mask) 

            # 정보3 : 과목명, 교수명, 강의실 
            def isHangul(text):
                hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
                return hanCount > 0

            def draw_text(image, index):
                draw = ImageDraw.Draw(image)
                image_width, image_height = image.size
                start_height = 12

                txt_lec = self.answer['과목명'][index]
                if self.answer['강의실'][index] == '없음':
                    txt_pf = self.answer['교수명'][index]
                else:
                    txt_pf = self.answer['교수명'][index] + '  ' + self.answer['강의실'][index]

                font_lec = ImageFont.truetype(font = self.font_path + 'NanumSquareB.ttf', size =24)
                font_pf = ImageFont.truetype(font = self.font_path + 'NanumSquareB.ttf', size = 18)

                if isHangul(txt_lec):
                    lines = textwrap.wrap(txt_lec, width = 13)  #width 체크하기
                    if len(lines) >= 3:
                        lines = [lines[0], lines[1] + '...']
                else:
                    lines = textwrap.wrap(txt_lec, width = 20)
                    if len(lines) >= 3:
                        lines = [lines[0], lines[1] + '...']

                for line in lines:
                    line_width, line_height = font_lec.getsize(line)
                    draw.text((13, start_height), line, font = font_lec, fill = 'black')
                    start_height += line_height+1

                line_width, line_height = font_pf.getsize(txt_pf)
                draw.text((14, start_height+4), txt_pf, font = font_pf, fill = 'gray')
                return image

            course_im = draw_text(back_im, i)
            return course_im
        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        def display_course(bond, course_im):
            day = self.answer['수업요일'][i]
            time = self.answer['수업시간'][i].split('~')[0]
            if len(day) == 1:
                bond.paste(course_im, (self.bond_x[day], self.bond_y[time]))
            else:
                bond.paste(course_im, (self.bond_x[day[0]], self.bond_y[time]))
                bond.paste(course_im, (self.bond_x[day[1]], self.bond_y[time]))   
            return bond
        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # 사용자 정보
        self.user = Everytime.student_name.value
        self.num = Everytime.student_id.value
        self.answer = make_df(get_filename(self.user, self.num))

        # 시간표 만들기
        self.bond = Image.open(self.bond_path + 'bond.jpg')
        self.bond_x = {'월':177, '화':500, '수':823, '목':1146, '금':1468}
        self.bond_y = {'09:00' : 85, '10:00' : 197, '10:30' : 252, '12:00' : 419, '13:00' : 530, '13:30' : 585, '14:00' : 641, '14:30' : 697, '15:00' : 752, '15:30' : 808, 
                                  '15:40' : 826, '16:30' : 918, '16:40' : 937, '17:00' : 974, '17:30' : 1029, '18:00' : 1085, '18:30' : 1140, '19:30' : 1251}

        for i in range(0, len(self.answer)):
            self.bond = display_course(self.bond, make_course(i))

        # 시간표 저장 및 보여주기
        self.bond.save(self.image_path + get_filename(self.user, self.num)[:-4] + '.jpg')
        self.bond.show()
#---------------------------------------------------------------------------------------------------------------------------------------------------------        
    def start_recommend(self, change):
        clear_output()
        coursing = Coursing()
        coursing.run()
        time.sleep(1)
        
        clear_output()
        self.visualization()
        print("시간표 추천이 완료되었습니다.  60초 후 처음 화면으로 돌아갑니다. 😉 (만족스럽지 않으시다면, 반드시 들어야 하는 과목을 추가해보세요)")
        
        time.sleep(40)
        clear_output()
        self.run()
#---------------------------------------------------------------------------------------------------------------------------------------------------------        
    def data_setting(self, change):
        clear_output()
        display(self.sg1)
        self.sg1.on_click(self.sg_start)
        
    def sg_start(self, change):
        clear_output()
        print("데이터 수집을 위해 2016년 1학기부터 2021년 1학기까지의 서강대 강의 과목명을 전처리 중입니다... (약 2초~5초 소요)")
        self.course_start()
        print("데이터 수집을 위해 2016년 1학기부터 2021년 1학기까지의 서강대 강의 경쟁률을 전처리 중입니다... (약 2초~5초 소요)")
        self.competition_start()
        time.sleep(3)
        clear_output()
        display(self.et1)
        display(self.back4)
        self.et1.on_click(self.et_start)
        self.back4.on_click(self.reback)
        
    def et_start(self, change):
        clear_output()
        print("2016년 1학기부터 2021년 1학기까지의 에타 강의 목록 및 강의평을 크롤링 중입니다... (약 12시간~14시간 소요)")
        self.et_crawling_start()
        
    def reback(self, change):
        clear_output()
        time.sleep(0.5)
        self.run()
        
    def reback2(self, change):
        clear_output()
        time.sleep(0.5)
        self.run()
        
    def course_start(self):
        course = Course()
        course.run()
        
    def competition_start(self):
        competition = Competition()
        competition.run()
        
    def et_crawling_start(self):
        schedule = Schedule()
        evaluation = Evaluation()
        schedule.run()
        evaluation.run()
        print("데이터 수집이 모두 완료되었습니다.")
        time.sleep(3)
        clear_output()
        self.run()
#--------------------------------------------------------------------------------------------------------------------------------------------------------- 
    def data_preprocessing(self, change):
        clear_output()
        display(self.pre1)
        self.pre1.on_click(self.pre_start)
        
    def pre_start(self, change):
        clear_output()
        print("데이터 수집을 위해 2016년 1학기부터 2021년 1학기까지의 서강대 강의 과목명을 전처리 중입니다... (약 2초~5초 소요)")
        self.course_start()
        print("데이터 수집을 위해 2016년 1학기부터 2021년 1학기까지의 서강대 강의 경쟁률을 전처리 중입니다... (약 2초~5초 소요)")
        self.competition_start()
        time.sleep(2)
        clear_output()
        print("과목별 예상 경쟁률을 산정중입니다... (약 2초~3초 소요)")
        self.ratio_start()
        time.sleep(1.5)
        print("교수님 특징을 추출중입니다... (약 15분~20분 소요)")
        self.proeval_start()
        time.sleep(1.5)
        print("꿀/배움 과목을 선정중입니다... (약 21분~24분 소요)")
        self.honeystudy_start()
        
    def honeystudy_start(self):
        honeystudy = HoneyStudy()
        honeystudy.run()
        clear_output()
        print("최종 데이터를 병합중입니다.")
        self.merge_start()
        time.sleep(2)
        clear_output()
        print("데이터 전처리를 완료하였습니다.")
        time.sleep(2)
        clear_output()
        self.run()
        
    def proeval_start(self):
        proeval = ProEval()
        proeval.run()
        
    def ratio_start(self):
        ratios = Ratio()
        ratios.run()
        
    def merge_start(self):
        merg = Merge()
        merg.run()        
#---------------------------------------------------------------------------------------------------------------------------------------------------------
    ''' 메인 함수에 들어가는 변수에 값을 할당하는 부분 '''
    style = {'description_width' : 'initial'}
    opt = ['없음', '경영학', '경제학', '공공인재', '교육문화', '국어국문학', '국제인문학부', '글로벌한국학', '기계공학', '물리학', '미국문화', '미디어&엔터테인먼트', '바이오융합기술', '빅데이터사이언스', '사학', '사회학', '생명과학', '수학', '스타트업', '스포츠미디어', '신문방송학', '심리학', '아트&테크놀로지', '여성학', '영미어문', '유럽문화', '융합소프트웨어', '인공지능', '일본문화', '자연과학부', '전인교육원', '전자공학', '정치외교학', '정치학/경제학/철학', '종교학', '중국문화', '지식융합미디어학부', '철학', '커뮤니케이션학', '컴퓨터공학', '한국발전과국제개발협력', '한국사회문화', '화공생명공학', '화학']
    opt1 = ['경영학', '경제학', '공공인재', '교육문화', '국어국문학', '국제인문학부', '글로벌한국학', '기계공학', '물리학', '미국문화', '미디어&엔터테인먼트', '바이오융합기술', '빅데이터사이언스', '사학', '사회학', '생명과학', '수학', '스타트업', '스포츠미디어', '신문방송학', '심리학', '아트&테크놀로지', '여성학', '영미어문', '유럽문화', '융합소프트웨어', '인공지능', '일본문화', '자연과학부', '전인교육원', '전자공학', '정치외교학', '정치학/경제학/철학', '종교학', '중국문화', '지식융합미디어학부', '철학', '커뮤니케이션학', '컴퓨터공학', '한국발전과국제개발협력', '한국사회문화', '화공생명공학', '화학']
    opt2 = ['없음', '경영학', '경제학', '공공인재', '교육문화', '국어국문학', '국제인문학부', '글로벌한국학', '기계공학', '물리학', '미국문화', '미디어&엔터테인먼트', '바이오융합기술', '빅데이터사이언스', '사학', '사회학', '생명과학', '수학', '스타트업', '스포츠미디어', '신문방송학', '심리학', '아트&테크놀로지', '여성학', '영미어문', '유럽문화', '융합소프트웨어', '인공지능', '일본문화', '자연과학부', '전인교육원', '전자공학', '정치외교학', '정치학/경제학/철학', '종교학', '중국문화', '지식융합미디어학부', '철학', '커뮤니케이션학', '컴퓨터공학', '한국발전과국제개발협력', '한국사회문화', '화공생명공학', '화학']
    
    # main event 1 (user information)
    student_id = widgets.Text(value = None, placeholder = '20196789', description = '학번', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    student_name = widgets.Text(value = None, placeholder = '홍길동', description = '이름', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    main_major = widgets.Dropdown(options = opt1, value = None, description = '본전공', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    sub_major = widgets.Dropdown(options = opt2, value = None, description = '복수전공', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    session = widgets.Text(value = None, placeholder = '5', description = '이수 학기수(이번 학기 포함)', style = style, layout = Layout(width = 'auto', height = 'auto'))
    main_many = widgets.IntSlider(value = 3, min = 0, max = 9, step = 1, description = '이번 학기에 들을 전공 과목수', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    sub_many = widgets.IntSlider(value = 3, min = 0, max = 6, step = 1, description = '이번 학기에 들을 교양 과목수', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    essential_course1 = widgets.Text(value = None, placeholder = '응용경영통계', description = '반드시 들어야 하는 과목(1)', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    essential_course2 = widgets.Text(value = None, placeholder = '통계자료분석', description = '반드시 들어야 하는 과목(2)', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    essential_course3 = widgets.Text(value = None, placeholder = '없음', description = '반드시 들어야 하는 과목(3)', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    schedule_thema = widgets.Dropdown(description ="시간표 테마", options = ['봄', '여름', '가을', '겨울'], disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))

    # main event 2 (schedule type)
    gap_class_day = widgets.Text(value = None, placeholder = 'O요일(또는 없음)', description = '공강 요일', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    schedule_type1 = widgets.Dropdown(description ="시간표 유형(1)", options = ['얼리버드형', '늦잠형', '상관없음'], disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    schedule_type2 = widgets.Dropdown(description ="시간표 유형(2)", options = ['삼시세끼형', '노밥형', '상관없음'], disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    
    # main event 3 (course type)
    course_type1 = widgets.IntSlider(value = 0, min = 0, max = 2, step = 1, description = '꿀 강도 🍯', style = style)
    course_type2 = widgets.IntSlider(value = 0, min = 0, max = 2, step = 1, description = '배움 강도 📗', style = style)
    
    # total event
    user_buttons1 = [student_id, student_name, main_major, sub_major, session, main_many, sub_many,
                                    essential_course1, essential_course2, essential_course3, schedule_thema]
    user_buttons2 = [gap_class_day, schedule_type1, schedule_type2]
    user_buttons3 = [course_type1]
    user_buttons4 = [course_type2]
    
    # next button
    event2 = widgets.Button(description = "다음 페이지")
    event3 = widgets.Button(description = "다음 페이지")
    event4 = widgets.Button(description = "다음 페이지")
    event5 = widgets.Button(description = "다음 페이지")
    
    # back button
    back0 = widgets.Button(description = "이전 페이지")
    back1 = widgets.Button(description = "이전 페이지")
    back2 = widgets.Button(description = "이전 페이지")
    back3 = widgets.Button(description = "이전 페이지")
    back4 = widgets.Button(description = "이전 페이지")
    back5 = widgets.Button(description = "처음으로")
    back6 = widgets.Button(description = "처음으로")
    back7 = widgets.Button(description = "처음으로")
    
    # callback button
    callback = widgets.Button(description = "처음으로", button_style = 'danger', layout = Layout(width = 'auto', height = 'auto'))
    
    # save button
    save1 = widgets.Button(description = '저장하기', button_style = 'info', layout = Layout(width = 'auto', height = 'auto'))
    
    # delete button
    delete1 = widgets.Button(description = '기존 User Data 삭제하기', button_style = 'warning', layout = Layout(width = 'auto', height = 'auto'))
    
    # recommend button
    recom1 = widgets.Button(description = '실행하기', button_style = 'primary', layout = Layout(width = 'auto', height = 'auto'))

    # sogang button
    sg1 = widgets.Button(description = '전처리를 진행하시겠습니까?', button_style = 'success', layout = Layout(width = 'auto', height = 'auto'))
    
    # everytime button
    et1 = widgets.Button(description = '크롤링을 진행하시겠습니까? (매우 오랜 시간이 소요될 수 있습니다.)', button_style = 'danger', layout = Layout(width = 'auto', height = 'auto'))
    
    # preprocessing button
    pre1 = widgets.Button(description = '전처리를 진행하시겠습니까?', button_style = 'success', layout = Layout(width = 'auto', height = 'auto'))
    
    # hs button
    hh1 = widgets.Button(description = '🍯 꿀 과목 추천', layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#FFD228'))
    ss1 = widgets.Button(description = '📗 배움 과목 추천', layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#7AF67A'))
    mm1 = widgets.Button(description = '📃 전공 리스트 보기', layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#FF9DFF'))
    nn1 = widgets.Button(description = '⛔ 처음으로', layout = Layout(width = 'auto', height = 'auto'), style = ButtonStyle(button_color = '#C8FFFF'))
    plus_4 = widgets.Dropdown(options = opt, value = '없음', description = '전공을 선택해주세요', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    plus_5 = widgets.Dropdown(options = opt, value = '없음', description = '전공을 선택해주세요', disabled = False, style = style, layout = Layout(width = 'auto', height = 'auto'))
    next_button1 = widgets.Button(description = '꿀이 흐르는 결과 보기', layout = Layout(width = 'auto', height = 'auto'))
    next_button2 = widgets.Button(description = '배움이 넘치는 결과 보기', layout = Layout(width = 'auto', height = 'auto'))

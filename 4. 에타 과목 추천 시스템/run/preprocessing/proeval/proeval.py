import numpy as np
import pandas as pd
import re
import os

import warnings
warnings.filterwarnings('ignore')

from tqdm import tqdm
tqdm.pandas()

from konlpy.tag import *
okt=Okt()

class ProEval:
    def __init__(self, path = '.'):
        self.path = path
        self.path_evaluation = self.path + '/data/et_evaluation/'
        
    def make_proeval(self):
        self.evaluation = pd.read_csv(self.path_evaluation + 'evaluation.csv', encoding = 'UTF-8-SIG')
        self.evaluation.dropna(inplace = True)
        self.evaluation.reset_index(inplace = True, drop = True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        def extractPhrase(x):
            return okt.morphs(x, stem=True) #형태소 추출
        def changeGgondae(x): # '꼰'
            c1 = x.count('꼰')
            c2 = x.count('깐깐')
            c3 = x.count('틀딱')
            c4 = x.count('권위')
            c5 = x.count('강요')
            c6 = x.count('라떼')
            c7 = x.count('나때')
            c8 = x.count('젊꼰')
            c9 = x.count('젋꼰')
            c10 = x.count('강압')
            c11 = x.count('명령')
            c12 = x.count('고집')
            c13 = x.count('아집')
            c14 = x.count('꼬장')
            c15 = x.count('꼽')
            return c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15
        def changeCute(x):
            c1 = x.count('귀엽다')
            c2 = x.count('귀여')
            c2 = x.count('귀요미')
            c3 = x.count('큐트')
            c4 = x.count('큐티')
            c5 = x.count('꿀귀')
            return c1+c2+c3+c4+c5
        def changeCharisma(x):
            c1 = x.count('카리스마')
            c2 = x.count('리더')
            return c1+c2
        def changeCold(x):
            c1 = x.count('시크')
            c2 = x.count('차갑')
            c3 = x.count('무심')
            c4 = x.count('도도')
            c5 = x.count('차도남')
            c6 = x.count('차도녀')
            return c1+c2+c3+c4+c5+c6
        def changeOpen(x):
            c1 = x.count('개방')
            c2 = x.count('오픈마인드')
            c3 = x.count('자유분방')
            return c1+c2+c3
        def changePassion(x):
            c1 = x.count('열정') 
            c2 = x.count('열성')
            c3 = x.count('열렬')
            c4 = x.count('열의')
            c5 = x.count('애정')
            c6 = x.count('열중')
            c7 = x.count('격렬')
            c8 = x.count('정렬')
            c9 = x.count('열심')
            return c1+c2+c3+c4+c5+c6+c7+c8+c9
        def changeAngel(x):
            c1 = x.count('사랑')
            c2 = x.count('친절')
            c3 = x.count('스윗')
            c4 = x.count('자상')
            c5 = x.count('천사')
            c6 = x.count('젠틀')
            c7 = x.count('엔젤')
            c8 = x.count('배려')
            c9 = x.count('세련')
            c10 = x.count('착하')
            c11 = x.count('러블리')
            c12 = x.count('힐링')
            c13 = x.count('갓')
            c14 = x.count('빛')
            c15 = x.count('강추')
            c16 = x.count('닥추')
            c17 = x.count('명강')
            c18 = x.count('띵강')
            c19 = x.count('감동')
            c20 = x.count('인생 강의')
            c21 = x.count('킹갓제네럴')
            c22 = x.count('적극 추천')
            c23 = x.count('짱짱맨')
            return c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15+c16+c17+c18+c19+c20+c21+c22+c23
        def changeGarbage(x):
            c1 = x.count('무례')
            c2 = x.count('쓰레기')
            c3 = x.count('적폐')
            c4 = x.count('지옥')
            c5 = x.count('짜증')
            c6 = x.count('스트레스')
            c7 = x.count('최악')
            c8 = x.count('고통')
            c9 = x.count('혐')
            c10 = x.count('개차반')
            c11 = x.count('불친절')
            c12 = x.count('듣지')
            c13 = x.count('월급')
            c14 = x.count('비호감')
            c15 = x.count('불합리')
            c16 = x.count('폐단')
            c17 = x.count('부조리')
            c18 = x.count('비추')
            c19 = x.count('쓰렉')
            c20 = x.count('불쾌')
            c21 = x.count('지옥')
            c22 = x.count('마세요')
            c23 = x.count('배울 게 없')
            c24 = x.count('도망치세요')
            c25 = x.count('도망쳐')
            c26 = x.count('할말하않')
            c27 = x.count('재앙')
            c28 = x.count('0점')
            c29 = x.count('악랄')
            c30 = x.count('악명')
            c31 = x.count('암덩어리')
            c32 = x.count('인성터짐')
            c33 = x.count('속터짐')
            c34 = x.count('핵폐기물')
            c35 = x.count('정신병자')
            c36 = x.count('드랍')
            c37 = x.count('거르세')
            c38 = x.count('걸러')
            c39 = x.count('개노답')
            c40 = x.count('살려줘')
            c41 = x.count('개판')
            c42 = x.count('헬')
            return c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15+c16+c17+c18+c19+c20+c21+c22+c23+c24+c25+c26+c27+c28+c29+c30+c31+c32+c33+c34+c35+c36+c37+c38+c39+c40+c41+c42
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.evaluation = (self.evaluation).groupby('교수명')['수강평'].unique().to_frame().reset_index()
        self.evaluation['개수'] = self.evaluation['수강평'].progress_apply(lambda x : len(x))
        self.evaluation['수강평'] = self.evaluation['수강평'].str.join(sep = ' ')
        self.evaluation['수강평'] = self.evaluation['수강평'].progress_apply(lambda x : extractPhrase(x)) 
        self.evaluation['수강평'] = self.evaluation['수강평'].str.join(sep =' ')
        self.evaluation['꼰대'] = self.evaluation['수강평'].progress_apply(lambda x : changeGgondae(x))
        self.evaluation['꼰대'] = self.evaluation['꼰대'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['귀요미'] = self.evaluation['수강평'].progress_apply(lambda x : changeCute(x))
        self.evaluation['귀요미'] = self.evaluation['귀요미'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['카리스마'] = self.evaluation['수강평'].progress_apply(lambda x : changeCharisma(x))
        self.evaluation['카리스마'] = self.evaluation['카리스마'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['시크'] = self.evaluation['수강평'].progress_apply(lambda x : changeCold(x))
        self.evaluation['시크'] = self.evaluation['시크'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['오픈마인드'] = self.evaluation['수강평'].progress_apply(lambda x : changeOpen(x))
        self.evaluation['오픈마인드'] = self.evaluation['오픈마인드'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['열정러'] = self.evaluation['수강평'].progress_apply(lambda x : changePassion(x))
        self.evaluation['열정러'] = self.evaluation['열정러'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['엔젤'] = self.evaluation['수강평'].progress_apply(lambda x : changeAngel(x))
        self.evaluation['엔젤'] = self.evaluation['엔젤'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['월급루팡'] = self.evaluation['수강평'].progress_apply(lambda x : changeGarbage(x))
        self.evaluation['월급루팡'] = self.evaluation['월급루팡'] * (1 + self.evaluation['개수']/1000)
        self.evaluation['호불호지수']=self.evaluation['엔젤'] - self.evaluation['월급루팡']
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.evaluation.dropna(inplace = True)
        self.evaluation.reset_index(inplace = True, drop = True)
        self.evaluation.to_csv(self.path_evaluation + 'professor_evaluation.csv', encoding = 'UTF-8-SIG', index = False)
    
    def run(self):
        self.make_proeval()
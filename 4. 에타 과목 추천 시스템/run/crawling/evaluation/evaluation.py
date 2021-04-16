from selenium import webdriver
from bs4 import BeautifulSoup
import bs4

from tqdm import tqdm
import pandas as pd
import numpy as np
import itertools
import time

class Evaluation:
    def __init__(self, path = '.'):
        self.path = path
        self.path_driver = self.path + '/data/driver/'
        self.path_et_evaluation = self.path + '/data/et_evaluation/'
        self.path_sg_course_lst = self.path + '/data/sg_course_lst/'
        
    def crawling_evaluation(self):
        url = 'https://everytime.kr/lecture'
        driver = webdriver.Chrome('./driver/chromedriver.exe')
        driver.maximize_window()
        driver.get(url)
        time.sleep(3)
        
        user_id = 'gi33808' # 에타 아이디 (추후 삭제 요망)
        et_login = driver.find_element_by_name("userid")
        et_login.clear()
        et_login.send_keys(user_id)

        user_pw = 'afm1908' # 에타 비번 (추후 삭제 요망)
        et_login = driver.find_element_by_name("password")
        et_login.clear()
        et_login.send_keys(user_pw)

        driver.find_element_by_xpath("""//*[@id="container"]/form/p[3]/input""").click()
        time.sleep(3)
        
        while True: # 광고 제거
            try:
                driver.find_element_by_xpath("""//*[@id="sheet"]/ul/li[3]/a""").click()
                time.sleep(3)
                break
            except:
                continue                
#----------------------------------------------------------------------------------------------------------------------------------------------------------       
        def make_evaluation(name):
            mid_result = []
            driver.get(url)
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="container"]/form/input[1]').click()
            course_search = driver.find_element_by_xpath('//*[@id="container"]/form/input[1]')
            course_search.send_keys(name)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="container"]/form/input[2]').click()
            time.sleep(4)

            # 과목 검색한 페이지 파싱
            page = driver.page_source
            soup = BeautifulSoup(page, "html.parser")

            # 과목별 강의 개수 확인 및 링크 수집
            cnt = len(soup.find_all('a', class_ = 'lecture'))
            link = []
            for m in range(cnt):
                link.append(soup.find_all('a', class_ = 'lecture')[m]['href'])

            # 강의별 강의평가 크롤링
            for i in range(len(link)):
                try:
                    if soup.find_all('span', class_ = 'star')[i].find('span')['style'] == 'width: 0%;':  # 강의평가 없는 경우
                        # 과목명 추가
                        mid_result.append(soup.find_all('p', class_ = 'name')[i].text)
                        # 교수명 추가
                        mid_result.append(soup.find_all('p', class_ = 'professor')[i].text)
                        # 전체평점 추가
                        mid_result.append('0')
                        # 나머지 NaN값 추가
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)
                        mid_result.append(np.nan)

                    else:  # 강의평가 있는 경우
                        driver.get('https://everytime.kr/' + link[i])
                        time.sleep(1)
                        page2 = driver.page_source
                        soup2 = BeautifulSoup(page2, "html.parser")

                        for j in range(0, 100):
                            try: 
                                str(soup2.find('div', class_ = 'articles').find_all('span', class_ = 'on')[j])
                                pass
                            except:
                                break
                            # 과목명 추가
                            mid_result.append(soup2.find('div', class_ = 'side head').find('h2').text)
                            # 교수명 추가
                            mid_result.append(soup2.find('div', class_ = 'side head').find('p').find('span').text)
                            # 전체평점 추가
                            mid_result.append(soup2.find('span', class_ = 'value').text)
                            # 과제 추가
                            mid_result.append(soup2.find('div', class_ = 'rating').find_all('p')[0].find('span').text)
                            # 조모임 추가
                            mid_result.append(soup2.find('div', class_ = 'rating').find_all('p')[1].find('span').text)
                            # 학점비율 추가
                            mid_result.append(soup2.find('div', class_ = 'rating').find_all('p')[2].find('span').text)
                            # 출결 추가
                            mid_result.append(soup2.find('div', class_ = 'rating').find_all('p')[3].find('span').text)
                            # 시험횟수 추가
                            mid_result.append(soup2.find('div', class_ = 'rating').find_all('p')[4].find('span').text)
                            # 개별평점 추가
                            if str(soup2.find('div', class_ = 'articles').find_all('span', class_ = 'on')[j])[31:34] == '100':
                                mid_result.append(100)
                            else:
                                mid_result.append(int(str(soup2.find('div', class_ = 'articles').find_all('span', class_ = 'on')[j])[31:33]))
                            # 수강학기 추가
                            mid_result.append(soup2.find_all('span', class_ = 'semester')[j].text[:7])
                            # 수강평 추가
                            mid_result.append(soup2.find_all('p', class_='text')[j].text)

                except:
                    break
            return mid_result
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.text_file = list(pd.read_csv(self.path_sg_course_lst + 'course_lst_total.txt', sep = ',').과목명.unique())
        self.result_lst = []
        for name in tqdm(self.text_file):
            try:
                result_lst.append(make_evaluation(name))
                print(name, ': 성공')
            except:
                print(name, ': 실패')
                break
        one_index = []
        two_index = []
        more_index = []
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        for i in range(len(self.result_lst)):
            if len(self.result_lst[i]) % 11 == 1:
                self.one_index.append(i)
            elif len(result_lst[i]) % 11 == 2:
                self.two_index.append(i)
            else:
                pass

        for i in self.one_index:
            self.result_lst[i] = self.result_lst[i][:len(self.result_lst[i]) - 1]
        for i in self.two_index:
            self.result_lst[i] = self.result_lst[i][:len(self.result_lst[i]) - 2]
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.result_lst2 = list(itertools.chain.from_iterable(self.result_lst))
        self.result_lst3 = [self.result_lst2[i : i + 11] for i in range(0, len(self.result_lst2), 11)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.result_df = pd.DataFrame(data = self.result_lst3, columns = ['과목명', '교수명', '전체평점', '과제', '조모임', '학점비율', '출결', '시험횟수', '개별평점', '수강학기', '수강평'])
        self.result_df.drop_duplicates(['과목명', '교수명', '수강평'], inplace = True)
        self.result_df.to_csv(self.path_et_evaluation + 'evaluation.csv', index = False, encoding = 'UTF-8-SIG')
        
    def run(self):
        self.crawling_evaluation()
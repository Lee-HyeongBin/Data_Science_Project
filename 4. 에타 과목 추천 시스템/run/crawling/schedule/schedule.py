from tqdm.notebook import tqdm
import pandas as pd
import numpy as np
import time
import os

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException

class Schedule:
    def __init__(self, path = '.'):
        self.path = path
        self.path_driver = self.path + '/data/driver/'
        self.path_et_schedule = self.path + '/data/et_schedule/'
        self.path_sg_course_lst = self.path + '/data/sg_course_lst/'
        
    def crawling_schedule(self):
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        def delete_adv_1():
            while True: # 광고 제거
                try:
                    driver.find_element_by_xpath("""//*[@id="sheet"]/ul/li[3]/a""").click()
                    time.sleep(1.5)
                    break
                except:
                    continue        
        def delete_adv_2():
            try:
                driver.find_element_by_xpath("""//*[@id="sheet"]/ul/li[3]/a""").click()
            except:
                pass
        def make_course_by_semester(year, semester, start, end):
            text_file = list(pd.read_csv(self.path_sg_course_lst + 'course_lst_' + str(year)[2:] + '_' + str(semester) + '.txt', sep = ',').과목명.unique())
            result_df = pd.DataFrame(columns = ['과목번호-분반', '과목명', '교수', '학점', '수업시간/강의실', '학년', '강의평', '담은 인원', '비고'])
            fault_lst = []

            delete_adv_2()
            driver.get(url + '/' + str(year) + '/' + str(semester))
            time.sleep(2.5)
            try:
                driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click()
                time.sleep(3)
            except ElementClickInterceptedException:
                driver.get(url + '/' + str(year) + '/' + str(semester))
                time.sleep(2.5)
                delete_adv_2()
                driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click()
                time.sleep(3)

            delete_adv_2()
            time.sleep(1)

            for name in tqdm(text_file[start:end]):
                # 1. 테이블 정보 가져오기
                try:
                    driver.find_element_by_xpath('//*[@id="subjects"]/div[1]/a[4]').click()
                    time.sleep(1)
                    course_search = driver.find_element_by_xpath('//*[@id="subjectKeywordFilter"]/div/input')
                    course_search.clear()
                    time.sleep(0.5)
                    course_search.send_keys(name)
                except ElementNotInteractableException or NoSuchElementException or ElementClickInterceptedException:
                    fault_lst.append(name)
                    continue

                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="subjectKeywordFilter"]/input').click()
                time.sleep(2.5)

                # 2. bs4로 parsing하기
                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                contents = []
                tmp = soup.find('div','list').find('tbody').find_all('td')

                for i in tmp:
                    tmp = i.get_text()
                    contents.append(tmp)
                contents = np.array(contents)
                column = []
                tmp = soup.find('div','list').find('thead').find_all('th')

                for k in tmp:
                    tmp = str(k).lstrip('<th>').split('<div>')
                    column.append(tmp[0])

                # 3. 데이터프레임 반환
                timetable = pd.DataFrame(contents.reshape(len(contents)//9,9), columns=column)

                # 4. 데이터프레임 병합
                result_df = result_df.append(timetable)

            # 5. 데이터프레임 중복 제거
            result_df.drop_duplicates(['과목번호-분반', '과목명'], inplace = True)
            return result_df, fault_lst
        def fault_course(year, semester, lst):
            text_file = lst
            result_df = pd.DataFrame(columns = ['과목번호-분반', '과목명', '교수', '학점', '수업시간/강의실', '학년', '강의평', '담은 인원', '비고'])

            for name in tqdm(text_file):
                print("(실패했던) 현재 검색중인 과목 이름 : {}".format(name))
                print()

                # 1. 테이블 정보 가져오기
                driver.get(url + '/' + str(year) + '/' + str(semester))
                time.sleep(3)
                delete_adv_2()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click()
                time.sleep(3)

                try:
                    delete_adv_2()
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="subjects"]/div[1]/a[4]').click()
                    time.sleep(3)
                    course_search = driver.find_element_by_xpath('//*[@id="subjectKeywordFilter"]/div/input')
                    course_search.send_keys(name)
                except ElementNotInteractableException or NoSuchElementException:
                    print("또 실패한 과목 이름 :", name)
                    continue

                time.sleep(1.5)
                driver.find_element_by_xpath('//*[@id="subjectKeywordFilter"]/input').click()
                time.sleep(2)

                # 2. bs4로 parsing하기
                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                contents = []
                tmp = soup.find('div','list').find('tbody').find_all('td')

                for i in tmp:
                    tmp = i.get_text()
                    contents.append(tmp)
                contents = np.array(contents)
                column = []
                tmp = soup.find('div','list').find('thead').find_all('th')

                for k in tmp:
                    tmp = str(k).lstrip('<th>').split('<div>')
                    column.append(tmp[0])

                # 3. 데이터프레임 반환
                timetable = pd.DataFrame(contents.reshape(len(contents)//9,9), columns=column)

                # 4. 데이터프레임 병합
                result_df = result_df.append(timetable)

            # 5. 데이터프레임 중복 제거
            result_df.drop_duplicates(['과목번호-분반', '과목명'], inplace = True)
            return result_df
        def start_crawling(year, semester):
            # 빈 데이터프레임 생성 (칼럼)
            result_mid = pd.DataFrame(columns = ['과목번호-분반', '과목명', '교수', '학점', '수업시간/강의실', '학년', '강의평', '담은 인원', '비고'])
            input_len = len(list(pd.read_csv(self.path_sg_course_lst + 'course_lst_' + str(year)[2:] + '_' + str(semester) +'.txt', sep = ',').과목명.unique()))
            # 결과 반환
            tmp, fault = make_course_by_semester(year, semester, 0, input_len)
            # 실패한 리스트 다시 시도
            fault_result = fault_course(year, semester, fault)
            # 결과 병합
            result = pd.DataFrame(columns = ['과목번호-분반', '과목명', '교수', '학점', '수업시간/강의실', '학년', '강의평', '담은 인원', '비고'])
            result = result.append(tmp)
            # 두 데이터 병합
            result = result.append(fault_result)
            result_mid = result_mid.append(result)

            # 최종 데이터 프레임 생성
            result_mid.drop_duplicates(['과목번호-분반', '과목명'], inplace = True)
            result_mid.to_csv(self.path_et_schedule + 'schedule_' + str(year) + '_' + str(semester) + '.csv', encoding = 'UTF-8-SIG', index = False)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
        url = 'https://everytime.kr/timetable'
        driver = webdriver.Chrome(self.path_driver + 'chromedriver.exe')
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
        
        delete_adv_1()
        self.year = 2020
        self.semester = 1
        while True:
            # 1. 크롤링 시작
            if (self.year, self.semester) == (2021, 2):
                break
            else:
                print("\n현재 크롤링이 진행중인 학기는 {0}년 {1}학기 입니다.".format(self.year, self.semester))
                start_crawling(self.year, self.semester)

            # 2. 연도/학기 재설정
            if self.semester == 1:
                self.semester += 1
            else:
                self.semester = 1
                self.year += 1
        self.year = 2016
        self.semester = 1
        self.result_final = pd.DataFrame(columns = ['과목번호-분반', '과목명', '교수', '학점', '수업시간/강의실', '학년', '강의평', '담은 인원', '비고'])
        while True:
            # 1. 병합 시작
            if (self.year, self.semester) == (2021, 2):
                break
            else:
                self.plus_schedule = pd.read_csv(self.path_et_schedule + 'schedule_' + str(self.year) + '_' + str(self.semester) + '.csv', encoding = 'UTF-8-SIG', index = False)
                self.result_final = result_final.append(self.plus_schedule)
                self.result_final.to_csv(self.path_et_schedule + 'schedule_final.csv', encoding = 'UTF-8-SIG', index = False)

            # 2. 연도/학기 재설정
            if self.semester == 1:
                self.semester += 1
            else:
                self.semester = 1
                self.year += 1
                
    def run(self):
        self.crawling_schedule()
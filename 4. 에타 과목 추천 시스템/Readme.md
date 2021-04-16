# 주의 사항
* 데이터 수집 및 전처리가 이미 완료된 알집 파일입니다. (오래 걸리기 때문에 미리 처리함) 따라서 바로 과목 추천 혹은 전공별 꿀/배움 과목 보기 옵션만 사용해주세요
* 폴더명을 Everytime으로 변경 후 실행해주세요 (4. 에타 과목 추천 시스템 → Everytime)
* ※ 표시는 사용자별 다른 파일이 필요하다는 것을 의미
<br>

# 폴더 설명
## 1. data
※ driver : 크롬 드라이버 경로 (exe)
- interface + font : 폰트 (ttf)
- interface + image + bond : 시간표 배경판 (csv)
- interface + image + course : 시간표 과목판 (csv)
- interface + image + start : 경로 수정 알리미판 (csv)
- et_competition : 에타 경쟁률 결과 (csv)
- et_evaluation : 에타 강의평, 교수별 특징 (csv)
- et_honeystudy : 꿀배움 과목 (csv)
- sg_capacity : 서강대 홈페이지 학기별 과목별 정원 (csv)
- sg_competition : 서강대 홈페이지 학기별 과목별 경쟁률 (csv)
- sg_course_lst : 서강대 홈페이지 학기별 과목명 (txt, csv)
<br>
## 2. result
- source : 모든 데이터를 merge + 전처리가 곁들여진 마지막 final_result 저장
- answer : source 파일과 userdb 파일을 활용하여 만들어진 유저별 최종 시간표 후보 파일 저장 공간
- imageDB : answer 파일을 활용해서 만든 이미지 저장 공간
<br>
## 3. run
- crawling + schedule : 에브리타임 시간표 크롤링 코드 파일이 저장되는 경로
- crawling + evaluation : 에브리타임 강의평가 크롤링 코드 파일이 저장되는 경로
- preprocessing + competition : 서강대 홈페이지 학기별 과목별 경쟁률 통일 코드 경로
- preprocessing + course : 서강대 홈페이지 학기별 과목명 생성 코드 경로
- preprocessing + honeystudy : 꿀배움 과목 생성 코드 경로
- preprocessing + proeval : 교수별 특징 생성 코드 경로
- preprocessing + ratio : 정원에 따른 경쟁률 생성 코드 경로
- preprocessing + merge : 1차 전처리가 완료된 파일 병합 코드 경로
- deleting : userdb를 리셋하는 코드 경로
- coursing : 유저별 시간표 과목 추천 코드 경로
<br>
## 4. userDB
- ipywidget으로 받은 정보 저장 (csv)
- 유저이름(학번)폴더 : 해당 유저의 시간표 저장 (png)

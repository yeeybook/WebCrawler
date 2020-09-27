import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd

URL = 'https://comic.naver.com/webtoon/weekday.nhn'
html = requests.get(URL).text # html 문서 전체를 긁어서 출력해줌, .text는 태그 제외하고 text만 출력되게 함
soup = BeautifulSoup(html, 'html.parser')

title = soup.find_all('a', {'class' : 'title'}) # a태그에서 class='title'인 html소스를 찾아 할당
id_list = [] ; title_list = [] ; author_list = [] ; day_list = [] ; genre_list = [] ; story_list = [] ; platform_list = []
num = 0

driver = webdriver.Chrome('C:/chromedriver.exe') # 크롬 사용하니까
driver.get(URL)

for i in range(len(title)):
    sleep(0.5) # 크롤링 중간 중간 텀을 주어 과부하 생기지 않도록

    page = driver.find_elements_by_class_name('title')
    page[i].click() #월요일 첫 번째 웹툰부터 순서대로 클릭

    sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser') # 이동한 페이지 주소 읽고 파싱

    day = soup.find_all('ul', {'class' : 'category_tab'})
    day = day[0].find('li', {'class' : 'on'}).text[0:1] # 요일 수집

    t = title[i].text
    if (t in title_list):  # 요일 두 개 이상이면 요일만 추가함
        day_list[title_list.index(t)] += ', ' + day
        driver.back()
        continue

    id_list.append(num) ; num += 1  # id 리스트에 추가
    title_list.append(t)  # 제목 리스트에 추가
    day_list.append(day) # 요일 리스트에 추가
    platform_list.append('네이버 웹툰') # 플랫폼 리스트에 추가

    author = soup.find_all('h2') # 두 번째 h2태그에 있음
    author = author[1].find('span', {'class' : 'wrt_nm'}).text[8:] # 7칸의 공백 후 8번 째부터 작가 이름임
    author_list.append(author) # 작가 리스트에 추가

    genre = soup.find('span', {'class' : 'genre'}).text # 장르 수집
    genre.replace("개그", "코믹") # 다음 웹툰과 장르 명칭 통합 위해
    genre_list.append(genre) # 장르 리스트에 추가

    story = soup.find_all('p') # 줄거리 수집
    story = str(story[3])
    story = story.replace('<p>', '').replace('</p>', '').replace('<br/>', '\n') # <br>을 개행으로 바꾸기
    story_list.append(story) # 줄거리 리스트에 추가

    driver.back() # 뒤로 가기

############################################크롤링 끝############################################

total_data = pd.DataFrame()
total_data['id'] = id_list
total_data['title'] = title_list
total_data['author'] = author_list
total_data['day'] = day_list
total_data['genre'] = genre_list
total_data['story'] = story_list
total_data['platform'] = platform_list
total_data.to_csv('네이버_웹툰.csv', encoding = 'utf-8-sig')

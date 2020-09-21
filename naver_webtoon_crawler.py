import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import pandas as pd

URL = 'https://comic.naver.com/webtoon/weekday.nhn'
html = requests.get(URL).content #html 문서 전체를 긁어서 출력해줌, .text는 태그 제외하고 text만 출력되게 함
soup = BeautifulSoup(html, 'html.parser')

title = soup.find_all('a', {'class' : 'title'}) #a태그에서 class='title'인 html소스를 찾아 할당
title_list = []
title_num = []

for i in range(len(title)):
    t = title[i].text
    if(t in title_list): #요일 두 개 이상이면 넘어감
        continue
    else:
        title_list.append(t)
        title_num.append(i)

#print(title_list)
driver = webdriver.Chrome('C:/chromedriver.exe') #크롬 사용하니까
driver.get(URL)

author_list = [] ; genre_list = [] ; day_list = []

for i in title_num:
    time.sleep(0.5) #크롤링 중간 중간 텀을 주어 과부하 생기지 않도록

    page = driver.find_elements_by_class_name('title')
    #class="title"인 모든 소스 가져옴
    #bs4는 find_all, selenium은 find_elements_by
    page[i].click()

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser') #이동한 페이지 주소 읽고 파싱

    day = soup.find_all('ul', {'class' : 'category_tab'})
    day = day[0].find('li', {'class' : 'on'}).text[0:2] + '일' #요일 수집
    day_list.append(day)

    author = soup.find_all('h2') #두 번째 h2태그에 있음
    author = author[1].find('span', {'class' : 'wrt_nm'}).text[8:] #7칸의 공백 후 8번 째부터 작가 이름임
    author_list.append(author)

    genre = soup.find('span', {'class' : 'genre'}).text #장르 수집
    genre_list.append(genre)

    # print(day_list[i],artist_list[i],genre_list[i])

    driver.back() #뒤로 가기

#-----------------------------------------크롤링 END-------------------------------

cols = []
total_data = pd.DataFrame(columns = cols)
total_data['id'] = title_num
total_data['title'] = title_list
total_data['author'] = author_list
total_data['day'] = day_list
total_data['genre'] = genre_list
# total_data.columns = ['id', 'title', 'author', 'day', 'genre']
# print(total_data.head())
total_data.to_csv('네이버웹툰.csv', encoding='euc-kr')
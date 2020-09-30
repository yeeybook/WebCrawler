from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://webtoon.daum.net/'
week = ['#day=mon&tab=day', '#day=tue&tab=day', '#day=wed&tab=day', '#day=thu&tab=day', '#day=fri&tab=day', '#day=sat&tab=day', '#day=sun&tab=day']
title_list = [] ; id_list = [] ; author_list = [] ;  day_list = []  ; genre_list = [] ; story_list = [] ; platform_list = []
num = 366 # 네이버 웹툰 id가 365까지였음

for i in range(7): #월요일부터 일요일까지
    URL = url + week[i]
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.get(URL) #요일별로 링크 가져옴

    sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser') # 제목, 작가, 요일 긁어오기 위해 현재 페이지 파싱

    title = soup.find_all('strong', {'class': 'tit_wt'}) # 제목 수집
    author = soup.find_all('span', {'class': 'txt_info'}) # 작가 수집
    day = soup.find('a', {'class': 'btn_comm link_tab on'}) # 요일 수집
    p = 0 # 첫 번째 작품 링크부터 들어가기 위해

    for j in range(len(title)):
        t = title[j].text
        if (t[:2] == '성인'): # 성인 웹툰이면 넘어감
            p += 1
            continue
        elif (t in title_list): # 요일 두 개 이상이면 요일만 추가하고 넘어감
            day_list[title_list.index(t)] += ', ' + day.text
            p += 1
            continue

        id_list.append(num) ; num += 1 # id 리스트에 추가
        title_list.append(t) # 제목 리스트에 추가
        author_list.append(author[j].text[3:]) # 작가 리스트에 추가
        day_list.append(day.text) # 요일 리스트에 추가
        platform_list.append('다음 웹툰') # 플랫폼 리스트에 추가

        page = WebDriverWait(driver, 15).until( # 필요한 데이터가 다 로딩될 때까지 최대 15초 기다려줌
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "link_wt")
            )
        )[:-10] # 밑에 있는 랭킹 10개는 가져올 필요 없음
        
        page[p].click()
        p += 1

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'txt_genre')
            )
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser') # 장르, 줄거리 가져오기 위해 현재 페이지 파싱

        genre = soup.find('dd', {'class': 'txt_genre'}).text.strip() # 장르 수집 (strip은 개행 제거 함수)
        genre_list.append(genre) # 장르 리스트에 추가

        story = soup.find('dd', {'class' : 'txt_story'}).text # 줄거리 수집
        story_list.append(story) # 줄거리 리스트에 추가

        driver.back()

        sleep(3)

############################################크롤링 끝############################################

total_data = pd.DataFrame()
total_data['id'] = id_list
total_data['title'] = title_list
total_data['author'] = author_list
total_data['day'] = day_list
total_data['genre'] = genre_list
total_data['story'] = story_list
total_data['platform'] = platform_list
total_data.to_csv('다음_웹툰.csv', encoding='utf-8-sig')

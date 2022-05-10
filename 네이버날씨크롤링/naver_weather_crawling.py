from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://search.naver.com/search.naver?query=%EB%82%A0%EC%94%A8'
response = requests.get(url)
html = response.text

if(response.status_code == 200):
    result = []

    soup = BeautifulSoup(html,'html.parser')
    source1 = soup.find('div', {'class':'report_card_wrap'})
    # print(source1)

    data1 = soup.find('ul',{'class':'today_chart_list'})
    # print(data1)

    # li 태그는 총 4개 이므로, 모두 가져오기 위해 find_all 이용
    data2 = data1.find_all('li')
    # print(data2)

    # 미세먼지 추출
    mise = data2[0].find('span', {'class':'txt'}).text
    print(f'현재 미세먼지 농도 : {mise}')

    # 초미세먼지 추출
    chomise = data2[1].find('span', {'class':'txt'}).text
    print(f'현재 초미세먼지 농도 : {chomise}')

    # 자외선 추출
    ultravio = data2[2].find('span', {'class':'txt'}).text
    print(f'현재 자외선 상태 : {ultravio}')

    # 일몰 추출
    sunset = data2[3].find('span', {'class','txt'}).text
    print(f'일몰 시간 : {sunset}')

    ##############추가 날씨 정보 출력하기#########################

    # source2 = soup.find('div', {'class':'temperature_info'})
    up = soup.find('dl', {'class', 'summary_list'})

    up2 = soup.find_all('dd')

    # 강수량 추출
    rainy = up2[0].text
    print(f'강수량 : {rainy}')
    # 습도 추출
    humi = up2[1].text
    print(f'습도 : {humi}')
    # 바람 추출
    wind = up2[2].text
    print(f'바람 : {wind}')

    print("{0:7} {1:<7} {2:<7} {3:<7} {4:<7} {5:<7} {6:<7} ".format(mise, chomise, ultravio, sunset, rainy, humi, wind))
    result.append([mise, chomise, ultravio, sunset, rainy, humi, wind])

with open('네이버날씨크롤링.csv', 'w') as f:
    f.write(f'미세먼지: {mise}' + '\n'
            + f'초미세먼지: {chomise}'+ '\n'
            + f'자외선: {ultravio}' + '\n'
            + f'일몰: {sunset}'+ '\n'
            + f'강수률: {rainy}'+ '\n'
            + f'습도: {humi}'+ '\n'
            + f'바람: {wind}')
f.close()


df = pd.read_csv('네이버날씨크롤링.csv', encoding='cp949')
print(df)

############## 온도 추출하기 ##############
temp = soup.find_all('div', {'class':'temperature_text'})[0].text
print(f'온도: {temp}')

with open('네이버날씨크롤링에 온도추가.csv', 'w', encoding='cp949') as f:
    f.write(f'온도: {temp}')

f.close()

################# 시간대별 온도 추출하기 ##################
time_temp = soup.find_all('div', {'class':'graph_inner _hourly_weather'})[0].text
pretty_time_temp = time_temp.replace(' ','')
# print(pretty_time_temp)
print('시간대별 날씨:'+pretty_time_temp)

with open('시간대별 날씨.csv', 'w', encoding='cp949') as f:
    f.write(f'시간대별 날씨: {pretty_time_temp}')
f.close()
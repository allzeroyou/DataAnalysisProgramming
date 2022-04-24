from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://search.naver.com/search.naver?query=%EB%82%A0%EC%94%A8'
response = requests.get(url)
html = response.text

if(response.status_code == 200):
    result = []

    soup = BeautifulSoup(html,'html.parser')

    # select 이용
    # weather = soup.select('ul.today_chart_list > li.item_today level1')
    # print(weather)
    # weather_2 = soup.select('li.item_today level1')
    # print(weather_2)

    misemongi = soup.select('a>span.txt')

    # find 이용
    # source1 = soup.find('div', {'class':'report_card_wrap'})
    # data1 = soup.find('ul',{'class':'today_chart_list'})
    # print(data1)
    # # li 태그는 총 4개 이므로, 모두 가져오기 위해 find_all 이용
    # data2 = data1.find_all('li')
    # print(data2)

    # 미세먼지 추출
    # mise = weather_2[0].find('span', {'class':'txt'}).text
    mise = misemongi[0].text
    print(f'현재 미세먼지 농도 : {mise}')

    # 초미세먼지 추출
    chomise = misemongi[1].text
    print(f'현재 초미세먼지 농도 : {chomise}')

    # 자외선 추출
    ultravio = misemongi[2].text
    print(f'현재 자외선 상태 : {ultravio}')

    # 일몰 추출
    sunset = misemongi[3].text
    print(f'일몰 시간 : {sunset}')

    ############## 추가 날씨 정보 출력하기 #########################

    # source2 = soup.find('div', {'class':'temperature_info'})
    source2 = soup.select_one('div.temperature_info>dl.summary_list')
    source3 = soup.select('dd.desc')

    # up = soup.find('dl', {'class', 'summary_list'})
    #
    # up2 = soup.find_all('dd')

    # 강수량 추출
    rainy = source3[0].text
    print(f'강수량 : {rainy}')
    # 습도 추출
    humi = source3[1].text
    print(f'습도 : {humi}')
    # 바람 추출
    wind = source3[2].text
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
temp = soup.select('div.temperature_text')[0].text
print(f'온도: {temp}')

# temp = soup.find_all('div', {'class':'temperature_text'})[0].text
# print(f'온도: {temp}')

with open('네이버날씨크롤링.csv', 'w', encoding='cp949') as f:
    f.write(f'온도: {temp}')

f.close()

################# 시간대별 온도 추출하기 ##################
time_temp_box = soup.select('li._li')

for time_temp in time_temp_box:
    time_temp_list = []
    time_temp_list.append(time_temp.text)
    print(time_temp.text)
    tomorrow = '23시' in time_temp.text
    if tomorrow:
        print('오늘의 날씨였습니다.')
        break
    else:
        print('------------------')


time_temp_find = soup.find_all('div', {'class':'graph_inner _hourly_weather'})[0].text
pretty_time_temp_find = time_temp_find.replace(' ','')
print(pretty_time_temp_find)

with open("weather_naver_time2.csv", "w", encoding="cp949") as f:
    f.write('시간대별 날씨 : ' + time_temp_find)
f.close()

# naver_weather_crawling = pd.DataFrame(time_temp_list, columns=('시간','날씨','온도'))
# naver_weather_crawling.to_csv('네이버날씨크롤링(4/24).csv', encoding='cp949', mode='w', index=True)
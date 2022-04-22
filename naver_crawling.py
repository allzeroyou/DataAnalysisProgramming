import urllib.request
import datetime
import json

# 내가 작성한 코드
client_id = 'yFmfMjVpmOKWgJJ0bbxw'
client_secret = 'ZyIwBR6iPz'

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Name-Client-Id", client_id)
    req.add_header("X-Name-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success"%datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("Error Code")
        return None

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if responseDecode == None :
        return None
    else:
        return json.loads(responseDecode)

def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append(
        {'cnt':cnt,
         'title':title,
         'description': description,
         'org_link':org_link,
         'link': org_link,
         'pDate':pDate}
    )
    return


def main():
    node = 'news'
    # 크롤링 할 대상-네이버 검색 API에서 검색할 대상 노드
    srcText = input('검색어를 입력하세요: ')
    # 사용자 입력으로 받은 검색어 저장
    cnt = 0 # 검색 결과 카운트
    jsonResult = [] # 검색 결과를 정리해 저장할 리스트 객체

    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    # getNaverSearch(node, srcText, start, display): 조건에 맞게 url을 만들어주고 검색하여 그 값을 반환
    total = jsonResponse['total']

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        # json.dumps : json 파일 생성/ 함수 파라미터로 json 을 깔끔하게 정렬
    outfile.write(jsonFile)

    while((jsonResponse != None) and (jsonResponse['display']!= 0)):
        # 값이 있는 경우 => 참
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)

        start = jsonResponse['start']+jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)

        print('전체 검색 : %d 건' %total)

        with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)

            outfile.write(jsonFile)

        print('가져온 데이터: %d건'%(cnt))
        print('%s_naver_%s.json SAVED'%(srcText, node))

if __name__ == '__main__': # 해당파일에 main이 있음을 명시적으로 표기
    main()
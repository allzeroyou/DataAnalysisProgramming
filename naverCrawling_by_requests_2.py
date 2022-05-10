import urllib.request
import datetime
import json
import requests

# 개인별 API 요청 인증키
client_id = 'yFmfMjVpmOKWgJJ0bbxw'
client_secret = 'ZyIwBR6iPz'

def getRequestUrl (url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#######################################################################################
# 위 코드를 requests 모듈 사용하기 (과제 정답)
def getRequestUrl_by_request (url, search_keyword, start, display):
    params = {'query': search_keyword, 'start': start, 'display': display}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            print('200 OK')
            contents = response.text
            return contents
    except Exception as e:
        print(e)
        print("Error for", response)
        return None

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)


    #url = base + node + parameters
    #responseDecode = getRequestUrl(url)  # [CODE 1]

    url = base + node
    responseDecode = getRequestUrl_by_request(url, srcText, start, display)

    if (responseDecode == None):
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

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description, 'org_link': org_link,
                       'link': org_link, 'pDate': pDate})
    return


def main():
    node = 'news'
    # 크롤링 할 대상-네이버 검색 API에서 검색할 대상 노드(node는 blog등으로 Input 가능)
    srcText = input('검색어를 입력하세요: ')
    cnt = 0  # 검색 결과 카운트
    jsonResult = []  # 검색 결과를 정리해 저장할 리스트 객체

    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    # getNaverSearch(node, srcText, start, display): 조건에 맞게 url 만들어 주고 검색 하여 그 값을 반환
    total = jsonResponse['total']

    with open('%s_jsonResponse_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResponse, indent=4, sort_keys=True, ensure_ascii=False)
        # json.dumps: 사전형 데이터를 JSON 문자열로써 정형화해 출력(가독성을 높임)
        # indent:띄어쓰기(가독성) #sort_keys:오름차순정렬 #ensure_ascii: 한글깨짐방지
        outfile.write(jsonFile)

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        # 검색결과가 있는 경우(없지 않은 경우)
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)  # [CODE 3]
            # 받은 데이터를 처리함.

        # start: 1001이 되는 순간 빠져나옴
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)  # [CODE 2]

    print('전체 검색 : %d 건' % total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)

        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" % (cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))


if __name__ == '__main__':
    main()

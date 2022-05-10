import urllib.request
import datetime
import time
import json

# 개인이 발급받은 api 정보 입력
client_id = 'yFmfMjVpmOKWgJJ0bbxw'
client_secret = 'ZyIwBR6iPz'


#[CODE 1]
def getRequestUrl(url):    
    req = urllib.request.Request(url)
    # header 정보에 clinet id, secret 전달
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getNaverSearch(node, srcText, start, display):    
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)
    
    url = base + node + parameters    
    responseDecode = getRequestUrl(url)   #[CODE 1]
    
    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

#[CODE 3]
def getPostData(post, jsonResult, cnt):    
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    
    pDate = datetime.datetime.strptime(post['pubDate'],  '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
    
    jsonResult.append({'cnt':cnt, 'title':title, 'description': description, 'org_link':org_link,
                       'link': org_link, 'pDate':pDate})
    return    

#[CODE 0]

def main():
    node = 'news'
    # 크롤링 할 대상-네이버 검색 API에서 검색할 대상 노드(node는 blog등으로 Input 가능)
    srcText = input('검색어를 입력하세요: ')
    # 사용자 입력으로 받은 검색어 저장
    cnt = 0 # 검색 결과 카운트
    jsonResult = [] # 검색 결과를 정리해 저장할 리스트 객체

    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    # getNaverSearch(node, srcText, start, display): 조건에 맞게 url을 만들어주고 검색하여 그 값을 반환
    total = jsonResponse['total']


    with open('%s_jsonResponse_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResponse, indent = 4, sort_keys=True, ensure_ascii=False)
        # json.dumps: 사전형 데이터를 JSON 문자열로써 정형화해 출력(가독성을 높임)
                                    #indent:띄어쓰기(가독성) #sort_keys:오름차순정렬 #ensure_ascii: 한글깨짐방지
        outfile.write(jsonFile)
 
    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        # 검색결과가 있는 경우(없지 않은 경우)
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)  #[CODE 3]
            # 받은 데이터를 처리함.
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)  #[CODE 2]
       
    print('전체 검색 : %d 건' %total)
    
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult,  indent=4, sort_keys=True, ensure_ascii=False)
                        
        outfile.write(jsonFile)
        
    print("가져온 데이터 : %d 건" %(cnt))
    print ('%s_naver_%s.json SAVED' % (srcText, node))


if __name__ == '__main__':
    main()

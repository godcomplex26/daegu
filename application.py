import re
from datetime import datetime
import json, urllib.request
from flask import Flask, request, jsonify, abort
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello goorm!"


@application.route("/a")
def hello2():
    return "<h1 style='color:cyan'>Hello goorm!</h1>"


@application.route("/hello_kakao", methods=['POST'])
def kakaoHello():
    body = request.get_json()
    print(body)
    mymsg = body['userRequest']['utterance']
    print('@----@')
    param1 = ''
    param2 = ''
    try:
        param1 = body['action']['detailParams']['Plant']['value']
        param2 = body['action']['detailParams']['sys_date']['value']
        print(param1)
        print(param2)
        print(body['action']['detailParams']['Plant']['origin'])
        print(body['action']['detailParams']['sys_date']['origin'])
    except:
        print('error')
        pass
    print('@----@')
    responseMsg = {
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': f"""당신의 메세지:{mymsg}"""
                }
            }]
        }
    }
    return responseMsg


@application.route("/mylotto", methods=['POST'])
def getLotto():
    resPonseMsg = ''
    lottourl = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo='
    drwNo = 1
    try:
        body = request.get_json()
        drwNo = body['action']['detailParams']['Lotto']['origin']
        drwNo = isdrwNoValid(drwNo)
        lottourl += str(drwNo)
        print(drwNo)
    except:
        try:
            if (body['action']['detailParams']['Current']['value'] == '최신'):
                drwNo = getCurrentRound()
            lottourl += str(drwNo)
        except:
            lottourl += str(drwNo)
        print(body)
        print(drwNo)
    res = urllib.request.urlopen(lottourl)
    res_msg = res.read().decode('utf8')
    jres = json.loads(res_msg)
    if jres['returnValue'] != 'success':
        resPonseMsg = '잘못된 입력입니다.'
    else:
        resPonseMsg = f"""
        {jres['drwtNo1']} {jres['drwtNo2']} {jres['drwtNo3']}
        {jres['drwtNo4']} {jres['drwtNo5']} {jres['drwtNo6']}
        보너스 : {jres['bnusNo']}
        """
    responseBody = {
        'version':'2.0',
        'template' : {
            'outputs' : [
                {
                    'simpleText' : {
                        'text' : resPonseMsg
                    }
                },
                {
                    'simpleImage' : {
                        'imageUrl':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlhPa-bfqWN69U5NnkX0NuE4yz-UmLGHtNCSVmc_hnQw&s',
                        'altText' : 'Lotto이미지'
                    }
                }
            ]
        }
    }
    return responseBody


def getCurrentRound():
    standardRound = 1115
    standardDate = datetime.strptime('2024-04-13', '%Y-%m-%d')
    today = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    date_diff = (today - standardDate).days
    count = date_diff//7
    return standardRound + count


def isdrwNoValid(drwNo):
    drwNo = extract_numbers(drwNo)
    if (int(drwNo) < 1):
        drwNo = 1
    elif (int(drwNo) > getCurrentRound()):
        drwNo = getCurrentRound()
    return drwNo


def extract_numbers(text):
    return re.sub(r'[^0-9]', '', text)


@application.route("/kakao_daegu", methods=["POST"])
def getDaegu():
    url = f'https://www.daegufood.go.kr/kor/api/tasty.html?mode=json&addr=%EC%A4%91%EA%B5%AC'
    
    
    
    
    resPonseMsg = ''
    try:
        body = request.get_json()
        drwNo = body['action']['detailParams']['Lotto']['origin']
        drwNo = isdrwNoValid(drwNo)
        lottourl += str(drwNo)
        print(drwNo)
    except:
        try:
            if (body['action']['detailParams']['Current']['value'] == '최신'):
                drwNo = getCurrentRound()
            lottourl += str(drwNo)
        except:
            lottourl += str(drwNo)
        print(body)
        print(drwNo)
        
    res = urllib.request.urlopen(url)
    res_msg = res.read().decode('utf8')
    jres = json.loads(res_msg)    
    
    if jres['returnValue'] != 'success':
        resPonseMsg = '잘못된 입력입니다.'
    else:
        resPonseMsg = jres['data']
    responseBody = {
        'version':'2.0',
        'template' : {
            'outputs' : [
                {
                    'simpleText' : {
                        'text' : resPonseMsg
                    }
                },
                {
                    'simpleImage' : {
                        'imageUrl':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlhPa-bfqWN69U5NnkX0NuE4yz-UmLGHtNCSVmc_hnQw&s',
                        'altText' : 'Lotto이미지'
                    }
                }
            ]
        }
    }
    return responseBody
    
    return jres


@application.route("/daegu")
def getDaegu():
    url = f'https://www.daegufood.go.kr/kor/api/tasty.html?mode=json&addr=%EC%A4%91%EA%B5%AC'
    res = urllib.request.urlopen(url)
    res_msg = res.read().decode('utf8')
    jres = json.loads(res_msg)
    return jres

if __name__ == '__main__':
    application.run('0.0.0.0', port=5087, debug=True)
from flask import Flask, render_template, request, redirect 
import random
 # render_template  html을 리턴해줌.

## Flask 클래스 생성
## __name__ : 파일의 이름
app = Flask(__name__)

# @ 네비게이터 : 바로 아래에 있는 함수를 실행하겠다.
# route(주소) : 주소에 요청을 하면 아래의 함수를 실행
# 127.0.0.1 내컴퓨터,  5000: default 포트번호
# @app.route('/') : 127.0.0.1:5000/ 주소에 요청하는 경우 아래의 함수를 실행
@app.route('/')  
def index():
    return 'Hello world'

#127.0.0.1 = local host
# 127.0.0.1:5000/main 이라는 주소로 요청을 하는 경우 아래의 함수를 실행
@app.route('/main')
def main():
    return render_template('main.html')   # render_template  html을 리턴해줌.

# 새로운 api 생성
# localhost:5000/login 주소로 생성
@app.route('/login')
def login():
    # main.html에서 데이터를 보내는 형식
    # {id: xxxx, pass: xxxx}
    _id = request.args.get('id')
    _pass = request.args.get('pass')
    print(_id, _pass)
    if (_id == 'test') & (_pass == '1234'):  # id가 'test'이고, pass가 '1234'일때만 성공
        # return '로그인 성공'
        return render_template('second.html')
    else:
        # retrun '로그인 실패'
        # 로그인 실패시 localhost:5000/main(127.0.0.1:5000/main)으로 이동
        return redirect('/main')
        # return _id, _pass

# localhost:5000/data api 생성
# post 형태로 요청시 
@app.route('/data',methods=['post'])
def data():
    _use = request.form['use']  # post는 form 함수 사용
    _list = ['바위', '가위', '보']
    choice_list = random.choice(_list)

    # 무승부인 경우
    if _use == choice_list:
        return '무승부'
    elif _use == '바위':
        if choice_list == '가위':
            result = '승'
        else:
            result = '패'
    elif _use == '가위': 
        if choice_list == '보':
            result = '승'
        else:
            result = '패'
    else:  
        if choice_list == '바위':
            result = '승'
        else:
            result = '패'
    return render_template('result.html', res = result)



# server를 경로복사하고, cmd 창에서 cd C:\Users\ezen\Documents\GitHub\python_ezen\Server한다음
# python index.py 실행   
# 실행이 안된다면 기존의 서버 창이 열려있는지 확인하고, 열려있으면 창을 닫는다.  


# app.run()  # 위의 코드를 실행하겠다는 함수
app.run(port=8080)  # 포트번호 바꾸기
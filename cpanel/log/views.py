from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
import pyrebase
import jwt


#firebase 프로젝트 정보
config ={
    'apiKey': "AIzaSyCKBN_w-mQNi1B0EIvIwOghr7y5afSkIb4",
    'authDomain': "club-management-system-bc814.firebaseapp.com",
    'projectId': "club-management-system-bc814",
    'storageBucket': "club-management-system-bc814.appspot.com",
    'messagingSenderId': "99652543260",
    'appId': "1:99652543260:web:d17e2bb697763a947950d9",
    'measurementId': "G-Z5R49455MZ",    
    'databaseURL': "https://club-management-system-bc814-default-rtdb.firebaseio.com/"
}

#firebase 연동
firebase = pyrebase.initialize_app(config)

#자격 증명
authe = firebase.auth()
database = firebase.database()

# Create your views here.
def signIn(request):
    return render(request, "signIn.html")

#로그인 함수
def postsign(request):
    #email과 password를 받는다.
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)  #firebase의 authe API를 사용하여 로그인 정보 확인
    except:
        message = "invalid credentials" #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})    #signIn 화면 출력하면서 메세지 전송

    #로그인 정보를 계속해서 유지하기 위해 FIREBASE에서 제공하는 ID Token을 django 섹션에 저장하는 것이다.
    session_id=user['idToken']
    uid = extract_uid_from_id_token(session_id)
    request.session['uid'] = str(uid)
    return HttpResponseRedirect(reverse('your_view'))

def logout(request):
    try:
        del request.session['uid']   #django의 로그아웃 함수
    except KeyError:
        pass
    return render(request, "index.html")   #signIn 화면 다시 출력

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#UID 추출 및 세션에 저장하는 Django 코드
def extract_uid_from_id_token(id_token):
    try:
        # Firebase에서 발급한 JWT 디코딩
        decoded_token = jwt.decode(id_token, options={"verify_signature": False}, algorithms=["RS256"])

        # UID 추출
        uid = decoded_token.get('user_id') or decoded_token.get('sub')

        return uid
    
    except jwt.ExpiredSignatureError:
        # 토큰의 유효 기간이 만료된 경우
        print("Token has expired.")
        return None

    except jwt.InvalidTokenError as e:
        # 유효하지 않은 토큰인 경우
        print(f"Invalid token: {e}")
        return None



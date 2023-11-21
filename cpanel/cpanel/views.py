from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
import pyrebase
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


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

#로그인 페이지 출력
def index(request):
        return render(request, "index.html")

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
    request.session['uid'] = str(session_id)
    return HttpResponseRedirect(reverse('index'))

def logout(request):
    try:
        del request.session['uid']   #django의 로그아웃 함수
    except KeyError:
        pass
    return render(request, "index.html")   #signIn 화면 다시 출력

#회원가입 페이지
def signUp(request):
    return render(request, "signup.html")

#회원가입하기
def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    uid = user['localId']
    data = {"name": name, "status": "1"}

    database.child("users").child(uid).child("detail").set(data)
    return render(request, "signIn.html")

def create(request):
    return render(request,"create.html")

def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))

    work = request.POST.get('work')
    progress = request.POST.get('progress')

    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        print("info"+str(a))

        data = {
            "work": work,
            "grogress": progress
        }
        database.child('users').child(a).child('reports').child('millis').set(data)
        name = database.child("users").child(a).child('details').child('name').get(idtoken).val()
        return render(request, "welcome.html", {'e':name})
    except KeyError:
        message = "Oops! User Logged out Please SignIn Again"
        return render(request, "signIn.html",{"messg": message})
    
def members(request):
    if 'uid' not in request.session:
        message = "login please." #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})

    return render(request, "members.html")

def money(request):
    if 'uid' not in request.session:
        message = "login please." #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})

    return render(request, "money.html")


def calendar(request):
    if 'uid' not in request.session:
        message = "login please." #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})
    
    return render(request, "calendar.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

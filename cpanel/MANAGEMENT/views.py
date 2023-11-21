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
    
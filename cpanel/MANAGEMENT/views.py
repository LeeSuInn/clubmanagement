from django.shortcuts import render, HttpResponseRedirect
import pyrebase
from google.cloud import firestore



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
db = firestore.Client()

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
    
    
def your_view(request):
    user_uid = request.session.get('uid')

    # 모든 컬렉션에 대해 반복
    for collection in db.collections():
        # 각 컬렉션의 이름과 세션의 uid 비교
        if collection and user_uid == collection.id:
            # DocumentReference를 가져오기
            doc_ref = db.collection(str(collection.id)).document("동아리")
            # DocumentSnapshot을 가져오기
            document_snapshot = doc_ref.get()
            
            # 문서의 데이터 가져오기
            data = document_snapshot.to_dict()

            club_name = data.get('동아리 이름', '')  # 동아리 이름에 해당하는 key 사용

            # 뷰에서 템플릿에 전달할 컨텍스트 변수 설정
            context = {'CLUBNAME': club_name}

    # 뷰에서 렌더링된 HTML 템플릿 반환
    return render(request, 'index.html', context)

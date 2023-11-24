from django.shortcuts import render
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

#사이트 띄우기
def money(request):
    if 'uid' not in request.session:
        message = "login please." #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})

    return render(request, "money.html")

#사이트 띄우기
def pay_dues_list(request):
    if 'uid' not in request.session:
        message = "login please." #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})

    user_uid = request.session.get('uid', '')  # 세션에서 사용자 UID 가져오기
    payments = get_pay_dues__data(user_uid)

    return render(request, 'pay_dues.html', {'payments': payments})

#firestore에서 데이터 가져오기
def get_pay_dues__data(user_uid):
    members_ref = db.collection(user_uid).document('동아리').collection('회비 관리')

    payments = []
    for member_doc in members_ref.stream():
        member_data = member_doc.to_dict()
        
        # 여기서 1학기, 2학기를 boolean 값으로 변환하여 payments 리스트에 추가
        payments.append({
            '학번': member_doc.id,
            '이름': member_data.get('이름', ''),
            '1학기': bool(member_data.get('1학기', False)),
            '2학기': bool(member_data.get('2학기', False)),
        })
    return payments
import json
from django.http import JsonResponse
from django.shortcuts import render
import pyrebase
from google.cloud import firestore
from django.views.decorators.cache import cache_control


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
            '1학기': member_data.get('1학기', None),
            '2학기': member_data.get('2학기', None),
        })
    return payments

def sanitize_document_id(document_id):
    # 특수 문자 및 공백 제거
    cleaned_id = ''.join(e for e in document_id if e.isalnum())
    # 길이 제한
    return cleaned_id[:150]


def pay_dues_edit(request):
    user_uid = request.session.get('uid', '')  # 세션에서 사용자 UID 가져오기
    payments = get_pay_dues__data(user_uid)

    if request.method == 'POST':
        # POST 요청이면 수정된 데이터를 Firestore에 업데이트
        json_data = json.loads(request.body.decode('utf-8'))
        updated_data_list = json_data.get('updated_data', [])

        for updated_data in updated_data_list:
            # 각 행에서 1학기와 2학기 값을 가져옴
            student_id = updated_data.get('학번')  # '학번'과 같은 키 사용
            
            if student_id is not None:
                # 각 학생의 데이터 추출
                value1 = updated_data.get('1학기')
                value2 = updated_data.get('2학기')

            # Firestore에 업데이트
                firestore_document = db.collection(user_uid).document("동아리").collection("회비 관리").document(student_id)
                try:
                    firestore_document.update({
                        '1학기': value1,
                        '2학기': value2,
                    })
                    print("Firestore 업데이트 성공")
                except Exception as e:
                    print(f"Firestore 업데이트 실패: {e}")
            else:
                # student_id가 None인 경우에 대한 처리
                print("학생 ID가 None입니다. 데이터를 처리하지 않습니다.")

        return JsonResponse({'status': 'success'})

    return render(request, 'pay_dues.html', {'payments': payments})
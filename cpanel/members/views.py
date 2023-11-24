import json
from django.shortcuts import render
import pyrebase
from firebase_admin import firestore
from django.http import JsonResponse
from google.cloud import firestore
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt



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

def members(request):
    if 'uid' not in request.session:
        message = "login please." #틀린 정보일 때 경고 메세지
        return render(request, "signIn.html", {"messg":message})

    return render(request, "members.html")

def get_data(request):
    # Firestore에서 데이터 가져오기
    
    # 세션에서 사용자의 ID 가져오기 (가정)
    user_uid = request.session.get('uid')

    # 모든 컬렉션에 대해 반복
    all_collections = db.collections()
    for collection in all_collections:
        # 각 컬렉션의 이름과 세션의 uid 비교
        
        if collection and user_uid == collection.id:
            # 일치하는 경우 해당 컬렉션 내의 "부원" 서브컬렉션에 접근
            doc_ref = db.collection(str(collection.id)).document('동아리').collection('부원')
            docs = doc_ref.stream()

            # 이후 데이터 처리 또는 반환 등을 수행
    if docs:
        # Firestore 문서 데이터를 JSON 형식으로 변환하여 응답
        data = [doc.to_dict() for doc in docs]
        return JsonResponse({'status': 'success', 'data': data}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'status': 'error', 'message': 'No documents found'})

@require_POST
def add_member(request):
    user_uid = request.session.get('uid')
    try:
        # 클라이언트에서 전송한 데이터 가져오기
        data = request.POST

        # Firestore에 데이터 추가
        members_ref = db.collection(str(user_uid)).document('동아리').collection('부원')

        학번 = data.get('학번', '')
        member_ref = members_ref.document(학번)
        member_ref.set({ 
            '학번': 학번,
            '이름': data.get('이름', ''),
            '전화번호': data.get('전화번호', ''),
            '이메일': data.get('이메일', ''),
            '직책': data.get('직책', ''),
        })


        return JsonResponse({'status': 'success', 'message': '부원을 성공적으로 추가하였습니다.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_POST
def delete_members(request):
    try:
        # 클라이언트에서 전송한 데이터 가져오기
        data = json.loads(request.body.decode('utf-8'))
        학번Array = data.get('학번Array', [])

        # 현재 세션의 uid를 가져옴
        user_uid = request.session.get('uid')
        
        # uid를 이용하여 해당 컬렉션을 가져옴
        collection_ref = db.collection(str(user_uid)).document('동아리').collection('부원')

        for 학번 in 학번Array:
            # 문서 ID로 학번을 사용하여 해당 문서 삭제
            doc_ref = collection_ref.document(학번)
            doc_ref.delete()

        return JsonResponse({'status': 'success', 'message': '선택한 부원들을 성공적으로 삭제하였습니다.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def edit_member(request):
    if request.method == 'POST':
        try:
            # 클라이언트로부터 받은 JSON 데이터를 파싱합니다.
            data = json.loads(request.body.decode('utf-8'))

            # 현재 세션의 uid를 가져옴
            user_uid = request.session.get('uid')

            # 학번을 기준으로 해당 멤버를 찾습니다.
            member_ref = db.collection(user_uid).document('동아리').collection('부원').document(data['학번'])

            # 수정된 데이터로 업데이트합니다.
            member_ref.update({
                '이름': data['이름'],
                '전화번호': data['전화번호'],
                '이메일': data['이메일'],
                '직책': data['직책'],
            })

            return JsonResponse({'status': 'success', 'message': '멤버 정보가 성공적으로 수정되었습니다.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

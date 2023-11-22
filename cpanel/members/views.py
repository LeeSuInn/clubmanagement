import logging
from django.shortcuts import render
import pyrebase
from firebase_admin import firestore
from django.http import JsonResponse
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

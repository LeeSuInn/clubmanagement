import json
from django.http import JsonResponse
from django.shortcuts import render
import pyrebase
from django.views.decorators.csrf import csrf_exempt
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

def cash_page(request):
        if 'uid' not in request.session:
            message = "login please." #틀린 정보일 때 경고 메세지
            return render(request, "signIn.html", {"messg":message})

        return render(request, "money.html")


def financial_list(request):
    user_uid = request.session.get('uid')
    transactions_ref = db.collection(user_uid).document('동아리').collection('회비 내역')
    transactions = transactions_ref.stream()

    cash_ref = db.collection(user_uid).document('동아리')
    cash_document = cash_ref.get()
    
    # cash_document가 None이 아닌 경우에만 to_dict()를 호출
    cash_balance = cash_document.to_dict().get("잔액") if cash_document else None

    combined_data = {
        '회비 내역': [transaction.to_dict() for transaction in transactions],
        '잔액': cash_balance
    }
    
    return JsonResponse({'status': 'success', 'data': combined_data}, json_dumps_params={'ensure_ascii': False})

def add_money(request):
    user_uid = request.session.get('uid')
    try:
        # 클라이언트에서 전송한 데이터 가져오기
        data = request.POST

        # Firestore에 데이터 추가
        money_ref = db.collection(user_uid).document('동아리').collection('회비 내역')
        dues_ref = db.collection(user_uid).document('동아리')
        dues_snapshot = dues_ref.get()

        # 데이터 가져오기
        dues = int(dues_snapshot.to_dict().get('잔액'))

        cash_ref = money_ref.document()
        cash_ref.set({ 
            '금액': int(data.get('금액',0)),
            '날짜': data.get('날짜', ''),
            '사유': data.get('사유', ''),
            '입/출금': data.get('입/출금', ''),
        })

        if data.get('입/출금', '') == "입금":
            dues += int(data.get('금액', ''))
        else:
            dues -= int(data.get('금액', ''))

        # 동아리 문서 업데이트
        dues_ref.update({'잔액': dues})

        return JsonResponse({'status': 'success', 'message': '회비를 성공적으로 추가하였습니다.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def edit_money(request):
    if request.method == 'POST':
        try:
            # 클라이언트로부터 받은 JSON 데이터를 파싱합니다.
            data = json.loads(request.body.decode('utf-8'))
            # 현재 세션의 uid를 가져옴
            user_uid = request.session.get('uid')
            # 데이터를 비교하여 문서를 찾습니다.
            money_collection_ref = db.collection(user_uid).document('동아리').collection('회비 내역')
            dues_ref = db.collection(user_uid).document('동아리')

            #동아리의 필드값들을 가져옴
            dues_snapshot = dues_ref.get()

            #필드 중 잔액 필드 값을 가져온다.
            dues = int(dues_snapshot.to_dict().get('잔액'))

            # 스트림을 통해 모든 문서 가져오기
            documents = money_collection_ref.get()

            #수정할 문서 초기화
            edit_doc = None

            for doc in documents:
                docs = doc.to_dict()
                in_out_data = docs.get("입/출금")
                date_data = docs.get("날짜")
                reason_data = docs.get("사유")
                cash_data = int(docs.get("금액"))                

                if (
                    data['selectedRowData']['입출금'] == in_out_data and 
                    data['selectedRowData']['날짜'] == date_data and 
                    data['selectedRowData']['사유'] == reason_data and 
                    int(data['selectedRowData']['금액']) == cash_data
                    ):
                    edit_doc = doc
                    break
                    

            # edit_doc이 None이 아닌지 확인
            if edit_doc is not None:
                # 수정할 문서의 참조를 가져옵니다.
                edit_doc_ref = money_collection_ref.document(edit_doc.id)

                # 수정된 데이터로 업데이트합니다.

                edit_doc_ref.update({
                    '입/출금': data['입출금'],
                    '날짜': data['날짜'],
                    '사유': data['사유'],
                    '금액': int(data['금액']),
                })

                if data['입출금'] == "입금":
                    dues = dues + int(data['금액']) - int(data['selectedRowData']['금액'])
                else:
                    dues = dues - int(data['금액']) - int(data['selectedRowData']['금액'])
            dues_ref.update({'잔액': dues})

            return JsonResponse({'status': 'success', 'message': '멤버 정보가 성공적으로 수정되었습니다.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
@csrf_exempt
def delete_selected_rows(request):
    user_uid = request.session.get('uid', '')  # 세션에서 사용자 UID 가져오기
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_data = data.get('selectedData', [])

            doc_ref = db.collection(user_uid).document('동아리').collection('회비 내역')
            documents = doc_ref.get()
            del_doc = None

            dues_ref = db.collection(user_uid).document('동아리')
            dues_snapshot = dues_ref.get()
            dues = int(dues_snapshot.to_dict().get('잔액'))


            for row_data in selected_data:    
                # Firestore에서 해당 데이터 삭제
                # 'your_field'은 실제 사용하는 Firestore 필드명으로 변경
                for doc in documents:
                    docs = doc.to_dict()
                    in_out_data = docs.get("입/출금")
                    date_data = docs.get("날짜")
                    reason_data = docs.get("사유")
                    cash_data = int(docs.get("금액"))                

                    if (
                        row_data['입출금'] == in_out_data and 
                        row_data['날짜'] == date_data and 
                        row_data['사유'] == reason_data and 
                        int(row_data['금액']) == cash_data
                        ):
                        del_doc = doc
                        break

                if del_doc is not None:
                    del_doc_ref = doc_ref.document(del_doc.id)
                    del_doc_ref.delete()

                    if row_data['입출금'] == "입금":
                        dues = dues - int(row_data['금액'])
                    else:
                        dues = dues + int(row_data['금액'])
                dues_ref.update({'잔액': dues})

                

        # 삭제 작업이 성공했다면
            return JsonResponse({'status': 'success', 'message': '선택한 회비 내역을 성공적으로 삭제하였습니다.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

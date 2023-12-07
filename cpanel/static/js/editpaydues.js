//1, 2학기 납부내역 수정하기
function editButtonClick() {
// 각 행의 셀을 수정 가능한 Select Box로 변경
var rows = document.querySelectorAll('#payment_management_Table tbody tr')
rows.forEach(function (row) {
    var cell3 = row.querySelector('td:nth-child(3)')
    var cell4 = row.querySelector('td:nth-child(4)')
    var value1 = cell3.textContent.trim() === 'O'
    var value2 = cell4.textContent.trim() === 'O'
    var select1 = '<select class="semester-select1"><option value="true" ' + (value1 ? 'selected' : '') + '>O</option><option value="false" ' + (!value1 ? 'selected' : '') + '>X</option></select>'
    var select2 = '<select class="semester-select2"><option value="true" ' + (value2 ? 'selected' : '') + '>O</option><option value="false" ' + (!value2 ? 'selected' : '') + '>X</option></select>'
    cell3.innerHTML = select1
    cell4.innerHTML = select2
})

// 수정 버튼 숨기고 수정 완료 버튼 표시
document.getElementById('editButton').style.display = 'none'
document.getElementById('saveButton').style.display = 'inline-block'
}

function saveButtonClick() {
// 수정된 데이터 저장
var updatedData = []
var rows = document.querySelectorAll('#payment_management_Table tbody tr')
rows.forEach(function (row) {
    var studentNumber = row.querySelector('td:nth-child(1)').textContent//학번 저장
    var select1 = row.querySelector('.semester-select1:nth-child(1)')//선택된 값 저장
    var select2 = row.querySelector('.semester-select2:nth-child(1)') //선택된 값 저장
    
    var value1 = select1 ? select1.value === 'true' : false//true면 true
    var value2 = select2 ? select2.value === 'true' : false//false면 false
    
    //firestore에 전송
    updatedData.push({
        '학번': studentNumber,
        '1학기': value1,
        '2학기': value2
    })
})

//목록 수정한 거 적용
fetch('/pay_dues_edit/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken  // Django에서 CSRF 보호를 위한 토큰
    },
    body: JSON.stringify({ 'updated_data': updatedData })
})
.then(response => response.json())
.then(data => {
    console.log('서버 응답:', data)
    // 서버에서의 응답에 따른 추가 로직 수행 가능
})
.catch(error => {
    console.error('에러 발생:', error)
})

// 원래 상태로 복구
rows.forEach(function (row) {
    var cell3 = row.querySelector('td:nth-child(3)')//갖고 있는 값 가져오기
    var cell4 = row.querySelector('td:nth-child(4)')
    var value1 = cell3.querySelector('.semester-select1').value === 'true'//O이면 true, X면 false
    var value2 = cell4.querySelector('.semester-select2').value === 'true'
    cell3.innerHTML = value1 ? 'O' : 'X' //true면 'O' 띄우기, false면 'X' 띄우기
    cell4.innerHTML = value2 ? 'O' : 'X'
})

// 수정 버튼 표시하고 저장 버튼 숨기기
document.getElementById('editButton').style.display = 'inline-block'
document.getElementById('saveButton').style.display = 'none'
}

//멤버 추가 함수
function addMember() {
    var formData = new FormData(document.getElementById('memberForm'))

    //add_member주소로 members의 views 모듈 호출
    fetch('/add_member/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message)
            
            // 성공한 경우 추가적인 작업 수행
            document.getElementById('학번').value = ''
            document.getElementById('이름').value = ''
            document.getElementById('전화번호').value = ''
            document.getElementById('이메일').value = ''
            document.getElementById('직책').value = ''

            toggleFormVisibility()

            // 페이지 새로고침하여 업데이트된 멤버 목록 표시
            fetchData()

        } else {
            alert('멤버 추가에 실패했습니다: ' + data.message)
        }
    })
    .catch(error => {
        console.error('멤버 추가 중 오류 발생:', error)
    })
}

function toggleFormVisibility() {
    var form = document.getElementById('addMemberForm')
    form.style.display = form.style.display === 'none' ? 'block' : 'none'
}

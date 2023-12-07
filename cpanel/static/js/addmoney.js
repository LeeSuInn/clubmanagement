//회비 추가 함수
function addmoney() {
    var formData = new FormData(document.getElementById('moneyForm'))
    
    //add_money주소로 money의 cash 모듈 호출
    fetch('/add_money/', {
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
            
            // 성공한 경우 추가적인 작업 수행(파일 제대로 보내고 있는지 확인)
            document.getElementById('입/출금').value = ''
            document.getElementById('날짜').value = ''
            document.getElementById('사유').value = ''
            document.getElementById('금액').value = ''

            toggleFormVisibility()

            // 페이지 새로고침하여 업데이트된 멤버 목록 표시
            fetchData()

        } else {
            alert('회비 추가에 실패했습니다: ' + data.message)
        }
    })
    .catch(error => {
        console.error('멤버 추가 중 오류 발생:', error)
    })
}

function toggleFormVisibility() {
    var form = document.getElementById('addmoneyForm')
    form.style.display = form.style.display === 'none' ? 'block' : 'none'
}

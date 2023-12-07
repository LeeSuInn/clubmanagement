// 삭제 버튼을 눌렀을 때 선택한 데이터를 삭제하는 함수
function deleteSelectedMembers() {
    var selectedCheckboxes = document.querySelectorAll('.select-checkbox:checked')
    
    // 선택한 부원들의 학번을 배열에 저장
    var 학번Array = Array.from(selectedCheckboxes).map(checkbox => {
        var row = checkbox.closest('tr')
        return row.querySelector('td:nth-child(2)').textContent // 학번이 들어있는 열
    })

    // 학번이 배열에 있다면 삭제 진행
    if (학번Array.length > 0) {
        // 서버에 삭제 요청 전송
        fetch('/delete_members/', {
            method: 'POST',
            body: JSON.stringify({ '학번Array': 학번Array }), // JSON 형식으로 변경
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message)
                // 페이지 새로고침하여 업데이트된 멤버 목록 표시
                fetchData()
            } else {
                alert('멤버 삭제에 실패했습니다: ' + data.message)
            }
        })
        .catch(error => {
            console.error('멤버 삭제 중 오류 발생:', error)
        })
    } else {
        alert('선택된 학번이 없습니다.')
    }
}

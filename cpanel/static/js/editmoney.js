function getSelectedRows() {
    var selectedRows = [];
    // 모든 체크박스 요소에 대해 반복
    var checkboxes = document.querySelectorAll('.select-checkbox');
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            // 체크된 행을 배열에 추가
            var row = checkbox.closest('tr');
            selectedRows.push(row);
        }
    });
    return selectedRows;
}

function toggleEditFormVisibility() {
    var selectedRows = getSelectedRows();

    // 체크된 행이 하나일 경우에만 수정 폼 열기(하나씩 수정하기)
    if (selectedRows.length === 1) {
        editSelectedRow(selectedRows[0]);
    } else {
        // 체크된 행이 없거나 다수일 경우 경고 메시지 표시
        alert('수정할 항목을 하나만 선택하세요.');
    }
}

// 수정 폼 열기
function editSelectedRow(row) {
    // 수정 폼에 선택된 행의 데이터 표시
    document.getElementById('edit_입/출금').value = row.cells[1].textContent;
    document.getElementById('edit_날짜').value = row.cells[2].textContent;
    document.getElementById('edit_사유').value = row.cells[3].textContent;
    document.getElementById('edit_금액').value = row.cells[4].textContent;

    // 수정 폼을 보이게 설정
    var editForm = document.getElementById('editmoneyForm');
    editForm.style.display = 'block';
}
// "취소" 버튼 클릭 시 수정 폼 닫기
document.getElementById('cancelEditButton').addEventListener('click', closeEditForm);
            
function editmoney() {
    // 폼에서 수정된 회비 내역 데이터 가져오기
    var editedmoneyData = {
        입출금: document.getElementById('edit_입/출금').value,
        날짜: document.getElementById('edit_날짜').value,
        사유: document.getElementById('edit_사유').value,
        금액: document.getElementById('edit_금액').value,
        // 선택된 행의 데이터 가져오기
        selectedRowData: getSelectedRowData(),

    };
    console.log(editedmoneyData)

    // 수정된 멤버 데이터를 서버로 전송하여 처리
    fetch('/edit_money/', {
        method: 'POST',
        body: JSON.stringify(editedmoneyData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            clearEditForm();
            console.log(data)

            // 수정 폼 숨기기
            toggleEditFormVisibility();
            
            var editForm = document.getElementById('editmoneyForm');
            editForm.style.display = 'none';
            
            // 멤버 목록 새로고침
            fetchData();  // 수정 후에 데이터 다시 가져와서 화면 갱신

        } else {
            alert('회비 수정에 실패했습니다: ' + data.message);
        }
    })
    .catch(error => {
        console.error('회비 수정 중 오류 발생:', error);
    });
}

//취소하기 버튼 눌었을 때 창 닫기
function closeEditForm() {
    var editForm = document.getElementById('editmoneyForm');
    editForm.style.display = 'none';
}

// 선택된 행의 데이터를 가져오는 함수
function getSelectedRowData() {
    var selectedRows = getSelectedRows();

    if (selectedRows.length === 1) {
        // 선택된 행이 하나인 경우 해당 행의 데이터 반환
        var selectedRow = selectedRows[0];
        return {
            입출금: selectedRow.cells[1].textContent,
            날짜: selectedRow.cells[2].textContent,
            사유: selectedRow.cells[3].textContent,
            금액: selectedRow.cells[4].textContent,
        };
    }

    // 선택된 행이 없거나 다수인 경우 빈 객체 반환 또는 에러 처리
    return {};
}

// 수정 폼을 닫고 입력된 값을 초기화하는 함수
function clearEditForm() {
    document.getElementById('edit_입/출금').value = '';
    document.getElementById('edit_날짜').value = '';
    document.getElementById('edit_사유').value = '';
    document.getElementById('edit_금액').value = '';
}

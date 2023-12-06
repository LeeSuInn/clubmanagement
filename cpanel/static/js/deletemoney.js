// 선택된 행들의 데이터를 삭제하는 함수
function deleteSelectedRows() {
    var selectedRows = getSelectedRows();

    if (selectedRows.length > 0) {
        var selectedData = [];

        // 선택된 행들의 데이터를 배열에 추가
        selectedRows.forEach(row => {
            var rowData = getRowData(row);
            selectedData.push(rowData);
        });

        // 서버로 데이터 전송
        fetch('/delete_selected_rows/', {
            method: 'POST',
            body: JSON.stringify({ selectedData: selectedData }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('회비 삭제에 성공했습니다.');

                // 삭제 성공한 경우 페이지 새로고침 또는 다른 동작 수행
                fetchData();
            } else {
                alert('회비 삭제에 실패했습니다: ' + data.message);
            }
        })
        .catch(error => {
            console.error('회비 삭제 중 오류 발생:', error);
        });
    } else {
        alert('삭제할 항목을 선택하세요.');
    }
}

// 선택된 행의 데이터를 가져오는 함수
function getRowData(row) {
    return {
        입출금: row.cells[1].textContent,
        날짜: row.cells[2].textContent,
        사유: row.cells[3].textContent,
        금액: row.cells[4].textContent,
    };
}

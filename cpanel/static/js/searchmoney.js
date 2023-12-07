function searchmoneys() {
    // 검색어 가져오기
    var searchInput = document.getElementById('search-input').value.toUpperCase()

    // 테이블의 각 행에 대해 반복
    var tableRows = document.querySelectorAll('#moneyTable tbody tr')
    tableRows.forEach(row => {
        // 입/출금, 날짜, 사유 셀의 내용 가져오기
        var 입출금Cell = row.querySelector('td:nth-child(2)')
        var 날짜Cell = row.querySelector('td:nth-child(3)')
        var 사유Cell = row.querySelector('td:nth-child(4)')
        
        // 셀이 찾아진 경우에만 textContent에 접근하도록 변경
        var 입출금 = 입출금Cell ? 입출금Cell.textContent.toUpperCase() : ''
        var 날짜 = 날짜Cell ? 날짜Cell.textContent.toUpperCase() : ''
        var 사유 = 사유Cell ? 사유Cell.textContent.toUpperCase() : ''


        // 검색어와 각 셀의 내용을 비교하여 표시 여부 결정
        if (입출금.includes(searchInput) || 날짜.includes(searchInput) || 사유.includes(searchInput)) {
            row.style.display = ''  // 보이기
        } else {
            row.style.display = 'none'  // 숨기기
        }
    })
}

function toggleSearchInput() {
    var searchInput = document.getElementById('search-input')
    searchInput.style.display = searchInput.style.display === 'none' ? 'inline-block' : 'none'
    searchInput.value = '' // 입력값 초기화
    searchmoneys() // 검색창 토글시 검색 함수 호출
}

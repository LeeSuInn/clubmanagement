function searchMembers() {
    // 검색어 가져오기
    var searchInput = document.getElementById('search-input').value.toUpperCase()

    // 테이블의 각 행에 대해 반복
    var tableRows = document.querySelectorAll('#data-body tr')
    tableRows.forEach(row => {
        // 학번 및 이름 셀의 내용 가져오기
        var 학번 = row.querySelector('td:nth-child(2)').textContent.toUpperCase()
        var 이름 = row.querySelector('td:nth-child(3)'  ).textContent.toUpperCase()

        // 검색어와 학번 또는 이름을 비교하여 표시 여부 결정
        if (학번.includes(searchInput) || 이름.includes(searchInput)) {
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
    searchMembers() // 검색창 토글시 검색 함수 호출
} 

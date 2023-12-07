// 정렬 상태를 나타내는 변수 추가
var sortAscending = true

// 정렬 버튼 누를 시
$('.sortButton').on('click', function () {
    var column = $(this).data('column') // 정렬할 열
    var type = $(this).data('type') // 데이터 유형
    var order = $(this).data('order') // 정렬 순서


    // 정렬 순서 업데이트
    sortAscending = order === 'asc' ? true : false

    // 정렬 순서 업데이트
    $(this).data('order', sortAscending ? 'desc' : 'asc')
    
    sortTable(column, type, sortAscending)

    // 버튼 텍스트 업데이트
    var buttonText = sortAscending ? '▲' : '▼'
    $(this).text(column === 2 ? buttonText : buttonText)
})

// 테이블 정렬 함수
function sortTable(column, type, ascending) {
    var tbody = $('#payment_management_Table tbody')
    var rows = tbody.find('tr').toArray()

    rows.sort(function (a, b) {
        var aValue = $(a).find('td:eq(' + column + ')').text().trim()
        var bValue = $(b).find('td:eq(' + column + ')').text().trim()

        if (type === 'string') {
            return ascending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
        } else {
            return ascending ? aValue - bValue : bValue - aValue
        }
    })

    tbody.empty().append(rows)
}

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

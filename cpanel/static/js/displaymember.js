function fetchData() {
    fetch('/get_data/')  // Django 프로젝트에 맞게 URL 조정
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayData(data.data);
            } else {
                displayError(data.message);
            }
        })
        .catch(error => {
            console.error('데이터 가져오는 중 오류 발생:', error);
            displayError('데이터를 가져오는 중 오류가 발생했습니다.');
        });
}

function displayData(data) {
    var tbody = document.getElementById('data-body');

    // 표에 있는 기존 데이터를 지웁니다.
    tbody.innerHTML = '';

    // 표에 각 부원의 정보를 새로운 행으로 추가합니다.
    data.forEach(member => {
        var row = document.createElement('tr');
        row.innerHTML = `
        <td style="text-align: center;">
            <input type="checkbox" class="select-checkbox">
        </td>
        <td>${member.학번}</td>
        <td>${member.이름}</td>
        <td>${member.전화번호}</td>
        <td>${member.이메일}</td>
        <td>${member.직책}</td>
        `;
        tbody.appendChild(row);
    });
}
                
// 페이지 로드 시 fetchData 함수 호출
document.addEventListener('DOMContentLoaded', fetchData);

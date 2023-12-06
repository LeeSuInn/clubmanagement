//데이터 받아오는 함수
function fetchData() {
    fetch('/get_pay_dues__data_json/')  //json 방식으로 데이터 받아오기
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayData(data.data); //성공할 경우 데이터 출력
            } else {
            }
        })
        .catch(error => {
            console.error('데이터 가져오는 중 오류 발생:', error);
        });            
}

//받아온 데이터 출력하는 함수
function displayData(data) {
    var tbody = document.getElementById('data-body');

    // 표에 있는 기존 데이터를 지웁니다.
    tbody.innerHTML = '';

    // 표에 각 부원의 정보를 새로운 행으로 추가합니다.
    data.forEach(payment => {
        var row = document.createElement('tr');
        row.innerHTML = `
        <td>${payment.학번}</td>
        <td>${payment.이름}</td>
        <td>${payment.일학기}</td>
        <td>${payment.이학기}</td>
    `;
        tbody.appendChild(row);
    });
}
// 페이지 로드 시 fetchData 함수 호출
document.addEventListener('DOMContentLoaded', function () {
    fetchData();
})

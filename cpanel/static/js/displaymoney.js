function fetchData() {
    fetch('/financial_list/')  // Update the URL accordingly
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayData(data.data);
            }
        })   
    }
    
    function displayData(data) {
        var tbody = document.getElementById('dataBody');
        var lastBalance = null;
        var totalDeposit = 0;
        var totalWithdrawal = 0;
        
        // 표에 있는 기존 데이터를 지웁니다.
        tbody.innerHTML = '';

    data['회비 내역'].forEach(financial => {
        // 입/출금과 잔액을 숫자로 변환
        var transactionAmount = parseFloat(financial['금액']);

        var row = document.createElement('tr');
        row.innerHTML = `
            <td style="text-align: center;">
                <input type="checkbox" class="select-checkbox">
            </td>
            <td>${financial['입/출금']}</td>
            <td>${financial['날짜']}</td>
            <td>${financial['사유']}</td>
            <td>${transactionAmount}</td>
        `;
        tbody.appendChild(row);

        // 현재 행의 잔액 정보를 기록
        lastBalance = parseFloat(data['잔액']);

        // 총 입금과 출금을 누적
        if (financial['입/출금'] === '입금') {
            totalDeposit += transactionAmount;
        } else if (financial['입/출금'] === '출금') {
            totalWithdrawal += transactionAmount;
        }

    });

    // 모든 행을 추가한 이후에 한 번만 잔액 열을 추가하고 중앙 정렬
    if (lastBalance !== null) {
        var balanceRow = document.createElement('tr');
        var balanceCell = document.createElement('td');
        balanceCell.colSpan = 5; // 잔액 열이 4개의 열을 합침
        balanceCell.className = 'center-column';
        balanceCell.textContent = `총 입금: ${totalDeposit}원  |  총 출금: ${totalWithdrawal}원  |  회비 잔액: ${lastBalance}원`;
        balanceRow.appendChild(balanceCell);
        tbody.appendChild(balanceRow);
    }
}
                                                            
    // 페이지 로드 시 fetchData 함수 호출
    document.addEventListener('DOMContentLoaded', fetchData);

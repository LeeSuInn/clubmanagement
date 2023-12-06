//firebase 환경설정
const firebaseConfig = {
        apiKey: "AIzaSyCKBN_w-mQNi1B0EIvIwOghr7y5afSkIb4",
        authDomain: "club-management-system-bc814.firebaseapp.com",
        projectId: "club-management-system-bc814",
        storageBucket: "club-management-system-bc814.appspot.com",
        messagingSenderId: "99652543260",
        appId: "1:99652543260:web:d17e2bb697763a947950d9",
        measurementId: "G-Z5R49455MZ",    
        databaseURL: "https://club-management-system-bc814-default-rtdb.firebaseio.com/"
};
//firebase 초기화
firebase.initializeApp(firebaseConfig);
  
// Firestore 초기화
const db = firebase.firestore();

//달력, 선택된 날짜 전역 변수 지정
var calendar;
var selectedDate;

//페이지 로드 시 달력, 일정 정보 출력
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        events:[],
        height: 550,  // 높이 지정


        dateClick: function(info) {
            console.log("Clicked event occurs: data = " + info.dateStr);

            // 현재 클릭된 날짜와 선택된 날짜가 다르면 스타일 초기화
            if (selectedDate !== info.dateStr) {
                resetSelectedDateStyle();
            }

            selectedDate = info.dateStr;

            // 선택된 날짜에 스타일 적용
            info.dayEl.classList.add('selected-date');

            // 선택된 날짜의 Todo 리스트를 불러옴
            loadTodoListFromFirestore(selectedDate);  // 페이지 로드 시 Firestore 데이터를 가져와서 표시
        }
    });

    // "일정 삭제" 버튼에 대한 이벤트 리스너 추가
    const deleteEventsBtn = document.getElementById('delete-events-btn');
    deleteEventsBtn.addEventListener('click', deleteEventsForSelectedDate);

    //firestore에서 데이터 로드 후 달력과 일정 출력
    loadAllTodoListsFromFirestore()
    calendar.render()
});

//to do 리스트 만들기
const todoform = document.querySelector("#todoform")
const todoInput = document.querySelector("#todoform input")
const todoList_ul = document.querySelector("#todolist")

// 각 날짜별 Todo 리스트를 관리하는 객체
const todoLists = {};

//제출 시 함수
function handleFormSubmit(event) {
    event.preventDefault(); //기본 동작 방지

    //입력 받은 일정 저장
    const curTodo = todoInput.value;

    //저장 후 초기화
    todoInput.value = "";

    //출력 폼 변수
    const todo_cur_li = document.createElement("li");
    const checkbox = document.createElement("input");
    const todo_cur_span = document.createElement("span");

    //todo 리스트 출력 내용
    checkbox.type = "checkbox";
    checkbox.className = "todo-checkbox";
    todo_cur_span.innerText = curTodo;

    todo_cur_li.appendChild(checkbox);
    todo_cur_li.appendChild(todo_cur_span);
    todoList_ul.appendChild(todo_cur_li);

    // 캘린더에도 일정 추가
    if (selectedDate && curTodo) {
        if (!todoLists[selectedDate]) {
            todoLists[selectedDate] = [];
        }
        //todo 리스트에 추가
        todoLists[selectedDate].push(curTodo);

        // FullCalendar에 이벤트 추가
        const newEvent = {
            title: curTodo,
            start: selectedDate,
            id: selectedDate,
        };

        calendar.addEvent(newEvent)

        // 일정 추가 후에 선택된 날짜의 스타일을 초기화
        resetSelectedDateStyle();
    }

    // firstore에 데이터 저장
    saveTodoListToFirestore();
}

todoform.addEventListener("submit", handleFormSubmit);

// 선택된 날짜의 스타일을 초기화하는 함수
function resetSelectedDateStyle() {
    const selectedDateElement = document.querySelector('.selected-date');
    if (selectedDateElement) {
        selectedDateElement.classList.remove('selected-date');
    }
}

// Firestore에 Todo 리스트 저장
function saveTodoListToFirestore() {
    if (selectedDate && todoLists[selectedDate]) {
        db.collection(uid).doc('동아리').collection('일정').doc(selectedDate).set({
        todos: todoLists[selectedDate]
    });
    }
}

// Firestore에서 Todo 리스트 불러오기
function loadTodoListFromFirestore(date) {
    if (selectedDate) {
        const docRef = db.collection(uid).doc('동아리').collection('일정').doc(date)

        // Firestore의 데이터가 변경될 때 감지하는 이벤트
        docRef.get().then((doc) => {
            if (doc.exists) {
                // Firestore에서 Todo 리스트를 불러오고 화면에 표시
                const todosData = doc.data();
                const todoList_ul = document.getElementById('todolist');
                todoList_ul.innerHTML = "";

                todosData.todos.forEach(todo => {
                    const todo_cur_li = document.createElement("li");
                    const checkbox = document.createElement("input");
                    const todo_cur_span = document.createElement("span");
                    
                    checkbox.type = "checkbox";
                    checkbox.className = "todo-checkbox";    
                    todo_cur_span.innerText = todo;

                    todo_cur_li.appendChild(checkbox);
                    todo_cur_li.appendChild(todo_cur_span);
                    todoList_ul.appendChild(todo_cur_li);
                });

                // FullCalendar의 이벤트를 업데이트
                updateFullCalendarEvents(selectedDate, todosData.todos);
                todoLists[selectedDate] = todosData.todos;
                saveTodoListToFirestore()
                loadAllTodoListsFromFirestore()
            } 
            //해당 날짜에 일정이 없을 시 초기화
            else{
                todoList_ul.innerHTML = "";
            }
        });
    }
}

// Firestore에서 모든 Todo 리스트 불러오기
function loadAllTodoListsFromFirestore() {
    db.collection(uid).doc('동아리').collection('일정').get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
            // 각 문서의 데이터를 가져와서 달력에 표시
            const date = doc.id;
            const todosData = doc.data();
            const todos = todosData.todos;

            // 선택된 날짜가 있을 때와 없을 때를 구분하여 처리
            if (selectedDate) {
                // 선택된 날짜가 있는 경우
                if (date !== selectedDate) {
                    // 선택된 날짜와 동일하지 않은 경우에만 FullCalendar에 이벤트 추가
                    todos.forEach((todo) => {
                        const newEvent = {
                            title: todo,
                            start: date,
                            id: date + '_' + todo  // 각 이벤트에 고유한 ID를 부여
                        };
                        calendar.addEvent(newEvent)
                    });
                }
            } else {
                // 선택된 날짜가 없는 경우 모든 날짜의 이벤트를 추가
                todos.forEach((todo) => {
                    const newEvent = {
                        title: todo,
                        start: date,
                        id: date + '_' + todo  // 각 이벤트에 고유한 ID를 부여
                    };
                    calendar.addEvent(newEvent)
                });
            }
        // todoLists 객체 업데이트
        todoLists[date] = todos;
        });
    }).catch((error) => {
        console.error("Error getting documents: ", error);
    });
}

// FullCalendar의 이벤트를 업데이트하는 함수
function updateFullCalendarEvents(date, todos) {
    // 현재 선택된 날짜의 모든 이벤트 초기화
    calendar.getEvents().forEach((existingEvent) => {
        existingEvent.remove();
    });

    // 새로운 이벤트를 추가
    todos.forEach((todo) => {
        const newEvent = {
            title: todo,
            start: date,
            id: date + '_' + todo  // 각 이벤트에 고유한 ID를 부여
        };
        calendar.addEvent(newEvent);
    });
}

//선택한 날짜의 일정을 삭제하는 함수
function deleteEventsForSelectedDate() {
    const checkedCheckboxes = document.querySelectorAll("#todolist li input.todo-checkbox:checked");

     // Check if any checkboxes are checked
    if (checkedCheckboxes.length === 0) {
        alert("삭제할 일정을 선택해주세요.");
        return;
    }
    //선택한 데이터 확인
    checkedCheckboxes.forEach((checkbox) => {
        const todoItem = checkbox.closest("li");
        const todoText = todoItem.querySelector("span").innerText;

        // 선택된 날짜와 Todo를 Todo 리스트에서 제거
        const todoIndex = todoLists[selectedDate].indexOf(todoText);
        if (todoIndex !== -1) {
            todoLists[selectedDate].splice(todoIndex, 1);
        }

        // FullCalendar에서 이벤트 업데이트
        updateFullCalendarEvents(selectedDate, todoLists[selectedDate]);

        // 화면에서 선택된 Todo 삭제
        todoItem.remove();
        alert("일정을 삭제하였습니다.");
    });
    
    // Firestore에 변경된 Todo 리스트 저장
    saveTodoListToFirestore();
    
    // 해당 날짜의 todolists가 비어 있다면 Firestore에서 해당 날짜의 문서를 삭제
    if (todoLists[selectedDate].length === 0) {
        deleteTodoListFromFirestore(selectedDate);
    }
    
    loadAllTodoListsFromFirestore();
    
    // Firestore에서 특정 날짜의 Todo 리스트를 삭제하는 함수
    function deleteTodoListFromFirestore(date) {
        db.collection(uid).doc('동아리').collection('일정').doc(date).delete()
        .catch((error) => {
            alert("일정을 삭제하지 못했습니다.: ", error);
        });
    }
}
            

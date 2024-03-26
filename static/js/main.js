document.addEventListener('DOMContentLoaded', function () {
    fetchPositions();
    fetchEmployees();
    document.getElementById('add-position-form').addEventListener('submit', addPosition);
    document.getElementById('add-employee-form').addEventListener('submit', addEmployee);
});

function fetchPositions() {
    axios.get('/positions/')
        .then(function (response) {
            const positionsList = document.getElementById('positions-list');
            const employeePositionSelect = document.getElementById('employee-position');
            positionsList.innerHTML = '';
            employeePositionSelect.innerHTML = '';
            response.data.forEach(function (position) {
                // Добавляем каждую должность в список
                const positionElement = document.createElement('div');
                positionElement.innerHTML = `
                <p>${position.name} (${position.category}) 
                    <button onclick="editPosition(${position.id})">Редактировать</button>
                    <button onclick="deletePosition(${position.id})">Удалить</button>
                </p>`;
                positionsList.appendChild(positionElement);

                // Добавляем каждую должность в выпадающий список для формы добавления сотрудника
                const option = document.createElement('option');
                option.value = position.id;
                option.textContent = `${position.name} (${position.category})`;
                employeePositionSelect.appendChild(option);
            });
        })
        .catch(function (error) {
            console.error('Error fetching positions:', error);
        });
}


function fetchEmployees() {
    axios.get('/employees/')
        .then(function (response) {
            const employeesList = document.getElementById('employees-list');
            employeesList.innerHTML = '';
            response.data.forEach(function (employee) {
                const employeeElement = document.createElement('div');
                employeeElement.innerHTML = `
                    <p>${employee.full_name} (${employee.gender}, ${employee.age} лет) - ${employee.position} (${employee.category}) 
                        <button onclick="editEmployee(${employee.id})">Редактировать</button>
                        <button onclick="deleteEmployee(${employee.id})">Удалить</button>
                    </p>`;
                employeesList.appendChild(employeeElement);
            });
        })
        .catch(function (error) {
            console.error('Error fetching employees:', error);
        });
}

function addPosition(event) {
    event.preventDefault();
    const name = document.getElementById('position-name').value;
    const category = document.getElementById('position-category').value;
    const csrftoken = getCookie('csrftoken');
    axios.post('/positions/add/', { name, category }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(function (response) {
            fetchPositions();
        })
        .catch(function (error) {
            console.error('Error adding position:', error);
        });
}

function deletePosition(positionId) {
    const csrftoken = getCookie('csrftoken');
    axios.delete(`/positions/${positionId}/delete/`, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(function (response) {
            fetchPositions();
        })
        .catch(function (error) {
            console.error('Error deleting position:', error);
        });
}


function editPosition(positionId) {
    window.location.href = `/positions/${positionId}/edit/`;
}

function addEmployee(event) {
    event.preventDefault();
    const full_name = document.getElementById('employee-name').value;
    const gender = document.getElementById('employee-gender').value;
    const age = document.getElementById('employee-age').value;
    const position_id = document.getElementById('employee-position').value;
    const csrftoken = getCookie('csrftoken');
    axios.post('/employees/add/', { full_name, gender, age, position_id }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(function (response) {
            fetchEmployees();
        })
        .catch(function (error) {
            console.error('Error adding employee:', error);
        });
}

function deleteEmployee(employeeId) {
    const csrftoken = getCookie('csrftoken');
    axios.delete(`/employees/${employeeId}/delete/`, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(function (response) {
            fetchEmployees();
        })
        .catch(function (error) {
            console.error('Error deleting employee:', error);
        });
}

function editEmployee(employeeId) {
    window.location.href = `/employees/${employeeId}/edit/`;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

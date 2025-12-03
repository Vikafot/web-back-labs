// === Заполнение таблицы фильмами ===
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (response) {
            return response.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // Заполнение ячеек
                tdTitle.innerText = films[i].title === films[i].title_ru ? '' : films[i].title;
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;

                // Кнопка "редактировать"
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    editFilm(i);
                };

                // Кнопка "удалить"
                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteFilm(i, films[i].title_ru);
                };

                // Сборка строки
                tdActions.appendChild(editButton);
                tdActions.appendChild(delButton);

                tr.appendChild(tdTitle);
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);
            }
        })
        .catch(function (error) {
            console.error('Ошибка при загрузке списка фильмов:', error);
        });
}

// === Удаление фильма ===
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(function () {
        fillFilmList(); // Обновляем таблицу после удаления
    })
    .catch(function (error) {
        console.error('Ошибка при удалении фильма:', error);
    });
}

// === Редактирование фильма (заглушка для раздела 9) ===
function editFilm(id) {
    alert('Редактирование фильма с id = ' + id + ' (будет реализовано в разделе 11)');
}
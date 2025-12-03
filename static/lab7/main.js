function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            films.forEach((film, index) => {
                const tr = document.createElement('tr');

                const tdTitle = document.createElement('td');
                const tdTitleRus = document.createElement('td');
                const tdYear = document.createElement('td');
                const tdActions = document.createElement('td');

                tdTitle.innerText = film.title === film.title_ru ? '' : film.title;
                tdTitleRus.innerText = film.title_ru;
                tdYear.innerText = film.year;

                const delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = () => deleteFilm(index, film.title_ru);

                tdActions.appendChild(editButton);
                tdActions.appendChild(delButton);

                tr.appendChild(tdTitle);
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке списка фильмов:', error);
        });
}

function deleteFilm(index, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${index}`, {
        method: 'DELETE'
    })
    .then(() => {
        fillFilmList();
    })
    .catch(error => {
        console.error('Ошибка при удалении фильма:', error);
    });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value.trim()
    };

    if (!film.title_ru || !film.year) {
        alert('Пожалуйста, заполните обязательные поля: название на русском и год.');
        return;
    }

    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при сохранении фильма');
        }
        return response;
    })
    .then(() => {
        hideModal();
        fillFilmList();
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Не удалось сохранить фильм. Проверьте данные.');
    });
}
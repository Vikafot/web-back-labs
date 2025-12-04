function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            films.forEach((film, index) => {
                const tr = document.createElement('tr');

                const tdTitleRus = document.createElement('td');
                const tdTitleOrig = document.createElement('td');
                const tdYear = document.createElement('td');
                const tdActions = document.createElement('td');

                tdTitleRus.innerText = film.title_ru;

                if (film.title && film.title !== film.title_ru) {
                    tdTitleOrig.innerHTML = `<em>(${film.title})</em>`;
                } else {
                    tdTitleOrig.innerText = '';
                }

                tdYear.innerText = film.year;

                const editBtn = document.createElement('button');
                editBtn.innerText = 'редактировать';
                editBtn.onclick = () => editFilm(index);

                const delBtn = document.createElement('button');
                delBtn.innerText = 'удалить';
                delBtn.onclick = () => deleteFilm(index, film.title_ru);

                tdActions.appendChild(editBtn);
                tdActions.appendChild(delBtn);

                tr.appendChild(tdTitleRus);
                tr.appendChild(tdTitleOrig);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);
            });
        })
        .catch(err => console.error('Ошибка загрузки фильмов:', err));
}

function deleteFilm(index, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`/lab7/rest-api/films/${index}`, { method: 'DELETE' })
        .then(() => fillFilmList())
        .catch(err => console.error('Ошибка удаления:', err));
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function editFilm(index) {
    fetch(`/lab7/rest-api/films/${index}`)
        .then(response => response.json())
        .then(film => {
            document.getElementById('id').value = index;
            document.getElementById('title-ru').value = film.title_ru || '';
            document.getElementById('title').value = film.title || '';
            document.getElementById('year').value = film.year || '';
            document.getElementById('description').value = film.description || '';
            showModal();
        })
        .catch(err => {
            alert('Не удалось загрузить данные фильма.');
            console.error(err);
        });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title_ru: document.getElementById('title-ru').value.trim(),
        title: document.getElementById('title').value.trim(),
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value.trim()
    };

    if (!film.title_ru || isNaN(film.year) || film.year < 1895 || film.year > 2025) {
        alert('Проверьте: русское название обязательно, год — от 1895 до 2025.');
        return;
    }
    if (!film.description) {
        document.getElementById('description-error').innerText = 'Заполните описание';
        return;
    }

    document.getElementById('description-error').innerText = '';

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}/`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (response.ok) {
            return {};
        }
        return response.json().catch(() => ({ description: 'Неизвестная ошибка сервера' }));
    })
    .then(data => {
        if (data && (data.description || data.title_ru || data.year)) {
            const msg = data.description || data.title_ru || data.year || 'Ошибка ввода';
            document.getElementById('description-error').innerText = msg;
        } else {
            hideModal();
            fillFilmList();
        }
    })
    .catch(err => {
        console.error('Ошибка отправки:', err);
        document.getElementById('description-error').innerText = 'Не удалось связаться с сервером.';
    });
}
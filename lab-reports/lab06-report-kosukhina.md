# Звіт до лабораторної роботи №6
**Виконала:** Олександра Косухіна  
**Тема:** Інтеграція REST API та асинхронний JavaScript (Fetch, Async/Await)  
**Роль у команді:** Учасник 3 (JavaScript-логіка, fetch, async/await, валідація та обробка помилок)

---

### 1. Мета роботи
Реалізувати клієнтську логіку на JavaScript для взаємодії з бекенд-API за допомогою сучасних асинхронних запитів (`fetch`, `async/await`), налаштувати безпечний рендер даних, валідацію форм та обробку мережевих помилок.

---

### 2. Виконані завдання (Учасник 3)

1. **Отримання та рендер даних (GET-запит):**
   * Створено файл `static/api-demo.js`.
   * Реалізовано асинхронну функцію `fetchData()`, яка завантажує список записів із сервера при завантаженні сторінки.
   * Забезпечено безпечний вивід даних за допомогою `textContent` (захист від XSS-атак).
   * Додано індикатор завантаження (`#loading`), який відображається під час запиту та ховається після його завершення.

2. **Створення записів (POST-запит):**
   * Налаштовано обробник події `submit` для форми додавання (`#addForm`).
   * Реалізовано відправку даних на сервер у форматі JSON з заголовком `Content-Type: application/json`.
   * Після успішного додавання форма автоматично очищається, а список записів оновлюється без перезавантаження сторінки.

3. **Валідація та обробка помилок:**
   * Додано перевірку полів форми на клієнті перед відправкою (заборона надсилання порожніх значень).
   * Реалізовано перевірку статусу відповіді (`response.ok`) та обробку винятків у блоці `try...catch` на випадок недоступності сервера чи помилок валідації.

---

### 3. Лістинг розробленого коду (`static/api-demo.js`)

```javascript
document.addEventListener('DOMContentLoaded', () => {
    fetchData();

    const addForm = document.getElementById('addForm');
    if (addForm) {
        addForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const messageBox = document.getElementById('message');
            const nameInput = document.getElementById('itemName'); 
            const descInput = document.getElementById('itemDescription');

            const name = nameInput ? nameInput.value.trim() : '';
            const description = descInput ? descInput.value.trim() : '';

            if (!name) {
                if (messageBox) {
                    messageBox.className = 'error';
                    messageBox.textContent = 'Будь ласка, заповніть обов\'язкове поле!';
                }
                return;
            }

            const requestData = { name, description };

            try {
                const response = await fetch('/api/v1/items', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.message || `Помилка сервера: ${response.status}`);
                }

                if (messageBox) {
                    messageBox.className = 'success';
                    messageBox.textContent = 'Запис успішно додано!';
                }

                addForm.reset();
                await fetchData();

            } catch (error) {
                console.error('Помилка при додаванні:', error);
                if (messageBox) {
                    messageBox.className = 'error';
                    messageBox.textContent = `Не вдалося додати запис: ${error.message}`;
                }
            }
        });
    }
});

async function fetchData() {
    const dataList = document.getElementById('dataList');
    const loading = document.getElementById('loading');
    const messageBox = document.getElementById('message');

    if (loading) loading.style.display = 'block';
    if (messageBox) messageBox.textContent = '';

    try {
        const response = await fetch('/api/v1/items');
        if (!response.ok) throw new Error(`Помилка сервера: ${response.status}`);

        const data = await response.json();
        dataList.innerHTML = '';

        if (data.length === 0) {
            dataList.innerHTML = '<p>Список поки що порожній.</p>';
            return;
        }

        data.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'item-card';
            
            const title = document.createElement('h3');
            title.textContent = item.name || 'Без назви';
            
            const desc = document.createElement('p');
            desc.textContent = item.description || '';

            itemElement.appendChild(title);
            itemElement.appendChild(desc);
            dataList.appendChild(itemElement);
        });

    } catch (error) {
        console.error('Помилка завантаження:', error);
        if (messageBox) {
            messageBox.className = 'error';
            messageBox.textContent = 'Не вдалося завантажити дані. Перевірте з’єднання з сервером.';
        }
    } finally {
        if (loading) loading.style.display = 'none';
    }
}
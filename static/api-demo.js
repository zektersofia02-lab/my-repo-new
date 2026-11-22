document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

// Функція для завантаження та відображення даних
async function fetchData() {
    const dataList = document.getElementById('dataList');
    const loading = document.getElementById('loading');
    const messageBox = document.getElementById('message');

    // Показуємо індикатор завантаження
    if (loading) loading.style.display = 'block';
    if (messageBox) messageBox.textContent = '';

    try {
        const response = await fetch('/api/v1/items'); // Заміни шлях, якщо Учасник 1 дав інший
        
        if (!response.ok) {
            throw new Error(`Помилка сервера: ${response.status}`);
        }

        const data = await response.json();
        
        // Очищаємо список перед рендером
        dataList.innerHTML = '';

        // Перевіряємо, чи є дані
        if (data.length === 0) {
            dataList.innerHTML = '<p>Список поки що порожній.</p>';
            return;
        }

        // Рендеримо кожен елемент
        data.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'item-card'; // Можеш змінити клас під стилі Учасника 2
            
            // Безпечне додавання через textContent
            const title = document.createElement('h3');
            title.textContent = item.name || 'Без назви'; // Заміни 'name' на поле твого ресурсу
            
            const desc = document.createElement('p');
            desc.textContent = item.description || ''; // Заміни 'description' на своє поле

            itemElement.appendChild(title);
            itemElement.appendChild(desc);
            dataList.appendChild(itemElement);
        });

    } catch (error) {
        console.error('Помилка завантаження:', error);
        if (messageBox) {
            messageBox.className = 'error'; // Клас для стилізації помилки
            messageBox.textContent = 'Не вдалося завантажити дані. Перевірте з’єднання з сервером.';
        }
    } finally {
        // Ховаємо індикатор завантаження
        if (loading) loading.style.display = 'none';
    }
}
// Обробка відправки форми (POST-запит)
document.addEventListener('DOMContentLoaded', () => {
    const addForm = document.getElementById('addForm');
    
    if (addForm) {
        addForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Зупиняємо стандартну перезавантажувальну поведінку форми

            const messageBox = document.getElementById('message');
            
            // Збираємо дані з полів форми (заміни 'name' та 'description' на реальні id твоїх інпутів)
            const nameInput = document.getElementById('itemName'); 
            const descInput = document.getElementById('itemDescription');

            const name = nameInput ? nameInput.value.trim() : '';
            const description = descInput ? descInput.value.trim() : '';

            // 1. Проста валідація на клієнті
            if (!name) {
                if (messageBox) {
                    messageBox.className = 'error';
                    messageBox.textContent = 'Будь ласка, заповніть обов\'язкове поле (назву)!';
                }
                return;
            }

            // Формуємо об'єкт для відправки
            const requestData = {
                name: name,
                description: description
            };

            try {
                // Відправляємо POST-запит
                const response = await fetch('/api/v1/items', { // Заміни шлях під свій бекенд, якщо потрібно
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.message || `Помилка сервера: ${response.status}`);
                }

                // Успіх!
                if (messageBox) {
                    messageBox.className = 'success';
                    messageBox.textContent = 'Запис успішно додано!';
                }

                // Очищаємо форму
                addForm.reset();

                // Оновлюємо список даних на сторінці
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
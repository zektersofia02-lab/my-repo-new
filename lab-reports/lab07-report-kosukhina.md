# Звіт до лабораторної роботи №7 — Учасник 3 (Інтеграційні тести API)

## 1. Мета роботи
Реалізація інтеграційних тестів для REST API ендпоінтів вебзастосунку з використанням фреймворку `pytest`, тестового клієнта Flask (`client`) та ізольованого середовища бази даних за схемою **AAA (Arrange, Act, Assert)**.

---

## 2. Опис виконаних завдань (Крок 3)
У межах командної роботи я відповідала за написання інтеграційних тестів для API-ендпоінтів (`/api/v1/products`). Було реалізовано 4 ключові сценарії (успішні та помилкові):
1. **Отримання списку товарів/послуг** — перевірка успішного запиту (`GET`, статус `200 OK`).
2. **Створення нового товару/послуги** — перевірка валідного додавання даних (`POST`, статус `201 Created`).
3. **Обробка некоректних даних** — перевірка негативного сценарію при відсутності обов'язкових полів (`POST`, статус `400 Bad Request`).
4. **Запит неіснуючого ресурсу** — перевірка обробки помилки, коли запису з таким ID немає в базі (`GET`, статус `404 Not Found`).

---

## 3. Лістинг розробленого коду (`tests/test_api.py`)

```python
def test_get_products_success(client):
    # Arrange: клієнт та тестова база готові через фікстуру
    
    # Act: отримуємо список усіх товарів/послуг
    response = client.get('/api/v1/products')

    # Assert: перевіряємо успішний статус 200 та тип даних (список)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_product_success(client):
    # Arrange: готуємо коректні дані для нового товару
    new_product = {
        "title": "Тестова послуга",
        "price": 1500,
        "description": "Тестовий опис"
    }

    # Act: надсилаємо POST-запит для створення запису
    response = client.post('/api/v1/products', json=new_product)

    # Assert: перевіряємо статус 201 (створено) та збережені поля
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Тестова послуга"
    assert data["price"] == 1500


def test_create_product_bad_request(client):
    # Arrange: готуємо некоректні дані (немає обов'язкових полів)
    invalid_product = {
        "title": ""
    }

    # Act: намагаємося створити товар із невалідними даними
    response = client.post('/api/v1/products', json=invalid_product)

    # Assert: сервер має повернути помилку 400 Bad Request
    assert response.status_code == 400


def test_get_product_not_found(client):
    # Arrange: задаємо ID товару, якого точно немає в базі
    non_existent_id = 99999

    # Act: намагаємося отримати неіснуючий товар
    response = client.get(f'/api/v1/products/{non_existent_id}')

    # Assert: сервер має повернути помилку 404 Not Found
    assert response.status_code == 404
🚀 Командний вебпроєкт на Flask
Сучасний багатосторінковий вебзастосунок, розроблений командою студентів із використанням Python Flask, Jinja2 та Tailwind CSS.
👥 Склад команди та ролі
Зектер Софія (Тімлід / DevOps): Налаштування репозиторія, архітектура застосунку (app.py), базовий шаблон (templates/base.html), головна сторінка (templates/index.html).
Шабат Анна (Backend & Content): Розробка маршрутів та внутрішніх сторінок «Про нас» (templates/about.html) і «Послуги» (templates/services.html).
Косухіна Олександра (Frontend & UI/UX): Розробка маршрутів, сторінка «Контакти» (templates/contact.html), налаштування стилів та адаптивність інтерфейсу.
Головачук Дарина (QA & Documentation Engineer): Повне тестування системи, перевірка навігації та адаптивності, координація GitHub Issues, складання документації (README.md) та звітів.
🛠 Технологічний стек
Backend: Python 3.x, Flask
Templating: Jinja2
Frontend / UI: HTML5, CSS3, Tailwind CSS
VCS / Tools: Git, GitHub, VS Code
⚙️ Інструкція з встановлення та запуску
1. Клонування репозиторію
git clone <посилання-на-репозиторій>
cd <назва-папки># my-repo-new

## REST API та документація Swagger (Flasgger)

Для проєкту реалізовано версіонований REST API на Flask Blueprints (`/api/v1` та `/api/v2`) із роботою через SQLite, а також інтерактивну документацію на базі **Flasgger** (Swagger UI).

### Доступ до документації
Після запуску сервера (`python app.py`) документація доступна за адресою:
- `http://127.0.0.1:5000/apidocs/`

---

### Маршрути API v1 (`/api/v1`)

#### Товари та послуги (`products`)
- `GET /api/v1/products` — отримати список усіх товарів/послуг (`200`)
- `GET /api/v1/products/<int:product_id>` — отримати товар/послугу за ID (`200`, `404`)
- `POST /api/v1/products` — створити новий товар/послугу (`201`, `400`)
- `PUT` / `PATCH /api/v1/products/<int:product_id>` — оновити товар/послугу за ID (`200`, `404`)
- `DELETE /api/v1/products/<int:product_id>` — видалити товар/послугу за ID (`204`, `404`)

#### Замовлення (`orders`)
- `GET /api/v1/orders` — отримати список усіх замовлень (`200`)
- `GET /api/v1/orders/<int:order_id>` — отримати замовлення за ID (`200`, `404`)
- `POST /api/v1/orders` — створити нове замовлення (`201`, `400`, `404`)
- `PUT` / `PATCH /api/v1/orders/<int:order_id>` — оновити замовлення за ID (`200`, `404`)
- `DELETE /api/v1/orders/<int:order_id>` — видалити замовлення за ID (`204`, `404`)

---

### Маршрути API v2 (`/api/v2`)

#### Товари та послуги (`products`)
- `GET /api/v2/products` — отримати список товарів/послуг із метаданими (`api_version`, `count`, `products`) (`200`)
- `GET /api/v2/products/<int:product_id>` — отримати товар/послугу за ID у форматі v2 (`200`, `404`)
- `POST /api/v2/products` — створити товар/послугу у форматі v2 (`201`, `400`)
- `PUT` / `PATCH /api/v2/products/<int:product_id>` — оновити товар/послугу у форматі v2 (`200`, `400`, `404`)
- `DELETE /api/v2/products/<int:product_id>` — видалити товар/послугу (`204`, `404`)

#### Замовлення (`orders`)
- `GET /api/v2/orders` — отримати список замовлень із метаданими (`api_version`, `count`, `orders`) (`200`)
- `GET /api/v2/orders/<int:order_id>` — отримати замовлення за ID у форматі v2 (`200`, `404`)
- `POST /api/v2/orders` — створити замовлення у форматі v2 (`201`, `400`)
- `PATCH /api/v2/orders/<int:order_id>` — оновити статус замовлення (`200`, `400`, `404`)
- `DELETE /api/v2/orders/<int:order_id>` — видалити замовлення (`204`, `404`)

---

### Перевірка API
Роботу документації та маршрутів перевірено через Swagger UI (`/apidocs/`). Наприклад, запит `GET /api/v1/orders` повертає статус `200` та JSON зі списком замовлень:

```json
[
  {
    "id": 1,
    "product_id": 2,
    "status": "Новий"
  }
]
## Інтеграція фронтенду `/api-demo`

Сторінка **`/api-demo`** інтегрована з бекенд-ендпоінтом `POST /api/v1/products` та `GET /api/v1/products`:
* **HTML-шаблон:** `templates/api-demo.html`
* **Клієнтський скрипт:** `static/api-demo.js`
* **Формат тіла запиту (`POST /api/v1/products`):**
  ```json
  {
    "title": "Назва послуги або товару",
    "price": 100,
    "description": "Опис (опціонально)"
  }
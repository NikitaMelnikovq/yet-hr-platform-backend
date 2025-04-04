# HR Backend для компании УЭТ

## 📖 Описание проекта

Backend для HR-платформы компании УЭТ. Реализует ...

---

## 🛠️ Стек технологий

- `Python` 3.12+
- `Django` 5.0+
- `PostgreSQL` 16+
- `Docker` и `Docker Compose`

---

## 🚀 Возможности системы

- [x] Авторизация и аутентификация пользователей
- [x] Редактирование/удалени/добавление вакансикй

---

## ⚙️ Запуск проекта

### 1️⃣ Клонируй репозиторий:

```bash
git clone https://github.com/company-uet/hr-backend.git
cd hr-backend
```

### 2️⃣ Настрой переменные окружения:

Создай файл `.env` в корне проекта и заполни его:

```env
SECRET_KEY=твой_секретный_ключ
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=твой_пароль
DB_HOST=db
DB_PORT=5432
```

### 3️⃣ Запусти проект через Docker:

```bash
docker-compose build
docker-compose up -d
```

**Приложение доступно:**  
👉 [http://localhost:8000](http://localhost:8000)

---

## 📦 Работа с базой данных

Запусти миграции:

```bash
docker-compose exec web python manage.py migrate
```

Создай суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 🧪 Запуск тестов

```bash
docker-compose exec web python manage.py test
```

---

## 📁 Структура проекта

```
hr-backend/
├── hr_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── auth_system/  # Авторизация и аутентификация
├── vacancies/  # Вакансии
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## 📚 Документация API

Swagger-документация доступна по адресу:

[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 📬 Контакты

- Разработчик: Мельников Никита
- Email: nikitamelnikov502@gmail.com

---

© 2025 УЭТ. Все права защищены.
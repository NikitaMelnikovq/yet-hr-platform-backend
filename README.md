# HR Backend для компании УЭТ

## 📖 Описание проекта

Backend для HR-платформы компании УЭТ реализует RESTful API для управления вакансиями с системой фильтрации, обработки обратной связи от кандидатов и интеграции с социальными сетями. Он обеспечивает работу страниц компании с информацией о корпоративной культуре, преимуществах работы и успехах организации, а также поддерживает блог. Разработанный на Django REST Framework с использованием PostgreSQL, backend обеспечивает безопасное хранение данных, высокую производительность и масштабируемость для эффективного взаимодействия HR-отдела с молодыми специалистами.

---

## 🛠️ Стек технологий

- `Python` 3.12+
- `Django` 5.0+
- `PostgreSQL` 16+
- `Docker` и `Docker Compose`

## ⚙️ Запуск проекта

### 1️⃣ Клонируй репозиторий:

```bash
git clone https://github.com/NikitaMelnikovq/yet-hr-platform-backend.git
cd yet-hr-platform-backend
git clone https://github.com/acuraels/yet-hr-platform-frontend.git
```

### 2️⃣ Настрой переменные окружения:

Создай файл `.env` в корне проекта и заполни его:

```env
SECRET_KEY=твой_секретный_ключ
DEBUG=True
POSTGRES_DB=hr_pl
POSTGRES_USER=postgres
POSTGRES_PASSWORD=твой_пароль
```

### 3️⃣ Запусти проект через Docker (Linux):

```bash
sudo docker compose -f docker-compose.dev.yml build
sudo docker compose -f docker-compose.dev.yml up
```

**Приложение доступно:**  
👉 [http://localhost:8000](http://localhost:8000)

---

## 📦 Работа с приложением

Добавь свой айпи в CORS_ALLOWED_ORIGINS, чтобы избежать ошибки CORS blocked:

Создай суперпользователя:

```bash
sudo docker exec -it yet-hr-platform-backend-backend-1 bash
python3 manage.py createsuperuser
```

---

## 📁 Структура проекта

```
hr/
├── hr/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
├── blog/
├── media/
├── vacancies/
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## 📚 Документация API

Swagger-документация доступна по адресу:

[http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## 📬 Контакты

- Разработчик: Мельников Никита
- Email: nikitamelnikov502@gmail.com

---

© 2025 УЭТ. Все права защищены.

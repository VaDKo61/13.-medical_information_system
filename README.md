# 🏥 Medical Information System

**Medical Information System (MIS)** — это простой веб-сервис, имитирующий работу медицинской информационной системы.

---

## 🚀 Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/VaDKo61/13.-medical_information_system
```
```bash
cd 13.-medical_information_system
```

---

### 2. Запустить проект в Docker
```bash
docker compose up --build
```

---

### 3. Выполнить миграции базы данных
```bash
docker compose exec web python manage.py migrate
```

---

### 4. Создать суперпользователя
```bash
docker compose exec web python manage.py createsuperuser
```

---

### 5. Открыть админ-панель
🔗 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

### 6. Документация API (Swagger)
📄 [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## 🧪 Запуск тестов
```bash
docker compose exec web pytest
```

---

## 📌 Технологии
- Python 3 / Django
- PostgreSQL
- Docker & Docker Compose
- Swagger (OpenAPI)
- Pytest

---
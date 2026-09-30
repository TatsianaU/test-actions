# Server Time API

Простой тестовый бэкенд на FastAPI. Возвращает текущие время и дату сервера.

## Запуск

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn main:app --reload
```

Сервер слушает http://127.0.0.1:8000.

## Эндпоинты

`GET /time`

```json
{
  "server_time": "2026-09-30T15:32:38+01:00",
  "timezone": "Westeuropäische Sommerzeit"
}
```

`GET /date` — локальная дата сервера. `GET /date/utc` — та же дата в UTC.

```json
{
  "server_date": "2026-09-30",
  "timezone": "Westeuropäische Sommerzeit"
}
```

Интерактивная документация: http://127.0.0.1:8000/docs

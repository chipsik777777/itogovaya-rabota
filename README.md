# LLM Text Summarization Service (FastAPI + GigaChat API)

Асинхронный микросервис для автоматического создания кратких выжимок текста на базе GigaChat API с поддержкой локального кеширования, механизма повторных попыток (Retry) и гарантированного Fallback ответа при недоступности внешнего сервиса.

## Архитектура проекта

- **`api/`**: Эндпоинты FastAPI (`/health`, `/process`) и Pydantic-схемы валидации.
- **`config/`**: Управление конфигурацией через `pydantic-settings` и файл `.env`.
- **`llm/`**: Клиент GigaChat API с логикой авторизации (OAuth2), ретраями (`tenacity`) и локальным фолбеком.
- **`services/`**: Внутренние сервисы (`InMemoryTTLCache` для кеширования с TTL).
- **`tests/`**: Набор автоматических юнит-тестов (`pytest`).

## Быстрый запуск

1. **Клонирование репозитория и создание окружения:**
   ```bash
   git clone <url-вашего-репозитория>
   cd llm-summary-service
   python -m venv .venv
   
   # Активация окружения:
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
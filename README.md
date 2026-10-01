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

---

## Результаты тестирования и демонстрация работы

### 1. Проверка доступности (/health)
Сервис корректно отвечает на запросы проверки состояния.
![Health Check](docs/images/01_health_check.png)

### 2. Успешный обработанный запрос (/process)
При первичном запросе вызывается LLM-модель, а результат сохраняется в кеш (`cached: false`).
![Success Request](docs/images/02_success_request.png)

### 3. Работа TTL-кеширования (Cache Hit)
Повторный идентичный запрос возвращается мгновенно из кеша без вызова внешнего API (`cached: true`).
![Cache Hit](docs/images/03_cache_hit.png)

### 4. Автоматические тесты (pytest)
Все unit-тесты для эндпоинтов и логики сервиса проходят успешно.
![Pytest Passed](docs/images/04_pytest_results.png) 
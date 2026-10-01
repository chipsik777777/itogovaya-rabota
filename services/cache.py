import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("service.cache")


class InMemoryTTLCache:
    """Кеш в памяти с ограничением по времени жизни (TTL)."""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[str]:
        if key not in self._store:
            logger.info(f"CACHE MISS: Ключ '{key}' не найден.")
            return None

        item = self._store[key]
        if time.time() - item["timestamp"] > self.ttl:
            logger.info(f"CACHE EXPIRED: Ключ '{key}' истек по TTL.")
            del self._store[key]
            return None

        logger.info(f"CACHE HIT: Ключ '{key}' найден в кеше.")
        return item["value"]

    def set(self, key: str, value: str) -> None:
        self._store[key] = {
            "value": value,
            "timestamp": time.time()
        }
        logger.info(f"CACHE SET: Значение для ключа '{key}' успешно сохранено.") 
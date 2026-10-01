import hashlib
import re
import logging
from llm.client import LLMClient
from services.cache import InMemoryTTLCache
from config.settings import settings

logger = logging.getLogger("service.pipeline")


class TextProcessorPipeline:
    """Бизнес-логика: координация кеша, LLM и пост-обработки."""

    def __init__(self):
        self.llm_client = LLMClient()
        self.cache = InMemoryTTLCache(ttl_seconds=settings.CACHE_TTL_SECONDS)

    def _generate_cache_key(self, text: str, max_words: int) -> str:
        raw_string = f"{text}_{max_words}"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

    def _post_process(self, raw_text: str) -> str:
        """Пост-обработка: очистка лишних пробелов."""
        return re.sub(r'\s+', ' ', raw_text).strip()

    async def run(self, text: str, max_words: int) -> tuple[str, bool]:
        cache_key = self._generate_cache_key(text, max_words)

        # 1. Проверка кеша
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result, True

        # 2. Вызов LLM
        raw_result = await self.llm_client.summarize(text, max_words)

        # 3. Пост-обработка
        processed_result = self._post_process(raw_result)

        # 4. Сохранение в кеш
        self.cache.set(cache_key, processed_result)

        return processed_result, False
import base64
import logging
import uuid
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config.settings import settings

logger = logging.getLogger("service.llm")


class LLMClient:
    """Модуль работы с GigaChat API с поддержкой ретраев и fallback."""

    def __init__(self):
        self.auth_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        self.model = settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT

    async def _get_access_token(self) -> str:
        """Получение временного токена доступа GigaChat."""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        clean_key = self.auth_key.strip()
        
        # Если передан сырой ключ "Client ID:Client Secret", кодируем его в Base64
        if ":" in clean_key:
            encoded_key = base64.b64encode(clean_key.encode("utf-8")).decode("utf-8")
            auth_header = f"Basic {encoded_key}"
        elif clean_key.startswith("Basic "):
            auth_header = clean_key
        else:
            auth_header = f"Basic {clean_key}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": auth_header
        }
        data = {"scope": "GIGACHAT_API_PERS"}

        async with httpx.AsyncClient(verify=False, timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()["access_token"]

    # Автоматически делает до 3 попыток при сбое сетевых запросов или API
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=6),
        reraise=True
    )
    async def _send_summary_request(self, text: str, max_words: int) -> str:
        token = await self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": f"Сделай краткую выжимку текста. Не более {max_words} слов."
                },
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        }

        async with httpx.AsyncClient(verify=False, timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def summarize(self, text: str, max_words: int) -> str:
        try:
            return await self._send_summary_request(text, max_words)
        except Exception as err:
            logger.error(f"Сбой GigaChat API после повторных попыток: {str(err)}. Переход на Fallback.")
            return self._fallback_response(text, max_words)

    def _fallback_response(self, text: str, max_words: int) -> str:
        words = text.strip().split()
        fallback_summary = " ".join(words[:max_words])
        if len(words) > max_words:
            fallback_summary += "..."
        return f"[FALLBACK SUMMARY]: {fallback_summary}"
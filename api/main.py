import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from services.pipeline import TextProcessorPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("service.api")

app = FastAPI(
    title="LLM Summarization Service",
    version="1.0.0"
)

pipeline = TextProcessorPipeline()


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000, description="Текст для суммаризации")
    max_words: int = Field(50, ge=5, le=500, description="Максимальное число слов в выжимке")


class SummarizeResponse(BaseModel):
    summary: str
    cached: bool


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}


@app.post("/process", response_model=SummarizeResponse, status_code=status.HTTP_200_OK)
async def summarize_text(request: SummarizeRequest):
    logger.info(f"Получен запрос на обработку. Длина текста: {len(request.text)}")
    try:
        summary_result, is_cached = await pipeline.run(request.text, request.max_words)
        return SummarizeResponse(summary=summary_result, cached=is_cached)
    except Exception as e:
        logger.error(f"Непредвиденная ошибка API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервиса при обработке запроса."
        )
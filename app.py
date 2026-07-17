import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl
from download_service import download_to_memory

app = FastAPI(title="Video Downloader API")

# Схема для валидации входящего JSON
class VideoRequest(BaseModel):
  url: str  # Принимает строку URL

@app.post("/download")
async def download_video_endpoint(request_data: VideoRequest):
  """
  Принимает JSON {"url": "https://..."}, скачивает видео в память
  и возвращает его пользователю в виде файла.
  """
  url_str = str(request_data.url).strip()

  if not url_str:
    raise HTTPException(status_code=400, detail="URL-ссылка не может быть пустой.")

  try:
    # Вызываем написанную ранее функцию скачивания в память
    filename, video_bytes = download_to_memory(url_str)

    if not video_bytes:
      raise HTTPException(status_code=500, detail="Не удалось получить данные видео.")

    # Оборачиваем байты в поток io.BytesIO, чтобы передать его в StreamingResponse
    video_stream = io.BytesIO(video_bytes)

    # Задаем базовый media_type для бинарных файлов (или video/mp4, если расширение .mp4)
    media_type = "video/mp4" if filename.endswith(".mp4") else "application/octet-stream"

    # Возвращаем файл обратно клиенту
    return StreamingResponse(
      video_stream,
      media_type=media_type,
      headers={
        # attachment заставляет браузер или клиента именно скачивать файл, а не просто открывать
        "Content-Disposition": f'attachment; filename="{filename}"'
      }
    )

  except Exception as e:
    # Если yt-dlp выдаст ошибку, вернем ее клиенту с кодом 400 или 500
    raise HTTPException(status_code=400, detail=f"Ошибка при обработке видео: {str(e)}")

# Блок для запуска сервера прямо из IntelliJ IDEA
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=9001)
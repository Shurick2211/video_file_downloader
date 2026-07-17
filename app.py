import io
import logging
from urllib.parse import quote
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from download_service import download_to_memory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Video Downloader API")


class VideoRequest(BaseModel):
  url: str

@app.post("/download")
async def download_video_endpoint(request_data: VideoRequest):

  url_str = str(request_data.url).strip()

  if not url_str:
    raise HTTPException(status_code=400, detail="URL cannot be empty.")

  try:
    filename, video_bytes = download_to_memory(url_str)

    if not video_bytes:
      raise HTTPException(status_code=500, detail="Failed to retrieve video data.")

    video_stream = io.BytesIO(video_bytes)

    media_type = "video/mp4" if filename.endswith(".mp4") else "application/octet-stream"

    encoded_filename = quote(filename, safe='')
    return StreamingResponse(
      video_stream,
      media_type=media_type,
      headers={
        "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
      }
    )

  except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    logger.error(f"Error processing video: {error_trace}")
    raise HTTPException(status_code=400, detail=f"Error processing video: {str(e)}")


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=9001)
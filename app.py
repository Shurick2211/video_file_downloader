import os
import shutil
import tempfile
import logging
from urllib.parse import quote
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from download_service import download_to_temp_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Video Downloader API")

class VideoRequest(BaseModel):
    url: str

def cleanup_temp_dir(temp_dir: str):
    """Background task to remove the temporary directory after the file is sent."""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        logger.error(f"Error cleaning up temporary directory {temp_dir}: {e}")

@app.post("/download")
async def download_video_endpoint(request_data: VideoRequest, background_tasks: BackgroundTasks):
    url_str = str(request_data.url).strip()

    if not url_str:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    # Create a temporary directory that we will manage
    temp_dir = tempfile.mkdtemp()

    try:
        filename, file_path = await download_to_temp_async(url_str, temp_dir)

        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Failed to retrieve video data.")

        media_type = "video/mp4" if filename.endswith(".mp4") else "application/octet-stream"
        encoded_filename = quote(filename, safe='')

        # Schedule the cleanup task to run AFTER the response has been completely sent
        background_tasks.add_task(cleanup_temp_dir, temp_dir)

        # FileResponse streams the file from disk, which is highly memory efficient
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except Exception as e:
        # If an error happens during download, clean up the temp dir immediately
        cleanup_temp_dir(temp_dir)
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error processing video: {error_trace}")
        raise HTTPException(status_code=400, detail=f"Error processing video: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)

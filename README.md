# Video Downloader API

A FastAPI-based video downloader service that supports multiple video platforms.

## Features

- **Multi-Platform Support**: Download videos from:
  - YouTube
  - TikTok
  - Instagram
  
- **In-Memory Processing**: Videos are downloaded to memory for efficient handling
- **Threaded Downloads**: Each download runs in a separate thread to prevent blocking
- **Streaming Response**: Efficient streaming of downloaded video files to clients
- **UTF-8 Filename Support**: Proper handling of non-ASCII filenames
- **Error Logging**: Comprehensive logging of errors and debug information

## Technology Stack

- **Framework**: FastAPI
- **Video Downloader**: yt-dlp
- **Server**: Uvicorn
- **Concurrency**: Python Threading (ThreadPoolExecutor)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd file-download
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn yt-dlp pydantic
```

## Usage

### Running the Server

```bash
python app.py
```

The API will be available at `http://localhost:9001`

### API Endpoints

#### POST `/download`

Downloads a video from a supported platform and streams it to the client.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Supported URLs:**
- YouTube: `https://www.youtube.com/watch?v=...`
- TikTok: `https://www.tiktok.com/@.../video/...`
- Instagram: `https://www.instagram.com/p/...`

**Response:**
- **Status 200**: Video file with appropriate Content-Disposition header
- **Status 400**: Invalid URL or processing error
- **Status 500**: Failed to retrieve video data

**Example with curl:**
```bash
curl -X POST "http://localhost:9001/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  -o video.mp4
```

**Example with Python:**
```python
import requests

url = "http://localhost:9001/download"
payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
response = requests.post(url, json=payload)

if response.status_code == 200:
    with open("video.mp4", "wb") as f:
        f.write(response.content)
    print("Video downloaded successfully!")
else:
    print(f"Error: {response.json()['detail']}")
```

## Project Structure

```
file-download/
├── app.py                  # FastAPI application and endpoints
├── download_service.py     # Video download logic
└── README.md              # This file
```

## How It Works

1. Client sends a POST request to `/download` with a video URL
2. The `download_to_memory()` function is invoked in a separate thread
3. yt-dlp downloads the video to a temporary directory
4. The video file is read into memory as bytes
5. The video is streamed back to the client with proper headers
6. Temporary files are cleaned up automatically

## Configuration

### Video Quality
The downloader uses the "best" format available. To change this, modify the `format` option in:
- `download_service.py`: Line 16 in `ydl_opts` dictionary

### Server Host and Port
Default: `http://0.0.0.0:9001`

To change, modify line 54 in `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=9001)
```

## Error Handling

All errors are logged with `logger.error()` and include:
- Full stack trace
- Error message
- Appropriate HTTP status codes

Check console output for debug information.

## Performance Considerations

- Videos are processed in separate threads to avoid blocking the API
- Large videos may take time to download depending on source and network
- Memory usage depends on video size
- Temporary files are automatically cleaned up

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

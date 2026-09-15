import os
from concurrent.futures import ThreadPoolExecutor
import yt_dlp
import asyncio

# A global thread pool to limit concurrent downloads and save resources.
# Max 3 concurrent downloads to avoid overwhelming the device.
_executor = ThreadPoolExecutor(max_workers=4)

def _download_to_temp_impl(url: str, temp_dir: str) -> tuple[str, str]:
    safe_filename = "video.mp4"
    temp_file = os.path.join(temp_dir, safe_filename)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': temp_file.replace('.mp4', ''),
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'restrictfilenames': True,
        'encoding': 'utf-8',
        'noprogress': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        original_title = info.get('title', 'video')
        ext = info.get('ext', 'mp4')
        base_filename = f"{original_title}.{ext}"

        files = os.listdir(temp_dir)
        if files:
            downloaded_file_path = os.path.join(temp_dir, files[0])
            if os.path.exists(downloaded_file_path):
                return base_filename, downloaded_file_path
        
        raise FileNotFoundError("yt-dlp completed, but the output file was not found.")

async def download_to_temp_async(url: str, temp_dir: str) -> tuple[str, str]:
    """
    Downloads the video asynchronously to a temporary directory without blocking the event loop.
    Returns a tuple of (original_filename, absolute_path_to_downloaded_file).
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, _download_to_temp_impl, url, temp_dir)

def download_video(url):
    print("Initializing download... This may take some time.")
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Analyzing link and downloading...")
            ydl.download([url])
        print("\n[SUCCESS] Video successfully downloaded to the project folder!")
    except Exception as e:
        print(f"\n[ERROR] Failed to download video: {e}")

if __name__ == "__main__":
    print("--- Universal Video Downloader ---")
    user_url = input("Paste a video link (YouTube, TikTok or Instagram): ").strip()
    if user_url:
        download_video(user_url)
    else:
        print("URL cannot be empty.")

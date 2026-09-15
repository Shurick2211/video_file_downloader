import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

import yt_dlp


def _download_to_memory_impl(url: str) -> tuple[str, bytes]:

  with tempfile.TemporaryDirectory() as temp_dir:

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
          with open(downloaded_file_path, "rb") as f:
            video_bytes = f.read()
          return base_filename, video_bytes
      
      raise FileNotFoundError("yt-dlp completed, but the output file was not found.")

def download_to_memory(url: str) -> tuple[str, bytes]:
  executor = ThreadPoolExecutor(max_workers=1)
  future = executor.submit(_download_to_memory_impl, url)
  result = future.result()
  executor.shutdown(wait=True)
  return result


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
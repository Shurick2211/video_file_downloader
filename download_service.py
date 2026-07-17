import os
import tempfile
import uuid

import yt_dlp

def download_to_memory(url: str) -> tuple[str, bytes]:

  with tempfile.TemporaryDirectory() as temp_dir:

    # Используем простое имя файла для избежания проблем кодирования
    safe_filename = "video.mp4"
    temp_file = os.path.join(temp_dir, safe_filename)
    
    ydl_opts = {
      'format': 'best',
      'quiet': True,
      'no_warnings': True,
      'outtmpl': temp_file.replace('.mp4', ''),  # yt-dlp добавит расширение
      'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'restrictfilenames': True,  # Ограничивает спецсимволы в именах файлов
      'encoding': 'utf-8',  # Явно указываем UTF-8 кодировку
      'noprogress': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      # Получаем оригинальное имя видео для возврата клиенту
      original_title = info.get('title', 'video')
      ext = info.get('ext', 'mp4')
      base_filename = f"{original_title}.{ext}"

      # Ищем загруженный файл в temp_dir
      files = os.listdir(temp_dir)
      if files:
        downloaded_file_path = os.path.join(temp_dir, files[0])
        
        if os.path.exists(downloaded_file_path):
          with open(downloaded_file_path, "rb") as f:
            video_bytes = f.read()
          return base_filename, video_bytes
      
      raise FileNotFoundError("yt-dlp завершил работу, но итоговый файл не найден.")

def download_video(url):
  print("Инициализация загрузки... Это может занять некоторое время.")

  ydl_opts = {
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      print("Анализируем ссылку и скачиваем...")
      ydl.download([url])
    print("\n[УСПЕХ] Видео успешно скачано в папку проекта!")
  except Exception as e:
    print(f"\n[ОШИБКА] Не удалось скачать видео: {e}")

if __name__ == "__main__":
  print("--- Универсальный Скачиватель Видео ---")
  user_url = input("Вставь ссылку на видео (YouTube, TikTok или Instagram): ").strip()

  if user_url:
    download_video(user_url)
  else:
    print("Ссылка не может быть пустой.")
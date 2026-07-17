import os
import io
import tempfile

import yt_dlp

def download_to_memory(url: str) -> tuple[str, bytes]:
  """
  Скачивает видео во временный файл, читает его в байты и удаляет файл.
  """
  # Имя файла мы узнаем в процессе скачивания, используя специальный хук
  downloaded_file_path = None

  # Создаем временную директорию ОС, которая сама очистится
  with tempfile.TemporaryDirectory() as temp_dir:

    ydl_opts = {
      'format': 'best',
      'quiet': True,
      'no_warnings': True,
      # Скачиваем строго во временную папку
      'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
      'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # Извлекаем инфо
      info = ydl.extract_info(url, download=True)
      # Получаем реальное имя файла, которое сохранила библиотека
      filename = ydl.prepare_filename(info)
      # Выделяем только базовое имя (например, "video.mp4") для отправки клиенту
      base_filename = os.path.basename(filename)

      # Находим, куда физически лег файл внутри temp_dir
      downloaded_file_path = ydl.prepare_filename(info)

    # Читаем файл в массив байт
    if downloaded_file_path and os.path.exists(downloaded_file_path):
      with open(downloaded_file_path, "rb") as f:
        video_bytes = f.read()

      # Возвращаем имя файла и его байты
      return base_filename, video_bytes
    else:
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
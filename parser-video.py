import os
import time
import requests
from is_within_allowed_time import is_within_allowed_time
from db_connect import connect_to_db
from mysql.connector import Error


def download_video(connection, video_id, download_url, save_path):
    """Скачивает видео и обновляет статус в базе данных."""
    try:
        cursor = connection.cursor()

        # Обновляем статус на 'downloading'
        cursor.execute(
            "UPDATE videos SET video_status = 'downloading' WHERE id = %s", (video_id,))
        connection.commit()

        # Скачиваем видео
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Сохраняем видео
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Обновляем статус на 'completed'
        cursor.execute(
            "UPDATE videos SET video_status = 'completed' WHERE id = %s", (video_id,))
        connection.commit()
        print(f"Видео {video_id} успешно загружено и сохранено в {save_path}")
    except requests.RequestException as e:
        # Обновляем статус на 'failed' при ошибке
        cursor.execute(
            "UPDATE videos SET video_status = 'failed' WHERE id = %s", (video_id,))
        connection.commit()
        print(f"Ошибка при загрузке видео {video_id}: {e}")
    except Error as db_error:
        print(f"Ошибка базы данных при обработке видео {video_id}: {db_error}")


def process_videos(connection, output_dir):
    """Извлекает видео со статусом 'pending' и загружает их."""
    try:
        cursor = connection.cursor(dictionary=True)

        # Извлекаем видео со статусом 'pending'
        cursor.execute(
            "SELECT id, download_url,report_id FROM videos WHERE video_status = 'pending' limit 10")
        videos = cursor.fetchall()

        if not videos:
            print("Нет видео для загрузки.")
            return

        for video in videos:
            video_id = video["id"]
            report_id = video["report_id"]
            download_url = video["download_url"]

            # Формируем путь для сохранения видео
            video_filename = f"report_{report_id}_{video_id}.mp4"
            save_path = os.path.join(output_dir, video_filename)

            # Загружаем видео
            download_video(connection, video_id, download_url, save_path)

    except Error as e:
        print(f"Ошибка при обработке видео: {e}")


def main():
    # Подключение к базе данных
    connection = connect_to_db()
    if not connection:
        exit("Не удалось подключиться к базе данных.")

    # Указываем директорию для сохранения видео
    output_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "videos")
    os.makedirs(output_directory, exist_ok=True)

    # Основной цикл обработки видео
    while True:
        process_videos(connection, output_directory)
        if not is_within_allowed_time():
            while not is_within_allowed_time():
                print("Ожидание перед следующим циклом...")
                time.sleep(60*60*1)
        # Проверяем каждые 10 минут
        print("Ожидание перед следующим циклом...")
        time.sleep(1)


if __name__ == "__main__":
    main()

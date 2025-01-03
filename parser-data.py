import json
import requests
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import time
from .is_within_allowed_time import is_within_allowed_time
# Load environment variables from .env
load_dotenv()

# Настройки подключения к MySQL

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def connect_to_db():
    """Подключение к базе данных."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Подключено к базе данных")
        return connection
    except Error as e:
        print(f"Ошибка подключения: {e}")
        return None


def save_offense(connection, offense, index, url):
    """Сохранение данных в таблицу offenses."""
    try:
        cursor = connection.cursor()
        sql_query = """
        INSERT INTO offenses (
            id, url,number, fine, fine_date, vehicle_img, article_number, article_text_ru,
            article_text_uz_cy, article_alias_ru, article_alias_uz_la, vehicle_id,
            fine_id, status, report_id, article_url, article_id, extra_img,
            extra_response, article_factor, response_id, response_text_ru,
            response_text_uz_cy, response_text_uz_la, processing_index
        ) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            offense.get("id"),
            url,
            offense.get("number"),
            offense.get("fine"),
            offense.get("fine_date"),
            offense.get("vehicle_img"),
            offense.get("article_number"),
            offense.get("article_text_ru"),
            offense.get("article_text_uz_cy"),
            offense.get("article_alias_ru"),
            offense.get("article_alias_uz_la"),
            offense.get("vehicle_id"),
            offense.get("fine_id"),
            offense.get("status"),
            offense.get("report_id"),
            offense.get("article_url"),
            offense.get("article_id"),
            offense.get("extra_img"),
            offense.get("extra_response"),
            offense.get("article_factor"),
            offense.get("response_id"),
            offense.get("response_text_ru"),
            offense.get("response_text_uz_cy"),
            offense.get("response_text_uz_la"),
            index
        )
        cursor.execute(sql_query, values)
        connection.commit()
    except Error as e:
        print(f"Ошибка сохранения offense: {e}")


def save_report(connection, report, offense_id):
    """Сохранение данных в таблицу reports."""
    try:
        cursor = connection.cursor()
        sql_query = """
        INSERT INTO reports (
            id, district_name_ru, district_name_uz_cy, district_name_uz_la, area_name_uz_cy,
            area_name_uz_la, area_name_ru, area_id, district_id, district_code,
            district_number, area_number, address, lat, lng, incident_time,
            create_time, status, district_yname_ru, district_yname_uz_cy,
            district_yname_uz_la, area_yname_ru, area_yname_uz_cy, area_yname_uz_la,
             extra_video_type, offense_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s)
        """
        values = (
            report.get("id"),
            report.get("district_name_ru"),
            report.get("district_name_uz_cy"),
            report.get("district_name_uz_la"),
            report.get("area_name_uz_cy"),
            report.get("area_name_uz_la"),
            report.get("area_name_ru"),
            report.get("area_id"),
            report.get("district_id"),
            report.get("district_code"),
            report.get("district_number"),
            report.get("area_number"),
            report.get("address"),
            report.get("lat"),
            report.get("lng"),
            report.get("incident_time"),
            report.get("create_time"),
            report.get("status"),
            report.get("district_yname_ru"),
            report.get("district_yname_uz_cy"),
            report.get("district_yname_uz_la"),
            report.get("area_yname_ru"),
            report.get("area_yname_uz_cy"),
            report.get("area_yname_uz_la"),
            report.get("extra_video_type"),
            offense_id,
        )
        # print(values)
        cursor.execute(sql_query, values)
        connection.commit()
    except Error as e:
        print(f"Ошибка сохранения report: {e}")


def save_video(connection, video, report_id):
    """Сохранение данных в таблицу videos."""
    try:
        cursor = connection.cursor()
        sql_query = """
        INSERT INTO videos (download_url, url, content_type, video_status, report_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            video.get("download-url"),
            video.get("url"),
            video.get("content-type"),
            "pending",  # Устанавливаем статус по умолчанию
            report_id,
        )
        cursor.execute(sql_query, values)
        connection.commit()
    except Error as e:
        print(f"Ошибка сохранения video: {e}")


def get_last_processed_index(connection):
    """Получение последнего обработанного индекса."""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT MAX(processing_index) AS last_index FROM offenses")
        result = cursor.fetchone()
        return result["last_index"] if result["last_index"] is not None else -1
    except Error as e:
        print(f"Ошибка получения индекса: {e}")
        return -1


def main():
    # Загружаем JSON-файл
    with open("link_v4.json", "r", encoding="utf-8") as file:
        records = json.load(file)

    connection = connect_to_db()
    if not connection:
        return

    last_index = get_last_processed_index(connection)
    print(f"Последний обработанный индекс: {last_index}")

    for index, record in enumerate(records):
        if not is_within_allowed_time():
            while not is_within_allowed_time():
                time.sleep(60*60*1)
        if index <= last_index:
            continue  # Пропускаем уже обработанные записи
        if index % 1000 == 0:
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Обработано {index} записей")
        new_url = record["concat"].replace("yhxbb", "yhxx")
        try:
            response = requests.get(new_url)
            response.raise_for_status()
            offense = response.json().get("offense", {})
            report = offense.get("report", {})
            video = report.get("video", {})
            extra_video = report.get("extra_video", {})

            save_offense(connection, offense, index, new_url)
            if report:
                save_report(connection, report, offense.get("id"))
            if video:
                save_video(connection, video, report.get("id"))
            if extra_video:
                save_video(connection, extra_video, report.get("id"))
        except requests.RequestException as e:
            print(f"Ошибка загрузки данных: {e}")

    connection.close()


if __name__ == "__main__":
    main()

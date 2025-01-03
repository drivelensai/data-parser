-- Создание таблицы offenses
CREATE TABLE offenses (
    id VARCHAR(36),
    url VARCHAR(255) ,
    number VARCHAR(50) NULL,
    fine INT NULL,
    fine_date DATETIME NULL,
    vehicle_img TEXT NULL,
    article_number VARCHAR(50) NULL,
    article_text_ru TEXT NULL,
    article_text_uz_cy TEXT NULL,
    article_alias_ru TEXT NULL,
    article_alias_uz_la TEXT NULL,
    vehicle_id VARCHAR(50) NULL,
    fine_id VARCHAR(50) NULL,
    status VARCHAR(50) NULL,
    report_id VARCHAR(36) NULL,
    article_url TEXT NULL,
    article_id INT NULL,
    extra_img TEXT NULL,
    extra_response TEXT NULL,
    article_factor FLOAT NULL,
    response_id VARCHAR(36) NULL,
    response_text_ru TEXT NULL,
    response_text_uz_cy TEXT NULL,
    response_text_uz_la TEXT NULL,
    processing_index INT NULL
);

-- Создание таблицы reports
CREATE TABLE reports (
    id VARCHAR(36) ,
    district_name_ru VARCHAR(255) NULL,
    district_name_uz_cy VARCHAR(255) NULL,
    district_name_uz_la VARCHAR(255) NULL,
    area_name_uz_cy VARCHAR(255) NULL,
    area_name_uz_la VARCHAR(255) NULL,
    area_name_ru VARCHAR(255) NULL,
    area_id VARCHAR(36) NULL,
    district_id VARCHAR(36) NULL,
    district_code INT NULL,
    district_number INT NULL,
    area_number INT NULL,
    address VARCHAR(255) NULL,
    lat FLOAT NULL,
    lng FLOAT NULL,
    incident_time DATETIME NULL,
    create_time DATETIME NULL,
    status VARCHAR(50) NULL,
    district_yname_ru VARCHAR(255) NULL,
    district_yname_uz_cy VARCHAR(255) NULL,
    district_yname_uz_la VARCHAR(255) NULL,
    area_yname_ru VARCHAR(255) NULL,
    area_yname_uz_cy VARCHAR(255) NULL,
    area_yname_uz_la VARCHAR(255) NULL,
    extra_video TEXT NULL,
    extra_video_type TEXT NULL,
    offense_id VARCHAR(36) NULL
);

-- Создание таблицы videos
CREATE TABLE videos (
    download_url TEXT NULL,
    url TEXT NULL,
    content_type VARCHAR(50) NULL,
    video_status ENUM('pending', 'downloading', 'completed', 'failed') DEFAULT 'pending',
    report_id VARCHAR(36) NULL
);

# Сервис проекта

Сервис состоит из HTTP сервера (в папке backend/) и Telegram бота (в папке bot/).

## Как запустить проект

1. Скачиваем файл с данными (https://www.kaggle.com/code/taiypeo/arxiv-lda/output?select=clustered_orig.csv)
и кладем в эту папку.
2. В этой папке создаем файл .env, в котором указываем `TELEGRAM_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>`
3. `docker compose up`

## Необходимые для запуска файлы

Эти файлы должны быть в данной папке перез запуском `docker compose up`:
- clustered_orig.csv
- .env
- docker-compose.yml

## Используемые Docker образы

- bot/ -- https://hub.docker.com/r/taiypeo/mlds-project-bot
- http_server/ -- https://hub.docker.com/r/taiypeo/mlds-project-backend

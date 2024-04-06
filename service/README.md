# Сервис проекта

Сервис состоит из HTTP сервера (в папке backend/) и Telegram бота (в папке bot/).
Telegram бот ходит в HTTP сервер для получения данных и отдает их пользователю.
Бот позволяет получить информацию о кластерах научных статей по машинному обучению за 2023,
а также сами статьи из кластеров.

## Бот Telegram

Подробнее про бот (ссылка на бота и список команд) можно
прочитать в папке [bot/](https://github.com/taiypeo/mlds-project/tree/main/service/bot).

## Бекенд

Подробнее про бекенд можно
прочитать в папке [http_server/](https://github.com/taiypeo/mlds-project/tree/main/service/http_server).

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

Также лежит в [used_docker_images.md](https://github.com/taiypeo/mlds-project/tree/main/service/used_docker_images.md).

- bot/ -- https://hub.docker.com/r/taiypeo/mlds-project-bot
- http_server/ -- https://hub.docker.com/r/taiypeo/mlds-project-backend

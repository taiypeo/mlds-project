# Backend сервер для проекта

Домашнее задание по прикладному Python #5

## Как сбилдить образ Docker

1. Скачиваем файл с данными (https://www.kaggle.com/code/taiypeo/arxiv-lda/output?select=clustered_orig.csv)
2. `docker build --tag=arxiv-project-backend .`


## Как запустить контейнер
```bash
docker run -itd -p 80:80 arxiv-project-backend
```

## Как протестить работу сервиса
```bash
curl -v "<IP>/ping"
curl -v -X POST "<IP>/rating?rating=5"
curl -v "<IP>/rating"
curl -v "<IP>/random-papers?cluster=3"
curl -v "<IP>/paper-stats"
```
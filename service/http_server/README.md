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
1. Проверка живости сервиса: `curl -v "<IP>/ping"`
2. Потавить оценку сервису: `curl -v -X POST "<IP>/rating?rating=5"`
3. Показать среднюю оценку: `curl -v "<IP>/rating"`
4. Показать (по дефолту 5) случайные пейперы из кластера #3: `curl -v "<IP>/random-papers?cluster=3"`
5. Показать общую статистику по пейперам: `curl -v "<IP>/paper-stats"`

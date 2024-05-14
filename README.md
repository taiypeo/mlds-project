# Проект "Анализ цитируемости статей"

Автор: Лысенко Иван, МОВС 1 курс

Куратор: Илья Скворцов

![GIF с примером работы](https://github.com/taiypeo/mlds-project/assets/4065977/ce6407bf-4ef0-41bf-ab25-507e7ad2d894)

## Структура проекта
```bash
.
├── checkpoint5-presentation.pdf  (презентация к 5 чекпоинту)
├── checkpoint6-examples.pdf  (примеры работы и тестирования к 6 чекпоинту)
├── clustering  (описание результатов экспериментов)
│   └── README.md
├── data  (описание результатов генерации графа цитирований)
│   ├── arxiv-pda.ipynb  (ноутбук для генерации графа цитирований)
│   └── README.md  (Markdown файл с ссылкой на полученный граф)
├── eda  (описание результатов разведочного анализа данных)
│   └── EDA.md
├── LICENSE  (лицензия проекта)
├── midterm-defense-presentation.pdf  (презентация к предзащите)
├── README.md  (общая документация по проекту)
└── service  (код для сервиса)
    ├── bot  (код для Telegram бота)
    │   ├── bot.py
    │   ├── Dockerfile
    │   ├── README.md
    │   └── requirements.txt
    ├── docker-compose.yml  (Docker Compose файл для запуска проекта)
    ├── http_server  (код для бекенда)
    │   ├── Dockerfile
    │   ├── main.py
    │   ├── README.md
    │   ├── requirements.txt
    │   └── tests  (тесты)
    │       └── test_http_server.py
    ├── README.md  (описание сервиса)
    └── used_docker_images.md  (используемые Docker образы)
```

## Чекпоинт 7
Эксперименты, связанные с глубинным обучением описаны в конце [clustering/README.md](https://github.com/taiypeo/mlds-project/blob/main/clustering/README.md#sentence-bert--k-meansdbscan).

## Бот
Код бота Телеграм и бекенда для него, описание функционала, инструкции по запуску и тестированию,
а также ссылки на Docker Hub для использованных образов находятся в
папке [service/](https://github.com/taiypeo/mlds-project/tree/main/service).

Также список используемых Docker образов лежит в файле [service/used_docker_images.md](https://github.com/taiypeo/mlds-project/tree/main/service/used_docker_images.md).

## Чекпоинт 5
- Презентация к чекпоинту лежит в корне репозитория [тут](https://github.com/taiypeo/mlds-project/blob/main/checkpoint5-presentation.pdf)
- В дополнение к презентации, результаты экспериментов описаны в папке [clustering/](https://github.com/taiypeo/mlds-project/tree/main/clustering) в README
- Ноутбук для обработки данных на [Kaggle](https://www.kaggle.com/code/taiypeo/arxiv-pda/notebook)
- Ноутбук для лучшей модели [LDA](https://www.kaggle.com/code/taiypeo/arxiv-lda/notebook)
- Про бот Telegram написано в предыдущем разделе

## Данные

[Данные](https://drive.google.com/drive/folders/1zg6rsWlvxnA1wh6EmV5fV6spjjxkb7tF?usp=sharing) были собраны с помощью [ноутбука в Kaggle](https://www.kaggle.com/code/taiypeo/arxiv-pda/notebook).

В качестве входных данных был использован датасет "[arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)" на Kaggle.

Ноутбук arxiv-pda.ipynb рассматривает статьи по машинному обучению 2023 года с arXiv, а затем с помощью [API Semantic Scholar](https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers)
получает список ссылок каждой статьи. Для каждой ссылки с помощью того же API получается список ее ссылок (не рассматриваем новые статьи, иначе будет слишком много).
В итоге получаются файлы:

- graph.json -- граф цитирований рассмотренных статей. Формат:
  ```
  {
    "semantic_scholar_id_1": ["semantic_scholar_id_2", "semantic_scholar_id_3", ...],
    "semantic_scholar_id_2": ["semantic_scholar_id_3", ...],
    ...
  }
  ```
- papers.json -- информация про статьи (название, абстракт, год, Semantic Scholar ID). Формат:
  ```
  {
    "semantic_scholar_id_1": {
      "paperId": "semantic_scholar_id_1",
      "title": "title_1",
      "abstract": "abstract_1",
      "year": 2023
    },
    ...
  }
  ```
- unique_original_ids.json -- список Semantic Scholar ID исходных статей с arXiv 2023 года. Формат:
  ```
  [
    "semantic_scholar_id_1",
    "semantic_scholar_id_2",
    ...
  ]
  ```
- paper_references_cleaned.json -- вспомогательный файл, используемый для генерации остальных. Не будет дальше использоваться, сохранялся на всякий случай как промежуточное состояние.

## Примерный план работы

- Сбор данных
- Анализ литературы по графовой кластеризации и NLP методам для кластеризации
- Анализ графа цитирований с помощью простых методов графовой кластеризации (например, спектральной кластеризации)
- Кластеризация статей по контенту, например, используя эмбеддинги BERT
- Topic modeling?
- Использование моделей attributed graph clustering, учитывающих как структуру графа, так и контент вершин
- Анализ полученных результатов

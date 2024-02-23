# Проект "Анализ цитируемости статей"

Автор: Лысенко Иван, МОВС 1 курс

Куратор: Кофанова Мария

## Чекпоинт 5
- Результаты экспериментов описаны в папке [clustering/](https://github.com/taiypeo/mlds-project/tree/main/clustering).
  Вместо презентации я подробно описал все в README.md.
- Ноутбук для обработки данных на [Kaggle](https://www.kaggle.com/code/taiypeo/arxiv-pda/notebook)
- Ноутбук для лучшей модели [LDA](https://www.kaggle.com/code/taiypeo/arxiv-lda/notebook)

## Бот
Код бота Телеграм, а также GIF с примером работы находятся в папке [bot/](https://github.com/taiypeo/mlds-project/tree/main/bot).

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

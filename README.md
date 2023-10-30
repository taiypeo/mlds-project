# mlds-project
Проект "Анализ цитируемости статей"

## Данные

[Данные](https://drive.google.com/drive/folders/1zg6rsWlvxnA1wh6EmV5fV6spjjxkb7tF?usp=sharing) были собраны с помощью [ноутбука в Kaggle](https://www.kaggle.com/code/taiypeo/arxiv-pda/notebook).

В качестве входных данных был использован датасет "[arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)" на Kaggle.

Ноутбук arxiv-pda.ipynb рассматривает статьи по машинному обучению 2023 года с arXiv, а затем с помощью [API Semantic Scholar](https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers)
получает список ссылок каждой статьи. Для каждой ссылки с помощью того же API получается список ее ссылок (не рассматриваем новые статьи, иначе будет слишком много).
В итоге получаются файлы:

- graph.json -- граф цитирований рассмотренных статей
- papers.json -- информация про статьи (название, абстракт, год, Semantic Scholar ID)
- unique_original_ids.json -- список Semantic Scholar ID исходных статей с arXiv
- paper_references_cleaned.json -- вспомогательный файл, используемый для генерации остальных

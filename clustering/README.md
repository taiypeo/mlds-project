# Результаты кластеризации

## Спектральная кластеризация
Результаты по спектральной кластеризации можно найти в папке [eda/](https://github.com/taiypeo/mlds-project/tree/main/eda)

## LDA
Ноутбук для LDA лежит на [Kaggle](https://www.kaggle.com/code/taiypeo/arxiv-lda/notebook). Результаты кластеризации по темам
можно найти во вкладке "Output".

После провалившихся экспериментов со спектральной кластеризацией, я решил попробовать простой бейзлайн topic modelling, не учитывающий
связи между статьями. В качестве модели я взял LDA, как довольно популярную и, по предыдущему опыту, рабочую.

Из своего [графа](https://github.com/taiypeo/mlds-project/tree/main/data) я взял только статьи 2023 года с arXiv (те, с которых начиналась сборка графа).
Для текстового описания каждой статьи я
- Склеил название и abstract
- Привел полученные текста к нижнему регистру
- Токенизировал полученные тексты на слова с помощью библиотеки nltk
- Убрал токены, которые содержали символы, отличные от латинского алфавита
- Лемматизировал токены с помощью WordNetLemmatizer из nltk
- Обратно соединил токены в текст, склеив их пробелами

Далее я работал только с такими упрощенными текстами.

С помощью библиотеки gensim, я создал словарь используемых токенов, не учитывая слишком редкие, которые встречались меньше, чем в 20 документах,
а также слишком частые, которые были больше, чем в 50% документов. Оказалось, что некоторые токены ("algorithm", "learning", "training", "data")
тоже оказались довольно частыми, и поэтому захламляли выход LDA, поэтому я их тоже убрал из словаря.

На текстах с помощью итогового словаря из 6715 токенов я натренировал модель LDAMulticore из gensim (n_topics=10). Темы получились такие:
```
[(0,
  '0.040*"network" + 0.030*"neural" + 0.011*"performance" + 0.011*"architecture" + 0.011*"deep" + 0.009*"accuracy" + 0.009*"parameter" + 0.008*"adversarial" + 0.008*"layer" + 0.007*"attack"'),
 (1,
  '0.027*"object" + 0.018*"image" + 0.018*"segmentation" + 0.014*"feature" + 0.013*"detection" + 0.012*"scene" + 0.011*"point" + 0.008*"pose" + 0.008*"dataset" + 0.007*"propose"'),
 (2,
  '0.017*"domain" + 0.015*"label" + 0.014*"performance" + 0.013*"sample" + 0.011*"class" + 0.011*"datasets" + 0.009*"task" + 0.009*"classification" + 0.008*"propose" + 0.008*"distribution"'),
 (3,
  '0.062*"image" + 0.022*"generation" + 0.020*"diffusion" + 0.016*"generative" + 0.009*"latent" + 0.008*"generate" + 0.008*"face" + 0.008*"quality" + 0.008*"propose" + 0.007*"text"'),
 (4,
  '0.015*"using" + 0.015*"medical" + 0.013*"dataset" + 0.013*"detection" + 0.010*"image" + 0.010*"recognition" + 0.010*"classification" + 0.008*"feature" + 0.008*"result" + 0.008*"accuracy"'),
 (5,
  '0.039*"graph" + 0.023*"representation" + 0.016*"knowledge" + 0.015*"feature" + 0.015*"information" + 0.012*"network" + 0.011*"structure" + 0.010*"propose" + 0.009*"node" + 0.009*"task"'),
 (6,
  '0.025*"task" + 0.021*"video" + 0.020*"transformer" + 0.015*"visual" + 0.012*"attention" + 0.011*"representation" + 0.010*"temporal" + 0.010*"performance" + 0.010*"feature" + 0.009*"image"'),
 (7,
  '0.038*"language" + 0.017*"task" + 0.015*"llm" + 0.014*"text" + 0.010*"large" + 0.008*"question" + 0.008*"performance" + 0.007*"reasoning" + 0.007*"dataset" + 0.007*"human"'),
 (8,
  '0.013*"problem" + 0.011*"function" + 0.008*"policy" + 0.008*"show" + 0.007*"optimization" + 0.007*"approach" + 0.007*"distribution" + 0.006*"reinforcement" + 0.006*"result" + 0.005*"bound"'),
 (9,
  '0.013*"system" + 0.010*"research" + 0.008*"application" + 0.007*"ha" + 0.007*"ai" + 0.007*"machine" + 0.007*"time" + 0.006*"paper" + 0.006*"explanation" + 0.006*"approach"')]
```

Не все темы интерпретируемые, однако есть довольно понятные. Например, тема 1 относится к таким задачам computer vision, как object detection или segmentation. Тема 3 относится к генеративным CV моделям (diffusion, GAN, ...).
Тема 7 относится к LLM. И так далее.

Итоговое распределение размеров тем:
- 0    3367
- 1    4206
- 2    4100
- 3    2094
- 4    1932
- 5    2182
- 6    2830
- 7    6291
- 8    4969
- 9    3492

Данная модель получила следующие coherence scores:
```
{'c_uci': 0.16782136767006903,
 'u_mass': -1.9202423728221656,
 'c_v': 0.4305037505193886,
 'c_npmi': 0.025258243796836926}
```

Пока что они вышли не очень высокими.
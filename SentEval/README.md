# SentEval

This is a student project for sentiment analysis of restaurant reviews which is a part of [HSE Computational Linguistics studying program](https://www.hse.ru/en/ma/ling/).<br>
The project is absolutely free so you can try load all the materials and test it yourself.<br>

### How does it work?

0. You choose a restaurant name
1. We collect reviews from Foursquare and Zoon
2. Then we analyze it with pymystem3 (extract lemma and part of speech)
3. Lemmas are processed by pre-trained word2vec model and 3 SVM models <br>(each model is responsible for certain aspect: food, service, interior)
4. The results are summarized and you can see the overall sentiment

### Resources
> You can find all models [here](https://drive.google.com/folderview?id=0BwRU-58YQiIiTnA5OHFOOW1rVTA&usp=sharing)<br>
> and see all the project history on [WikiSpaces](https://hsecompling.wikispaces.com/-/SentiEval/SentiEval/?responseToken=0ea6eaf455f3f11f6009e44546715e099) and [presentation](https://www.hse.ru/data/2015/04/15/1094819508/%D0%BF%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%20Senteval%20.pdf)

# SentEval

Это научно-исследовательский проект в рамках учебной программы [Компьютерная лингвистика в магистратуре НИУ ВШЭ](https://www.hse.ru/ma/ling/).<br>
Основная цель проекта - реализация анализа тональности отзывов о ресторанах.<br>
Это открытый проект, поэтому любой желающий может воспользоваться результатами онлайн, либо скачать все материалы и протестировать их самостоятельно.<br>

### Как это работает?

0. Вы вводите название ресторана
1. Мы автоматически собираем отзывы с сайтов Foursquare и Zoon
2. Затем мы анализируем тексты отзывов с помощью библиотеки pymystem3 (лемматизируем и определяем части речи)
3. Далее полученные леммы поступают на вход обученной модели word2vec и трём SVM моделям <br>(каждая из трёх моделей отвечает за определенный аспект: еда, сервис, интерьер)
4. Результаты усредняются и получаем общую оценку отзывов по ресторану.

### Ресурсы:
> Все вышеуказанные модели можно скачать [здесь](https://drive.google.com/folderview?id=0BwRU-58YQiIiTnA5OHFOOW1rVTA&usp=sharing),<br>
> а почитать историю проекта можно на [WikiSpaces](https://hsecompling.wikispaces.com/-/SentiEval/SentiEval/?responseToken=0ea6eaf455f3f11f6009e44546715e099) и [presentation](https://www.hse.ru/data/2015/04/15/1094819508/%D0%BF%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%20Senteval%20.pdf)

### Если вы хотите воспользоваться материалами проекта самостоятельно:

0. Необходимо убедиться, что предустановлены:
	* Python 2.7 (https://www.python.org/download/releases/2.7/)
	* библиотеки для python: foursquare, numpy, BeautifulSoup, gensim, sklearn, pymystem3
1. скопировать этот репозиторий
2. скачать модели отсюда https://drive.google.com/folderview?id=0BwRU-58YQiIiTnA5OHFOOW1rVTA&usp=sharing
3. в скрипте process_restaurant_request.py в строчках 137, 138, 139 и 143 указать соответствующие пути к моделям (мы не стали размещать модели в репозатории, так как они весьма массивные - в сумме ~ 1.1 Gb)
4. в командной строке убедиться, что вы находитесь в той же папке, где лежит скрипт, и ввести:
	>>> python process_restaurant_request.py "название ресторана"
5. в результате вы получите json с оценками по 3 аспектам и числом обработанных отзывов.

# SentEval

This is a student project for sentiment analysis of restaurant reviews.<br>
You can test it as a web service on http://sehse.azurewebsites.net/<br>

### How does it work?

0. You choose a restaurant name
1. We collect reviews from Foursquare and Zoon
2. Then we analyze it with pymystem3 (extract lemma and part of speech)
3. Lemmas are processed by pre-trained word2vec model and 3 SVM models <br>(each model is responsible for certain aspect: food, service, interior)
4. The results are summarized and you can see the overall sentiment

### Resources
> You can find all models [here](https://drive.google.com/folderview?id=0BwRU-58YQiIiTnA5OHFOOW1rVTA&usp=sharing)<br>
> and see all the project history on [WikiSpaces](https://hsecompling.wikispaces.com/-/SentiEval/SentiEval/?responseToken=0ea6eaf455f3f11f6009e44546715e099) and [presentation](https://www.hse.ru/data/2015/04/15/1094819508/%D0%BF%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%20Senteval%20.pdf)
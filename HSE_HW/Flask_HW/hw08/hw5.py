# -*- coding: utf-8 -*-
# Philip Dick small library

from flask import Flask, render_template, request, url_for
import codecs
import glob

app = Flask(__name__)

@app.route('/')
def index():
    files = glob.glob("texts/*.txt")
    titles = [(n, str(text).strip('.txt').strip('texts/')) for n, text in enumerate(files)]
    return render_template("index.html", texts=titles)

@app.route("/view/<int:id>")
def article(id):
    novel = glob.glob("texts/*.txt")[id]
    fd = codecs.open(novel, 'r', encoding = "utf-8")
    text = fd.readlines()
    title = text[0]
    return render_template("article.html", article=text[1:], title=title)

@app.route('/search', defaults={'page':1}, methods=['POST', 'GET'])
@app.route('/search/page/<int:page>')

def search(page):
    text_ids = []
    if request.method == 'POST':
        query = request.values.get('query')
        for i in range(len(files)):
            text = files[i]
            if query.lower().strip() in text.lower():
                text_ids.append(i)
    requested_files = []
    for k in text_ids:
        requested_files.append(files[k])
    return render_template('search.html', texts=requested_files)

if __name__ == "__main__":
    app.run(debug=True)

# -*- coding: utf-8 -*-
# Philip Dick small library

from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)

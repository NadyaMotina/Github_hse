# -*- coding: utf-8 -*-
# Philip Dick small library

from flask import Flask, render_template, request, jsonify
import codecs
import glob

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/json/texts')
def texts():
	# Define how many text names to show next
	start = int(request.values.get('start'))
	amount = int(request.values.get('amount'))
	#
	# extract texts and their names
	files = glob.glob("texts/*.txt")
	titles = [str(text).strip('.txt').strip('texts/') for text in files]
	texts = []
	for i in range(len(files)):
		texts.append(dict(textid=str(i), text=titles[i]))
	return jsonify(dict(texts=texts[start:(start+amount)]))

@app.route("/view/<int:id>")

def article(id):
    novel = glob.glob("texts/*.txt")[id]
    fd = codecs.open(novel, 'r', encoding = "utf-8")
    text = fd.readlines()
    title = text[0]
    return render_template("article.html", article=text[1:], title=title)

if __name__ == "__main__":
    app.run(debug=True)

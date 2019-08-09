from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/stock')
def stock():
	return render_template('stock.html',title = 'Stock',press = 'true')

@app.route('/article')
def article():
	return render_template('article.html',title = 'Article', press = 'true')

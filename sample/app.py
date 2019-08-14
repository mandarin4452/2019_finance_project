from flask import Flask, render_template, redirect, request, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/<int:num>')
def inputTest(num=None):
    return render_template('main.html',num=num)

@app.route('/calculate',methods=['POST'])
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
        if temp == '':
            temp = 0
    else:
        temp = None
    return redirect(url_for('inputTest',num=temp))

if __name__ == '__main__':
    app.run(debug = True)

#https://doorbw.tistory.com/46?category=679147
#수요일까지 해결하기


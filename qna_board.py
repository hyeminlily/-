from flask import Flask, render_template, request, session
from bson import ObjectId
import datetime
import qna_func

app = Flask(__name__)

@app.route('/board')
def getList():
    list = qna_func.getList()
    return render_template('board.html', list=list)

@app.route('/dashboard')
def dashboard():
    list = qna_func.getList()
    return render_template('dashboard.html', list=list)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        saved_at = datetime.datetime.now()
        qna_func.insert(title, content, saved_at)
        return render_template('dashboard.html', list=list)
    return render_template('insert.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        orgin_id = request.form['id']
        new_id = ObjectId(orgin_id)
        title = request.form['title']
        content = request.form['content']
        saved_at = datetime.datetime.now()
        qna_func.update(new_id, title, content, saved_at)
        return render_template('dashboard.html', list=list)
    else:
        orgin_id = request.args.get('id', '')
        new_id = ObjectId(orgin_id)
        post_one = qna_func.detail(new_id)
        return render_template('update.html', post_one=post_one)

@app.route('/delete')
def delete():
    orgin_id = request.args.get('id', '')
    new_id = ObjectId(orgin_id)
    qna_func.delete(new_id)
    return render_template('dashboard.html', list=list)

if __name__ == '__main__':
    app.run(debug=True, host='203.236.209.98')
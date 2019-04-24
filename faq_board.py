from flask import Flask, render_template, request, session
from bson import ObjectId
import datetime
import faq_func

app = Flask(__name__)

@app.route('/board')
def getList():
    list = faq_func.getList()
    faq = faq_func.getFaq()
    return render_template('board.html', list=list, faq=faq)

@app.route('/dashboard')
def dashboard():
    list = faq_func.getList()
    return render_template('dashboard.html', list=list)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        saved_at = datetime.datetime.now()
        faq_func.insert(title, content, saved_at)
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
        faq_func.update(new_id, title, content, saved_at)
        return render_template('dashboard.html', list=list)
    else:
        orgin_id = request.args.get('id', '')
        new_id = ObjectId(orgin_id)
        post_one = faq_func.detail(new_id)
        return render_template('update.html', post_one=post_one)

@app.route('/delete')
def delete():
    orgin_id = request.args.get('id', '')
    new_id = ObjectId(orgin_id)
    faq_func.delete(new_id)
    return render_template('dashboard.html', list=list)

@app.route('/faqboard')
def faqboard():
    list = faq_func.getFaq()
    return render_template('faqboard.html', list=list)

@app.route('/insertfaq', methods=['GET', 'POST'])
def insertfaq():
    if request.method == 'POST':
        kinds = request.form['kinds']
        title = request.form['title']
        content = request.form['content']
        saved_at = datetime.datetime.now()
        faq_func.insertFaq(kinds, title, content, saved_at)
        return render_template('faqboard.html', list=list)
    return render_template('insertfaq.html')

@app.route('/updatefaq', methods=['GET', 'POST'])
def updatefaq():
    if request.method == 'POST':
        orgin_id = request.form['id']
        new_id = ObjectId(orgin_id)
        kinds = request.form['kinds']
        title = request.form['title']
        content = request.form['content']
        saved_at = datetime.datetime.now()
        faq_func.updateFaq(new_id, kinds, title, content, saved_at)
        return render_template('faqboard.html', list=list)
    else:
        orgin_id = request.args.get('id', '')
        new_id = ObjectId(orgin_id)
        post_one = faq_func.detailFaq(new_id)
        return render_template('updatefaq.html', post_one=post_one)

@app.route('/deletefaq')
def deletefaq():
    orgin_id = request.args.get('id', '')
    new_id = ObjectId(orgin_id)
    faq_func.deleteFaq(new_id)
    return render_template('faqboard.html', list=list)

if __name__ == '__main__':
    app.run(debug=True, host='203.236.209.108')
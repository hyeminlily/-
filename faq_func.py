from pymongo import MongoClient
def getList():
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    board = db['board']
    boardAll = board.find({})

    list = []
    for b in boardAll:
        list.append(b)
    return list

def insert(title, content, saved_at):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    board = db['board']
    doc = {'title': title, 'content': content, 'saved_at': saved_at}
    board.insert_one(doc)
    client.close()

def detail(id):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    board = db['board']
    post_one = board.find_one({'_id': id})
    client.close()
    return post_one

def update(id, title, content, saved_at):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    board = db['board']
    q = {'_id': id}
    set = {'$set': {'title': title, 'content': content, 'saved_at': saved_at}}
    board.update_one(q, set)
    client.close()

def delete(id):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    board = db['board']
    board.remove({'_id': id})
    client.close()

def getFaq():
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    faq = db['faq']
    faqAll = faq.find()

    list = []
    for f in faqAll:
        list.append(f)
    return list

def insertFaq(kinds, title, content, saved_at):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    faq = db['faq']
    doc = {'kinds': kinds, 'title': title, 'content': content, 'saved_at': saved_at}
    faq.insert_one(doc)
    client.close()

def detailFaq(id):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    faq = db['faq']
    post_one = faq.find_one({'_id': id})
    client.close()
    return post_one

def updateFaq(id, kinds, title, content, saved_at):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    faq = db['faq']
    q = {'_id': id}
    set = {'$set': {'kinds': kinds, 'title': title, 'content': content, 'saved_at': saved_at}}
    faq.update_one(q, set)
    client.close()

def deleteFaq(id):
    client = MongoClient("localhost", 27017)
    db = client['hyeminseo']
    faq = db['faq']
    faq.remove({'_id': id})
    client.close()
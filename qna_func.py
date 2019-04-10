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
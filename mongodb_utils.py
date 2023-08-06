from pymongo import MongoClient
import pandas as pd 

def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.academicworld
    return db 

def return_keywords():
    db = connect_to_mongo()
    df = db.publications.aggregate([
    { '$unwind': '$keywords' }, 
    { '$limit': 100}, 
    { '$project': {'keywords.name':1}}
])

    words = pd.DataFrame(list(df))['keywords'].tolist()
    words = [i['name'] for i in words]
    
    return words

def widget4_helper(selected_keyword = 'Deep Learning'):
    db = connect_to_mongo()
    pipeline = [
        {"$unwind": "$keywords"},
        {"$match": {'keywords.name': f"{selected_keyword}"}},

        {"$lookup": {
            "from": 'faculty',
            "localField": 'id',
            "foreignField": 'publications',
            "as": 'faculty'
        }},

        {"$project": {
            '_id': 1,
            'faculty.name': 1,
            'keywords.name': 1,
            'keywords.score': 1,
            'numCitations': 1,
            'KRC': {"$multiply": ['$numCitations', '$keywords.score']},
            'faculty.affiliation.name': 1
        }},

        {"$unwind": "$faculty"},

        {"$group": {
            "_id": '$faculty.affiliation.name',
            'KRC': {"$sum": '$KRC'}
        }},

        {"$sort": {'KRC': -1}}
    ]

    db.publications.create_index('keywords.name')
    result = db.publications.aggregate(pipeline)
    df = pd.DataFrame(list(result))
    df.columns = ['University','Score']
    df = df.iloc[:10]
    
    universities = df['University'].tolist()
    universities = universities + ['NA'] * (10 - len(universities))
    
    scores = df['Score'].tolist()
    scores = scores + [0] * (10 - len(scores))


    return universities, scores


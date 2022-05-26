from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['bd_hh']
vacancy_hh = db.vacancy_hh

my_salary = 250000

for vacancy in vacancy_hh.find ({"$or": [
            {"$and": [{'min_salary': None}, {'max_salary': {"$gte": my_salary}}]},
            {'min_salary': {"$gte": my_salary}},
            {"$and": [{'min_salary': {"$lte": my_salary}}, {'max_salary': {"$gte": my_salary}}]},
            {'max_salary': None}
            ]}):
    pprint(vacancy)


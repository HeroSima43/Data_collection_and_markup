# Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе.
# https://www.mongodb.com/ https://www.mongodb.com/products/compass
# Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта
# с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
# Поэкспериментируйте с различными методами запросов.
# Зарегистрируйтесь в ClickHouse.
# Загрузите данные в ClickHouse и создайте таблицу для их хранения.

from pymongo import MongoClient
from clickhouse_driver import Client
import json
from pprint import pprint


def store_into_mongodb(all_books):
    client = MongoClient('mongodb://localhost:27017')
    client.drop_database('booksales')
    booksales = client["booksales"]
    books = booksales["books"]
    books.insert_many(all_books)
    return books


def select_from_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    booksales = client["booksales"]
    books = booksales["books"]
    # найти сведения о книге 'Penny Maybe'
    query = {'name': 'Penny Maybe'}
    pprint(books.find_one(query))
    # найти книги дороже 59 и дешевле 60
    query = {'price': {'$gt': 59, '$lt': 60}}
    projection = {"_id": 0, "name": 1, 'price': 1}
    for book in books.find(query, projection):
        pprint(book)
    projection = {"_id": 0, "name": 1}
    # найти книги, в названии которых есть слово People
    query = {"name": {"$regex": "[Pp]eople"}}
    for book in books.find(query, projection):
        pprint(book)


def store_into_clickhouse(all_books):
    client = Client(host='localhost')
    client.execute('DROP DATABASE IF EXISTS booksales;')
    client.execute('CREATE DATABASE booksales;')
    client.execute(
        '''
        CREATE TABLE booksales.books (
            `id` UInt64,
            `name` String,
            `price` Float32,
            `available` Int32,
            `description` String)
            ENGINE = MergeTree()
            PRIMARY KEY `id`;
        '''
    )
    id = 0
    for book in all_books:
        client.execute('INSERT INTO booksales.books (id, name, price, available, description) VALUES',
                       [(id, book['name'], book['price'], book['available'], book['description'])])
        id += 1


# Загружаем данные из файла .json
with open('Lesson_3/books_to_scrape.json', 'r') as f:
    all_books = json.load(fp=f)

store_into_mongodb(all_books)
select_from_mongodb()
store_into_clickhouse(all_books)

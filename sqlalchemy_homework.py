from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_homework_models import create_tables, delete_tables,\
    Publisher, Book, Shop, Stock, Sale
import json

with open('credentials.txt', 'r') as file:
    username = file.readline().strip()
    data_base = file.readline().strip()
    password = file.readline().strip()

DSN = 'postgresql://%s:%s@localhost:5432/%s' % (username, password, data_base)
engine = create_engine(DSN)

delete_tables(engine)
create_tables(engine)

""" читаем файл и заполняем базу"""

with open('test_data.json', 'r', encoding='UTF-8') as f:
    data = json.load(f)
publishers = data[:4]
books = data[4:10]
shops = data[10:13]
stocks = data[13:22]
sales = data[22:]

Session = sessionmaker(bind=engine)
session = Session()

for item in publishers:
    name = (item['fields']['name'])
    data = Publisher(name=name)
    session.add(data)
    session.commit()
for item in books:
    id_publisher = item['fields']['id_publisher']
    title = item['fields']['title']
    data = Book(id_publisher=id_publisher, title=title)
    session.add(data)
    session.commit()
for item in shops:
    name = (item['fields']['name'])
    data = Shop(name=name)
    session.add(data)
    session.commit()
for item in stocks:
    id_book = item['fields']['id_book']
    id_shop = item['fields']['id_shop']
    count = item['fields']['count']
    data = Stock(id_book=id_book, id_shop=id_shop, count=count)
    session.add(data)
    session.commit()
for item in sales:
    price = item['fields']['price']
    date_sale = (item['fields']['date_sale'][0:10])
    id_stock = item['fields']['id_stock']
    count = item['fields']['count']
    data = Sale(price=price, date_sale=date_sale, id_stock=id_stock, count=count)
    session.add(data)
    session.commit()

""" название издательства для поиска"""

publisher_name = 'O’Reilly'

""" обьединения таблиц и запросы"""

data = select(Book.title, Shop.name, Sale.price*Sale.count,Sale.date_sale).select_from(Publisher, Book, Stock, Shop, Sale).\
    join(Book, Publisher.id == Book.id_publisher).filter(Publisher.name == publisher_name). \
    join(Stock, Book.id == Stock.id_book).\
    join(Shop, Stock.id_shop == Shop.id).\
    join(Sale, Stock.id == Sale.id_stock)

"""вывод результата"""

print("{:<42} {:<12} {:<13} {:<12}".format('Book name', 'Shop name', 'Total price', 'Date'))
print()
for row in session.execute(data):
    print("{:<42} {:<12} {:<13} {:<12}".format(row[0], row[1], row[2], row[3]))

session.close()


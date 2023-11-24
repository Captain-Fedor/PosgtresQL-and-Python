import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_homework_models import create_tables, delete_tables, drop_table,\
    Publisher, Book, Shop, Stock, Sale, Book_to_Stock, Stock_to_Sale
import json

with open('credentials.txt', 'r') as file:
    username = file.readline().strip()
    data_base = file.readline().strip()
    password = file.readline().strip()

DSN = 'postgresql://%s:%s@localhost:5432/%s' % (username, password, data_base)
engine = sqlalchemy.create_engine(DSN)

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
    date_sale = item['fields']['date_sale']
    id_stock = item['fields']['id_stock']
    count = item['fields']['count']
    data = Sale(price=price, date_sale=date_sale, id_stock=id_stock, count=count)
    session.add(data)
    session.commit()

""" название издательства для поиска"""

publisher_name = 'O’Reilly'

""" обьединения таблиц и запросы"""

subq = session.query(Book).join(Publisher).filter(Publisher.name == publisher_name).subquery()
query = session.query(Stock).join(subq, Stock.id_book == subq.c.id)
for p in query:            #помежуточная таблица с названием книги и id магазина Book_to_Stock
    title = p.book.title
    id_shop = p.id_shop
    id_stock = p.id
    data = Book_to_Stock(title=title, id_shop=id_shop, id_stock=id_stock)
    session.add(data)
    session.commit()

query = session.query(Book_to_Stock, Shop).\
    outerjoin(Shop, Book_to_Stock.id_shop == Shop.id).all()

        #промежуточная таблица с названием книги, названием магазина, id_stock Stock_to_Sale
for Book_to_Stock, Shop in query:
    title = Book_to_Stock.title
    shop_name = Shop.name
    id_stock = Book_to_Stock.id_stock
    data = Stock_to_Sale(title=title, shop_name=shop_name, id_stock=id_stock)
    session.add(data)
    session.commit()

"""вывод результата"""

print(Book_to_Stock.title, Shop.name, Book_to_Stock.id_stock)
print()
print()
query = session.query(Stock_to_Sale, Sale).\
    join(Sale, Stock_to_Sale.id_stock == Sale.id_stock).all()

print("{:<42} {:<12} {:<13} {:<12}".format('Book name', 'Shop name', 'Total price', 'Date'))
print()
for Stock_to_Sale, Sale in query:
   print("{:<42} {:<12} {:<13} {:<12}".format(Stock_to_Sale.title, Stock_to_Sale.shop_name,
                                              Sale.price*Sale.count, Sale.date_sale.date()))

"""удаление промежуточных таблицц"""

drop_table(engine, Book_to_Stock)
drop_table(engine, Stock_to_Sale)

session.close()


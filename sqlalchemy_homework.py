from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_homework_models import create_tables, delete_tables
import json

def get_shops(password_file, publisher_name, file_name):
    credentials = password_read(password_file)
    engine = database_engine(credentials)
    Session = sessionmaker(bind=engine)
    session = Session()
    data_read(file_name, session)
    extract_data(session, publisher_name)
    session.close()
def password_read(password_file):
    with open(password_file, 'r') as file:
        username = file.readline().strip()
        data_base = file.readline().strip()
        password = file.readline().strip()
        credentials = (username, password, data_base)
    return credentials

def database_engine(*args):
    args = args[0]
    DSN = 'postgresql://%s:%s@localhost:5432/%s' % (args[0], args[1], args[2])
    engine = create_engine(DSN)
    delete_tables(engine)
    create_tables(engine)
    return engine

def data_read(file_name, session):
    from sqlalchemy_homework_models import Publisher, Book, Shop, Stock, Sale
    with open(file_name, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        publishers = data[:4]
        books = data[4:10]
        shops = data[10:13]
        stocks = data[13:22]
        sales = data[22:]

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
def extract_data(session, publisher_name):
    from sqlalchemy_homework_models import Publisher, Book, Shop, Stock, Sale
    data = select(Book.title, Shop.name, Sale.price*Sale.count,Sale.date_sale).select_from(Publisher, Book, Stock, Shop, Sale).\
        join(Book, Publisher.id == Book.id_publisher).filter(Publisher.name == publisher_name). \
        join(Stock, Book.id == Stock.id_book).\
        join(Shop, Stock.id_shop == Shop.id).\
        join(Sale, Stock.id == Sale.id_stock)

    print("{:<42} {:<12} {:<13} {:<12}".format('Book name', 'Shop name', 'Total price', 'Date'))
    print()
    for row in session.execute(data) :
        print("{:<42} {:<12} {:<13} {:<12}".format(row[0], row[1], row[2], row[3]))



if __name__ == '__main__':
    get_shops(password_file='credentials.txt', publisher_name='O’Reilly', file_name='test_data.json')



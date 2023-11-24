
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True
    id = sq.Column(sq.Integer, primary_key=True)

class Book(BaseModel):
    __tablename__ = 'Books'
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('Publishers.id'), nullable=False)

class Publisher(BaseModel):
    __tablename__ = "Publishers"
    name = sq.Column(sq.String(length=40), unique=True)
    books = relationship(Book)

class Shop(BaseModel):
    __tablename__ = 'Shops'
    name = sq.Column(sq.String(length=40), unique=True)

class Stock(BaseModel):
    __tablename__ = 'Stocks'
    id_book = sq.Column(sq.Integer, sq.ForeignKey('Books.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('Shops.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship('Book', backref='stock_book')
    shop = relationship('Shop', backref='stock_shop')

class Sale(BaseModel):
    __tablename__ = 'Sales'
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stocks.id'), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='sales')

class Book_to_Stock(BaseModel):
    __tablename__ = 'Book_to_Stock'
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stocks.id'), nullable=False)
    title = sq.Column(sq.String(length=40), sq.ForeignKey('Books.title'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('Shops.id'), nullable=False)

class Stock_to_Sale(BaseModel):
    __tablename__ = 'Stock_to_Sale'
    # title = sq.Column(sq.String(length=40), sq.ForeignKey('Books.title'), nullable=False)
    # shop_name = sq.Column(sq.String(length=40), sq.ForeignKey('Shops.name'), unique=True)
    # id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stocks.id'), nullable=False)
    title = sq.Column(sq.String(length=40), nullable=False)
    shop_name = sq.Column(sq.String(length=40))
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stocks.id'), nullable=False)

def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)

def drop_table(engine, table):
    table.__table__.drop(engine)












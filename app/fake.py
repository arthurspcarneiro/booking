from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Role, Trade


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()

def start_again():
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    users(10)
    posts(10)
    u = User(email='arthurpythonmail@gmail.com',
                 username='arthurpythonmail',
                 password='123456',
                 confirmed=True,
                 role = Role.query.filter_by(name="Administrator").first())
                 
    db.session.add(u)
    db.session.commit()

def trades(count=100):
    fake = Faker()
    i = 0
    u = User.query.filter_by(username="arthurpythonmail").first()
    while i < count:
        trade = Trade(order = "Buy",\
                        product = "call",code = "PETR4",\
                            strategy = "Seco",\
                            trade_date = fake.past_date(),\
                            strike = 10,amount = 100,\
                            price = 25,
                            trade_user = u) 
        db.session.add(trade)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()




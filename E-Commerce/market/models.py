# NOTE: CTRL + B to see inner workings of the class relative to where CTRL + B was hit

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)

# class Item(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     barcode = db.Column(db.String(length=12), nullable=False, unique=True)
#     price = db.Column(db.Integer(), nullable=False)
#     description = db.Column(db.String(length=1024), nullable=False, unique=True)
#
#     def __repr__(self):
#         return f'Item {self.name}'

# from market import db
# from market import bcrypt
# from market import login_manager
from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)
    return User.query.get(int(user_id))

# class Item(db.Model):
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        # db.session.add(...) <- line not required?
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        # db.session.add(...) <- line not required?
        db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # self.password_hash = plain_text_password
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        # if bcrypt.check_password_hash(self.password_hash, attempted_password):
            # return True
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'User {self.username}'

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            # pass
            # return f'{str(p)[:-3]},{str(p)[-3:]}'
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'${self.budget}'

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items
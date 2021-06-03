from market import app, db
# from flask import render_template, redirect, url_for, flash, get_flashed_messages
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    # return '<h1>Hello World</h1>'
    return render_template('home.html')

# @app.route('/market')
# def market_page():
#     items = Item.query.all()
#     return render_template('market.html', items=items)
# @app.route('/market')
# @login_required
# def market_page():
#     items = Item.query.all()
#     return render_template('market.html', items=items)
# @app.route('/market')
# @login_required
# def market_page():
#     purchase_form = PurchaseItemForm()
#     items = Item.query.all()
#     return render_template('market.html', items=items, purchase_form=purchase_form)
# @app.route('/market')
@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    # if purchase_form.validate_on_submit():
        # print(purchase_form)
        # print(purchase_form.__dict__)
        # print(purchase_form['submit'])\
        # print(purchase_form['purchased_item'])
        # print(request.form.get('purchased_item'))
    if request.method == 'POST':
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                # p_item_object.owner = current_user.id
                # current_user.budget -= p_item_object.price
                # # db.session.add(...) <- line not required?
                # db.session.commit()
                p_item_object.buy(current_user)
                flash(f'Congratulations! You purchased {p_item_object.name} for ${p_item_object.price}', category='success')
            else:
                flash(f'Unfortunately, you don\'t have sufficient funds to purchase the {p_item_object.name}', category='danger')
        # Sold Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                # self.owner = None
                # user.budget += self.price
                # # db.session.add(...) <- line not required?
                # db.session.commit()
                s_item_object.sell(current_user)
                flash(f'Congratulations! You sold your {s_item_object.name} back to the market', category='success')
            else:
                flash(f'Unfortunately, there was an error trying to sell the {s_item_object.name}', category='danger')
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        purchased_items = Item.query.filter_by(owner=current_user.id)
        # return render_template('market.html', items=items, purchase_form=purchase_form)
        return render_template('market.html', items=items, purchase_form=purchase_form, purchased_items=purchased_items, sell_form=sell_form)
    # # items = Item.query.all()
    # items = Item.query.filter_by(owner=None)
    # return render_template('market.html', items=items, purchase_form=purchase_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # user_to_create = User(username=form.username.data,
        #                       email_address=form.email_address.data,
        #                       # password_hash=form.password1.data
        #                       password=form.password1.data)
        # db.session.add(user_to_create)
        # db.session.commit()
        # return redirect(url_for('market_page'))
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              # password_hash=form.password1.data
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: # If there are no errors from the validations
        for err_msg in form.errors.values():
            # print(err_msg)
            # print(f'There was an error with creating a user: {err_msg}')
            # flash(f'There was an error with creating a user: {err_msg}')
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # attempted_user = User.query.get(form.username.data).first()
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Incorrect username or password. Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been successfully logged out', category='info')
    return redirect(url_for('home_page'))
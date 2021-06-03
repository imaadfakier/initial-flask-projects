# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# db = SQLAlchemy(app)

from market import app

# Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
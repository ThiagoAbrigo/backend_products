from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
import config.config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    # todo
    app.config.from_object("config.config.config")
    db.init_app(app)
    with app.app_context():
        from models.invoice import Invoice
        from models.invoiceDetail import InvoiceDetail
        from models.user import User
        from routes.api_session import api_session
        from routes.api_product import api_product
        from routes.api_lot import api_lot
        app.register_blueprint(api_product)
        app.register_blueprint(api_session)
        app.register_blueprint(api_lot)
        # create table bd
        db.create_all()
        # db.drop_all()
    return app

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from . import views, error_handlers, models, api_views
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

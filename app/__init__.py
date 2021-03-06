# -*- coding: UTF-8 -*-
from datetime import timedelta
from flask import Flask
from flask_apscheduler import APScheduler
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig
from app.lib import mongo
from app.lib.pyredis import PyRedis

import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(64)
app.config.from_object(ProductionConfig)

csrf = CSRFProtect()
csrf.init_app(app)

Mongo = mongo.MongoDB(app.config.get('MONGO_IP'), app.config.get('MONGO_PORT'), app.config.get('MONGO_DB_NAME'),
                      app.config.get('MONGO_USER'), app.config.get('MONGO_PWD'))

redis_web = PyRedis(hostname=app.config.get("REDIS_IP", ""), port=app.config.get("REDIS_PORT", ""),
                    password=app.config.get("REDIS_PWD", ""))
app.permanent_session_lifetime = timedelta(hours=24 * 2)
scheduler = APScheduler()


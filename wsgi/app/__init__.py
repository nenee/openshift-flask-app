from flask import Flask
from flask import request
app = Flask(__name__)
app.secret_key = 'ZoltaR2'
from app import simple
from app import views
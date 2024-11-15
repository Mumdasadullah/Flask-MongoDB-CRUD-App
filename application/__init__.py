from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "7a458fd40551f525a995dba9b404939b934e220e"
app.config["MONGO_URI"] = "mongodb+srv://asadullah:MongoDB22115*@cluster0.q4vic.mongodb.net/sample_mflix?retryWrites=true&w=majority&appName=Cluster0"

mongo = PyMongo(app)
db = mongo.db

from application import routes
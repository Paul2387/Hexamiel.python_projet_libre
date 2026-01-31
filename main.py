from flask import Flask, render_template

import pymongo
import os

from dotenv import load_dotenv

app = Flask(__name__)


app.secret_key='Paul_mongoDB1'

#connecter a mongo_db
client = pymongo.MongoClient("mongodb+srv://Paul-Medda:Paul_mongoDB1@site-dynamique.v1oxavg.mongodb.net/?retryWrites=true&w=majority&appName=site-dynamique")
db = client["Hexamiel"]


@app.route('/')
def index():
    Produits_data = list(db["Produits"].find({}))
    Api_data = list(db["Apiculteur"].find({}))
    return render_template('index.html', Produits = Produits_data, Api = Api_data)


@app.route("/boutique")
def boutique():
    Produits_data = list(db["Produits"].find({}))
    return render_template('front/boutique.html', Produits = Produits_data)


app.run(host='0.0.0.0', port=81)
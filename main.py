from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db = client.get_database("Hexamiel")



@app.route('/')
def index():
    Produits_data = list(db["Produits"].find({}))
    Api_data = list(db["Apiculteur"].find({}))
    return render_template('index.html', Produits = Produits_data, Apiculteurs = Api_data)


@app.route("/boutique")
def boutique():
    Produits_data = list(db["Produits"].find({}))
    return render_template('front/boutique.html', Produits = Produits_data)

@app.route("/page_apiculteur")
def page_apiculteur():
    Api_data = list(db["Apiculteur"].find({}))
    return render_template('front/page_apiculteur.html', Api = Api_data)


app.run(host='0.0.0.0', port=81)
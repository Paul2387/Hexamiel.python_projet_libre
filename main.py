from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt
from bson.objectid import ObjectId



load_dotenv()

app = Flask(__name__)

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db = client.get_database("Hexamiel")
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    Produits_data = list(db["Produits"].find({}))
    Api_data = list(db["Apiculteur"].find({}))
    return render_template('index.html', Produits = Produits_data, Apiculteur = Api_data)


@app.route("/boutique")
def boutique():
    Produits_data = list(db["Produits"].find({}))
    return render_template('front/boutique.html', Produits = Produits_data)

@app.route("/page_apiculteur")
def page_apiculteur():
    Api_data = list(db["Apiculteur"].find({}))
    return render_template('front/page_apiculteur.html', Api = Api_data)


@app.route('/connexion_client' , methods=['POST', 'GET'])
def connexion_client(): 
    if request.method == "GET":
        return render_template("front/connexion_client.html")
    

    db_Client = db["Client"]
    Client = db_Client.find_one({"nom" : request.form["Nom"]})
    if Client:
        if bcrypt.checkpw(request.form["mdp"].encode("utf-8"), Client["mdp"]):
            session['role'] = Client['role']
            session['Client'] = Client["nom"]
            return redirect ("/")
        else:
            return render_template('connexion_client.html',erreur = "les mots de passe doivent etre identiques")
   




@app.route('/creation_client')
def creation_client ():
    return render_template("front/creation_client.html")



@app.route('/insertion_client', methods=['POST','GET'])
def insertion_client():

    if request.method == "POST":
        db_Client = db["Client"]
        if (db_Client.find_one({"nom" : request.form["Nom"]})):
            return render_template("front/creation_client.html", erreur = "ce nom est deja utilisé")
        else :
            if (request.form["mdp"] == request.form["confirme_mdp"]):
            

                nom= request.form["Nom"]
                mdp= request.form["mdp"]
                contact= request.form["contact"]

                mdp_crypte = mdp.encode("utf-8")
                salt= bcrypt.gensalt()
                mdp_hash = bcrypt.hashpw(mdp_crypte, salt)

                nouvel_utilisateur = {
                    "nom" : nom,
                    "mdp" : mdp_hash,
                    "contact" : contact,
                    "role": "client"
                    
                }
    
                db["Client"].insert_one(nouvel_utilisateur)

                return redirect("/")

##Admin##
@app.route('/admin')
def admin():
    Produits_data = list(db["Produits"].find({}))
    Client_data = list(db["Client"].find({}))
    if 'Client' in session and session['role'] == 'admin':
        return render_template('back/back_acceuil.html', Produits = Produits_data, Client = Client_data)
    else :
        return render_template('index.html', erreur = "Vous n'avez pas les droits d'accès", Produits = Produits_data, Client = Client_data)

@app.route('/admin/update_role/<user_id>')
def update_role(user_id):
    if 'CLient' in session and session['role'] == 'admin':
        new_role = request.form.get('role')
        db['Client'].update_one({"_id" : ObjectId(user_id)}, {"$set" : {"role" : new_role}})

    return redirect(url_for('admin'))

@app.route('/admin/delete_client/<user_id>')
def delete_user(user_id):
    if 'CLient' in session and session['role'] == 'admin':
        db['Client'].delete_one({"_id" : ObjectId(user_id)})

    return redirect(url_for('admin'))

    




app.run(host='0.0.0.0', port=81)
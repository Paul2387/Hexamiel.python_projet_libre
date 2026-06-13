from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import bcrypt
from bson.objectid import ObjectId



load_dotenv()

app = Flask(__name__)

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db = client.get_database("Hexamiel")
app.secret_key = os.urandom(24)

TAGS = ["colza", "lavande", "fleurs"]

#update data
result = db['Produits'].update_many({"$or" : [
    {"tags" : {"$exists" : False}},
    {"likes" : {"$exists" : False}},
    {"liked_by" : {"$exists" : False}},
]},
    {
        "$set" : { "tags" : [],
                  "likes" : 0,
                  "liked_by" : []
                  }
    }
)

print("database uploaded")

@app.route('/')
def index():
    Produits_data = list(db["Produits"].find({}))
    Api_data = list(db["Apiculteur"].find({}))
    if 'Client' in session:
        Client = db["Client"].find_one({"nom" : session["Client"]})
    else:
        Client = 0

    return render_template('index.html', Produits = Produits_data, Apiculteur = Api_data, Client=Client)


@app.route("/boutique")
def boutique():
    Produits_data = list(db["Produits"].find({}))
    return render_template('front/boutique.html', Produits = Produits_data)


@app.route("/page_produit/<Produit_id>")
def show_Produit(Produit_id):
    Produit = list(db["Produits"].find_one({"_id": ObjectId(Produit_id)}))
    return render_template('front/page_produit.html', Produit = Produit)

@app.route("/profil_utilisateur/<Client_id>")
def show_Client(Client_id):
    Client = list(db["Client"].find_one({"_id": ObjectId(Client_id)}))
    Produits_data = list(db["Produits"].find({}))
    return render_template('front/profil_utilisateur.html', Client = Client, Produits = Produits_data )

@app.route("/profil_appiculteur/<Apiculteur_id>")
def show_Apiculteur(Apiculteur_id):
    Apiculteur = list(db["Apiculteur"].find_one({"_id": ObjectId(Apiculteur_id)}))
    Produits_data = list(db["Produits"].find({}))
    return render_template('front/profil_apiculteur.html', Apiculteur = Apiculteur, Produits = Produits_data )


@app.route("/page_apiculteur")
def page_apiculteur():
    Api_data = list(db["Apiculteur"].find({}))
    return render_template('front/page_apiculteur.html', Apiculteur = Api_data)


@app.route('/connexion_client' , methods=['POST', 'GET'])
def connexion_client(): 
    if request.method == "GET":
        return render_template("front/connexion_client.html")
    
    

    db_Client = db["Client"]
    db_Apiculteur = db["Apiculteur"]
    Client = db_Client.find_one({"nom" : request.form["Nom"]})
    Apiculteur = db_Apiculteur.find_one({"nom":request.form["Nom"]})
    if Client:
        if bcrypt.checkpw(request.form["mdp"].encode("utf-8"), Client["mdp"]):
            session['role'] = Client['role']
            session['Client'] = Client["nom"]
            return redirect ("/")
    elif Apiculteur:
        if bcrypt.checkpw(request.form["mdp"].encode("utf-8"), Apiculteur["mdp"]):
            session['role'] = Apiculteur['role']
            session['Apiculteur'] = Apiculteur["nom"]
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

                if len(nom) < 4:
                    return redirect (url_for("creation_client"))
                
                if len(mdp) < 5:
                    return redirect (url_for("creation_client"))
                
                if mdp != request.form["confirme_mdp"]:
                    return redirect (url_for("creation_client"))

                nouvel_utilisateur = {
                    "nom" : nom,
                    "mdp" : mdp_hash,
                    "contact" : contact,
                    "role": "client"
                    
                }
    
                db["Client"].insert_one(nouvel_utilisateur)

                return redirect("/")
            
@app.route('/creation_api')
def creation_api ():
    return render_template("front/creation_apiculteur.html")
            
@app.route('/insertion_api', methods=['POST','GET'])
def insertion_api():

    if request.method == "POST":
        db_Apiculteur = db["Apiculteur"]
        if (db_Apiculteur.find_one({"nom" : request.form["Nom"]})):
            return render_template("front/creation_apiculteur.html", erreur = "ce nom est deja utilisé")
        else :
            if (request.form["mdp"] == request.form["confirme_mdp"]):
            

                nom= request.form["Nom"]
                mdp= request.form["mdp"]
                contact= request.form["contact"]
                description= request.form["description"]
                lieu= request.form["lieu"]

                mdp_crypte = mdp.encode("utf-8")
                salt= bcrypt.gensalt()
                mdp_hash = bcrypt.hashpw(mdp_crypte, salt)

                if len(nom) < 4:
                    return redirect (url_for("creation_apiculteur"))
                
                if len(mdp) < 5:
                    return redirect (url_for("creation_apiculteur"))
                
                if mdp != request.form["confirme_mdp"]:
                    return redirect (url_for("creation_apiculteur"))

                nouvel_utilisateur = {
                    "nom" : nom,
                    "mdp" : mdp_hash,
                    "contact" : contact,
                    "description" : description,
                    "lieu" : lieu,
                    "role": "apiculteur"
                    
                }
    
                db["Apiculteur"].insert_one(nouvel_utilisateur)

                return redirect("/")



##publication d'un miel
@app.route("/miel/add")
def nouveau_miel():
    return render_template("front/nouveau_miel.html", tags = TAGS)


@app.route("/miel/create", methods = ['POST'])
def create_miel():
    nom = request.form['nom']
    description = request.form['description']
    tags = request.form.getlist("tags")

    image = request.files['image']
    
    if image:
        nom_fichier = secure_filename(image.filename)
        upload_path = os.path.join(app.static.folder, "images/miel_user", nom_fichier)
        image.save(upload_path)
        image_path = f"/static/images/miel_user/{nom_fichier}"
    
    else : image_path = ""

    miel = {
        "nom" : nom,
        "image" : image_path,
        "description" : description,
        "tags" : tags,
        "likes" : 0,
        "liked_by" : []
    }
    db["Produits"].insert_one(miel)

#likes

@app.route("/Produit/like/<Produit_id>")
def like_Produit(Produit_id):
    if 'Client' not  in session:
        return redirect(url_for('connexion_client'))

    Client = session['Client']

    Produit = db["Produits"].find_one({"_id" : ObjectId(Produit_id)})

    if not Produit:
        return redirect(url_for('index'))
    
    if Client in Produit.get("liked_by", []):
        db['Produit'].update_one({"_id": ObjectId(Produit_id)},
                             {"$inc" : {"likes" : -1},
                              "$push" : {"liked_by" : Client}
                              })
    else :
        db['Produits'].update_one({"_id": ObjectId(Produit_id)},
                             {"$inc" : {"likes" : 1},
                              "$push" : {"liked_by" : Client}
                              })

    
    
    return redirect(request.referrer)
                             
                             




##Admin##
@app.route('/admin')
def admin():
    Produits_data = list(db["Produits"].find({}))
    Client_data = list(db["Client"].find({}))
    Api_data = list(db["Apiculteur"].find({}))
    if 'Client' in session and session['role'] == 'admin':
        return render_template('back/back_acceuil.html', Produits = Produits_data, Client = Client_data)
    else :
        return render_template('index.html', erreur = "Vous n'avez pas les droits d'accès", Produits = Produits_data, Client = Client_data, Apiculteur = Api_data)

@app.route('/admin/update_role/<user_id>', methods=['POST'])
def update_role(user_id):
    if 'Client' in session and session['role'] == 'admin':
        new_role = request.form.get('role')
        db['Client'].update_one({"_id" : ObjectId(user_id)}, {"$set" : {"role" : new_role}})

    return redirect(url_for('admin'))

@app.route('/admin/delete_user/<user_id>')
def delete_user(user_id):
    if 'Client' in session and session['role'] == 'admin':
        db['Client'].delete_one({"_id" : ObjectId(user_id)})

    return redirect(url_for('admin'))

    

@app.route('/erreur404')
def error_404():
    return render_template("front/erreur_404.html"), 404

@app.errorhandler(404)
def page_not_found(error):
    return render_template('front/erreur_404.html'), 404

    

app.run(host='0.0.0.0', port=81)
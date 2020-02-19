from flask import Flask
from flask_cors import CORS, cross_origin
import sys
		
app = Flask(__name__)
cors = CORS(app)

partie_en_cours=0 		



@app.route('/')
#@cross_origin()
def index():
    resultat= ""
    if (partie_en_cours==0):
        resultat= "Aucun joueur, vous etes le premier"
    if (partie_en_cours==1):
        resultat= "Un joueur en attente, voulez vous rejoindre sa partie?"
    if (partie_en_cours==2):
        resultat= "Une partie est en cours"

    return resultat

    

@app.route('/second')
def index2():
	return 'Hello, Flask sous  repertoire!'
		
if __name__ == '__main__':  
    app.run(debug=True)
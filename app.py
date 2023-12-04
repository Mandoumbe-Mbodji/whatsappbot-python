from flask import Flask, request, render_template, abort
import sett 
import services

app = Flask(__name__)

@app.route('/bienvenue', methods=['GET'])
def  bienvenue():
    return 'Bonjour chez assurema, de Flask'

@app.route('/formulaire')
def index():
    return render_template('login.html')
#############################   Webhookkkk ##################
@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        # Récupérer le token de vérification et le challenge de la requête
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Comparer le token avec celui défini dans vos paramètres de configuration
        if token == sett.token and challenge is not None:
            # Renvoyer le challenge pour compléter le processus de vérification
            return challenge
        else:
            # Renvoyer une erreur 403 si le token est incorrect ou si le challenge est manquant
            abort(403, 'Token incorrect ou challenge manquant')
    except Exception as e:
        # Renvoyer une erreur 403 en cas d'exception non gérée
        abort(403, str(e))
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number,messageId,name)
        return 'envoyé'

    except Exception as e:
        return 'non envoyé ' + str(e)

if __name__ == '__main__':
    app.run()



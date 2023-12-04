import requests
import sett
import json
import time

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'message non reconnu'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'message non traité'
    
    
    return text

def envoi_Msg_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("est envoyé ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'message envoyé', 200
        else:
            return 'erreur de l\'envoi du message', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {

            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("message de l'utilisateur: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "hola" in text:
        headers = {'Content-Type': 'application/json'}
        body = "Bonjour 👋 Bienvenue sur Assurema, comment pouvons-nous vous aider aujourd'hui ?"
        footer = "Equipe Assurema"
        options = ["✅ 1- Découvrez les packs", "✅ 2-  Renouvellement d'assurance","✅ 3- Trouver une agence","📅 4- Prendre rendez-vous pour une meilleur prise en charge"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "1" in text:
        body = "Veuillez choisir le pack d'assurance qui vous interesse, en choissant le numéro correspondant"
        footer = "Equipe Assurema"
        options = ["✅ 5- PACK GANALE", "✅ 6-  PACK SOPE","✅ 7- PACK VIP","✅ 8- A LA CARTE"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "5" in text:
        body = "Garantie PACK GNALE\n Responsabilité civile\n Défense sur recours\n Personnes transportés"
        footer = "Equipe Assurema"
        options = ["✅ 9- OUI je choisi ce pack .", "⛔ 10- non, merci"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "9" in text:
        sticker = sticker_Message(number, get_media_id("Parfait", "sticker"))
        textMessage = text_Message(number,"Genial, Veuillez renseigner vos informations et procéder au paiement.")

        envoi_Msg_whatsapp(sticker)
        envoi_Msg_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Formulaire")
        envoi_Msg_whatsapp(document)
        time.sleep(3)

        body = "Vous souhaitez prendre rendez-vous avec l'un de nos spécialistes pour discuter plus en détail de ces services ?"
        footer = "Equipe Assurema"
        options = ["✅ 11- OUI, ", "12- non, merci." ]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "11" in text :
        body = "Superbe. Veuillez sélectionner une date et une heure pour la réunion.:"
        footer = "Equipe Assurema"
        options = ["📅 13 : demain 10h00", "📅 14-  Après-deamin, 14h00", "📅 15- Lundi, 16h00"]

        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "13" in text:
        body = "Excellent, vous avez sélectionné la réunion de demain 10 heures. Je vous enverrai un rappel la veille. Vous avez besoin d'aide pour autre chose aujourd'hui ?"
        footer = "Equipe Assurema"
        options = ["✅ Oui, S'il vous plait", "❌ non, merci."]


        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "non, merci." in text:
        textMessage = text_Message(number,"Parfait ! N'hésitez pas à nous contacter si vous avez d'autres questions. N'oubliez pas que nous proposons également des services de reservations de restaurations pour la communauté - à plus tard ! 😊")
        list.append(textMessage)
    else :
        data = text_Message(number,"Je suis désolé, je n'ai pas compris ce que vous avez dit. Voulez-vous que je vous aide à choisir l'une de ces options ?")
        list.append(data)

    for item in list:
        envoi_Msg_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("33"):
        return "33" + s[2:]
    else:
        return s


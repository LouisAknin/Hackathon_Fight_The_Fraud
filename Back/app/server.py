from flask import Flask, request, jsonify
import requests
from Back.app.main import Message_analyzer
import pandas as pd

app = Flask(__name__)

PUSHBULLET_TOKEN = "o.xxxx"

import re
from datetime import datetime

def update_mockdata_ts(client_id, sender, text, analysis, score):
    """Ajoute un nouveau cas de fraude au fichier mockData.ts sans supprimer le reste du fichier"""
    file_path = "/Users/louisaknin/consejero-bank-suite/src/data/mockData.ts"

    # Nettoyage du texte
    escaped_text = (
        text.replace('"', '\\"')
        .replace('\n', ' ')
        .replace('\r', '')
        .strip()
    )

    # Création d'une nouvelle entrée FraudData
    new_entry = (
        "  {\n"
        f'    id: "F{int(datetime.now().timestamp())}",\n'
        f'    clientId: "{client_id}",\n'
        f'    scammerNumber: "{sender}",\n'
        f'    messageText: "{escaped_text}",\n'
        f'    analysis: "{analysis}",\n'
        f'    score: {float(score):.2f},\n'
        f'    date: "{datetime.now().strftime("%Y-%m-%d")}",\n'
        f'    reviewed: false,\n'
        "  },"
    )

    # Lecture du contenu complet du fichier
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Recherche précise du bloc mockFraudData
    pattern = r"(export const mockFraudData: FraudData\[\] = \[\n)([\s\S]*?)(\n\];)"
    match = re.search(pattern, content)

    if not match:
        print("Impossible de trouver le tableau mockFraudData.")
        return

    before_block = content[:match.start(2)]
    current_entries = match.group(2).rstrip()
    after_block = content[match.end(2):]

    # Vérifie si le message existe déjà (évite les doublons)
    if sender in current_entries and escaped_text in current_entries:
        print("Entrée déjà existante, pas d’ajout.")
        return

    # Ajoute la nouvelle entrée avant la fin du tableau
    updated_entries = f"{current_entries}\n{new_entry}"
    updated_content = f"{before_block}{updated_entries}{after_block}"

    # Écrit le nouveau contenu complet dans le fichier
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("Nouvelle fraude ajoutée à mockData.ts sans supprimer le reste.")


# Fonction pour envoyer une notification Pushbullet
def send_pushbullet_notification(title, body):
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": PUSHBULLET_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "type": "note",
        "title": title,
        "body": body
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Notification Pushbullet envoyée !")
    else:
        print("Erreur Pushbullet :", response.status_code, response.text)

# Route principale pour les messages
@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json(force=True)
    print("Notification brute reçue :", data)

    raw_msg = data.get("message", "")
    sender, text = None, None

    # --- Parsing du message ---
    if raw_msg.startswith("From:"):
        try:
            parts = raw_msg.split("\n", 1)
            sender = parts[0].replace("From:", "").strip()
            text = parts[1].strip() if len(parts) > 1 else ""
        except Exception as e:
            print("Erreur parsing :", e)

    print(f"SMS reçu de : {sender}")
    print(f"Contenu : {text}")

    analyser = Message_analyzer(text)
    answer = analyser.analyse()

    explain_sentiment = analyser.explanation_sentiment

    print(answer, explain_sentiment)

    if answer == "spam":
        title = f"Spam frauduleux de {sender}"
        body = text

        update_mockdata_ts("C003", sender, text, explain_sentiment, 0.91)

        send_pushbullet_notification(title, explain_sentiment)
    else:
        title = f"Pas de spam de {sender}"
        body = text
        send_pushbullet_notification(title, body)
    """
    # --- Envoi de la notification ---
    if sender and text:
        title = f"Nouveau SMS de {sender
        body = text
        send_pushbullet_notification(title, body)"""

    # Réponse HTTP
    return jsonify({
        "status": "ok",
        "sender": sender,
        "text": text
    })

@app.route('/', methods=['GET'])
def home():
    return "Serveur Python + Pushbullet opérationnel !"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

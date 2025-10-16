import json
import boto3
import re

session = boto3.Session()

bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client

bedrock_model_id = "us.amazon.nova-lite-v1:0" #set the foundation model

""" 
import argparse

parser = argparse.ArgumentParser(description="Build fraud-context sentiment prompt")
parser.add_argument("--message", "-m", required=True, help="Message to analyze (put in quotes)")
args = parser.parse_args()
sms = args.message 
"""


def extract_json_and_score(response_text):
    """
    Nettoie la réponse du modèle, extrait le JSON valide,
    et retourne le dictionnaire Python + le final_score.
    """
    # 1. Supprime les balises Markdown et espaces parasites
    cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE).strip()

    try:
        # 2. Convertit en dict Python
        data = json.loads(cleaned)
        
        # 3. Extrait le score final
        explanation = data.get("explanation", None)
        final_score = data.get("fraud_risk", None)
        return data, final_score , explanation

    except json.JSONDecodeError as e:
        print(" JSON decoding failed:", e)
        print("Cleaned text was:\n", cleaned)
        return None, None , None


def sentiment_detection(sms):
    prompt = f"""
    You are an expert in fraud detection and linguistic forensics.
    Your goal is to evaluate how likely the following message is to be part of a fraud, scam, or social engineering attempt.

    Analyze the message : '{sms}' based on the following dimensions:
    1. **Overall sentiment** — classify as Positive / Negative / Neutral / Mixed.
    2. **Fraud score** — numeric value from 0 (certainly not fraud) to 100 (almost certainly fraud).
    3. **Fraud risk category** — low / medium / high / critical.
    - This score should take into account: stress, urgency, manipulative tone, emotional signals, and fraud_score intensity.
    4. **Concise explanation (3 sentences max)** — justify your analysis with linguistic and psychological reasoning.

    Expected output format (strict JSON):
    ```json
    {{
    "sentiment": "Positive | Negative | Neutral | Mixed",
    "fraud_score": 0_to_100,
    "fraud_risk": "low | medium | high | critical",
    "explanation": "Concise explenation in french, why it is a fraud, very sharp, one phrase maximum, explain why the content is a fraud, not the tone"
    }}"""
    messages = [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ]

    body = json.dumps({
            "schemaVersion": "messages-v1",
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": 1024,
                "topP": 0.5,
                "topK": 20,
                "temperature": 0.0
            }
        }) #build the request payload

    response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') #send the payload to Amazon Bedrock

    response_body = json.loads(response.get('body').read()) # read the response

    response_text = response_body["output"]["message"]["content"][0]["text"] #extract the text from the JSON response

    #print(response_text)
    _json, sentiment_detection, explanation = extract_json_and_score(response_text)

    return sentiment_detection , explanation
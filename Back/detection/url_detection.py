import json
import boto3

session = boto3.Session()

bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client

bedrock_model_id = "us.amazon.nova-lite-v1:0" #set the foundation model

import re

def extract_json_and_score(response_text):
    cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE).strip()

    try:
        data = json.loads(cleaned)
        
        final_score = data.get("url_risk", None)
        explanation = data.get("explanation", None)
        return data, final_score, explanation

    except json.JSONDecodeError as e:
        print(" JSON decoding failed:", e)
        print("Cleaned text was:\n", cleaned)
        return None, None , None


def url_detection(sms):
    prompt_url = f"""
You are an expert in fraud detection, linguistic forensics, and URL threat assessment.

Task A — URL detection:
1. Detect whether the message contains one or more URLs (http, https, www, or shortened links like bit.ly, t.co, tinyurl).
2. If one or more URLs are present, extract the most relevant URL (the clickable/explicit link or the one most likely used for phishing).
3. If no URL is present, set `url_present` to false and `url` to null.

Task B — URL maliciousness scoring (only if a URL is present):
Assess the extracted URL using only visible structural and textual indicators (do NOT perform network requests or external lookups). Consider signals such as:
- IP address instead of domain,
- unusually long or complex path/query parameters,
- excessive encoded characters,
- use of URL shorteners,
- lookalike domains or brand misspellings,
- uncommon or rare TLDs,
- mismatched display text vs actual URL,
- use of credential/urgent words (login, verify, account, secure),
- presence in a context suggesting attachments or downloads.

Produce:
- `url_present`: true/false
- `url`: the extracted URL string or null
- `url_risk`: "safe" | "unknown" | "weird" | "fraud"
- `explanation`: concise justification (max 2 sentences) citing the main structural cues.

Output **strict JSON only**, no extra text, no markdown, no commentary.

Here's the message to analyse: {sms}.

"""

    messages = [
            {
                "role": "user",
                "content": [
                    {"text": prompt_url}
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
    _json, url_detection, explanation  = extract_json_and_score(response_text)

    return url_detection , explanation       

import requests
from flask import current_app


def translate(text, target_language="English"):
    if 'GEMINI_API_KEY' not in current_app.config or \
            not current_app.config['GEMINI_API_KEY']:
        return 'Error: Translation service is not configured.'

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/gemini-2.5-flash-lite:generateContent"
        f"?key={current_app.config['GEMINI_API_KEY']}"
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    f"Translate this text to {target_language}. "
                    f"Only return translated text:\n{text}"
                )
            }]
        }]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return 'Error: Translation service failed.'

    return response.json()['candidates'][0]['content']['parts'][0]['text']


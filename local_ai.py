import requests

LOCAL_AI_URL = "https://zone-observations-gaps-reporter.trycloudflare.com/v1/chat/completions"


def ask_local_ai(messages):

    response = requests.post(
        LOCAL_AI_URL,
        json={
            "model": "local-model",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 150
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]

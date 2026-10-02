import os
import requests
import gradio as gr

API_KEY = os.environ["OPENROUTER_API_KEY"]

def chat(message, history):
    messages = [
        {
            "role": "system",
            "content": "You are my personal AI assistant. Answer clearly and helpfully."
        }
    ]

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": messages
        },
        timeout=60
    )

    data = response.json()

    if response.status_code != 200:
        return "Error: " + str(data)

    return data["choices"][0]["message"]["content"]


demo = gr.ChatInterface(
    fn=chat,
    title="My Personal AI",
    description="My own AI assistant"
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)

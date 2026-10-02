import os
import json
import requests
import gradio as gr

API_KEY = os.environ["OPENROUTER_API_KEY"]

MEMORY_FILE = "memory.json"

SYSTEM_PROMPT = """
You are My Personal AI, a smart, friendly personal AI assistant.

- Understand Bangla, English and Banglish.
- Reply naturally in the user's language/style.
- Help with study, coding, projects, writing and everyday questions.
- Give clear step-by-step explanations when useful.
- Never make up facts.
"""

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def chat(message, history):

    memory = load_memory()

    memory_text = "\n".join(
        f"- {item}" for item in memory
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
            + "\n\nThings you remember about the user:\n"
            + (memory_text if memory_text else "Nothing yet.")
        }
    ]

    for msg in history:
        role = msg.get("role")
        content = msg.get("content")

        if isinstance(content, list):
            text_parts = []

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)

            content = "".join(text_parts)

        if role in ["user", "assistant"] and content:
            messages.append({
                "role": role,
                "content": content
            })

    messages.append({
        "role": "user",
        "content": message
    })

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

    try:
        data = response.json()
    except:
        return "Server error."

    if response.status_code != 200:
        return "OpenRouter Error: " + str(data)

    try:
        answer = data["choices"][0]["message"]["content"]
    except:
        return "AI response পাওয়া যায়নি: " + str(data)

    # Simple memory detection
    lower = message.lower()

    memory_triggers = [
        "remember that",
        "remember this",
        "my name is",
        "amar nam",
        "আমার নাম",
        "মনে রাখো",
        "মনে রেখো"
    ]

    if any(trigger in lower for trigger in memory_triggers):

        if message not in memory:
            memory.append(message)
            save_memory(memory)

    return answer


demo = gr.ChatInterface(
    fn=chat,
    title="My Personal AI",
    description="My own AI assistant"
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)

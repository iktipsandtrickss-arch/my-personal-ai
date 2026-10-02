import os
import requests
import gradio as gr

from memory import save_memory, get_memories

API_KEY = os.environ["OPENROUTER_API_KEY"]

# For now, this AI is only for you.
USER_ID = "ishtiaq"

SYSTEM_PROMPT = """
You are My Personal AI, a smart, friendly personal AI assistant.

- Understand Bangla, English and Banglish.
- Reply naturally in the user's language/style.
- Help with study, coding, projects, writing and everyday questions.
- Give clear step-by-step explanations when useful.
- Never make up facts.
- Use the user's saved memories when they are relevant.
- Do not mention that you have a memory system unless the user asks.
"""


def chat(message, history):

    # Load memories from Supabase
    try:
        memories = get_memories(USER_ID)

        memory_text = "\n".join(
            f"- {item['memory']}"
            for item in memories
            if item.get("memory")
        )

    except Exception as e:
        memory_text = ""
        print("Memory load error:", e)

    # Build messages
    messages = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n\nThings you remember about the user:\n"
                + (memory_text if memory_text else "Nothing yet.")
            )
        }
    ]

    # Add previous conversation history
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

    # Add current user message
    messages.append({
        "role": "user",
        "content": message
    })

    # Send request to OpenRouter
    try:

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

    except Exception as e:

        return "Connection error: " + str(e)

    # Read response
    try:

        data = response.json()

    except:

        return "Server error."

    # OpenRouter error
    if response.status_code != 200:

        return "OpenRouter Error: " + str(data)

    # Get AI answer
    try:

        answer = data["choices"][0]["message"]["content"]

    except:

        return "AI response পাওয়া যায়নি: " + str(data)

    # -------------------------------------------------
    # MEMORY DETECTION
    # -------------------------------------------------

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

        try:

            save_memory(USER_ID, message)

            print("Memory saved:", message)

        except Exception as e:

            print("Memory save error:", e)

    return answer


# -------------------------------------------------
# GRADIO INTERFACE
# -------------------------------------------------

demo = gr.ChatInterface(
    fn=chat,
    title="My Personal AI",
    description="My own AI assistant"
)


# -------------------------------------------------
# START SERVER
# -------------------------------------------------

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)

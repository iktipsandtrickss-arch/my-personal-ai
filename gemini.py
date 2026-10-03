import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(messages):

    contents = []

    for message in messages:

        role = message.get("role")
        content = message.get("content", "")

        if isinstance(content, str):

            contents.append(
                f"{role.upper()}:\n{content}"
            )

        elif isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":

                        text_parts.append(
                            item.get("text", "")
                        )

            if text_parts:

                contents.append(
                    f"{role.upper()}:\n"
                    + "\n".join(text_parts)
                )

    prompt = "\n\n".join(contents)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

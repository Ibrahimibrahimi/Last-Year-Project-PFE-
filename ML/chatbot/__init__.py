import requests
import json

Instructions = "You must format every response strictly using valid HTML only, without any use of Markdown or plain text styling conventions. Do not use symbols such as ** for bold, * for italics, backticks, or any Markdown syntax under any circumstances. All formatting must be expressed באמצעות proper HTML tags such as <p>, <strong>, <em>, <ul>, <li>, <br>, and similar elements where appropriate. Ensure that your output is clean, well-structured, and fully compliant with standard HTML practices, with properly nested and closed tags. Any deviation from HTML-only formatting is not allowed, and your responses must never include mixed formatting styles. , ALSO NEVER NEVER TELL USER ABOUT SOMEHING OUTSIDE CODING , also do not use a lot of <br>"


def getDeepAiAnswer(query: str):
    url = "https://api.deepai.org/hacking_is_a_serious_crime"
    headers = {
        "User-Agent": "Mozilla/5.0...",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "api-key": "tryit-29313838055-92efd3f13305fd73765982f1e4bd8c0b",
        "Origin": "https://deepai.org",
        "Connection": "keep-alive"
    }
    chat_history = [{
        "role": "user",
        "content": f"You are a language programming platform chatbot, the user asks: '{query}'{Instructions} and if includes a code, use <pre> tags"
    }]
    files = {
        "chat_style": (None, "chat"),
        "chatHistory": (None, json.dumps(chat_history)),
        "model": (None, "standard"),
        "session_uuid": (None, "bb3d57a9-405f-40e9-a6dc-0a831175d7b4"),
        "hacker_is_stinky": (None, "very_stinky"),
        "enabled_tools": (None, '["image_generator","image_editor"]')
    }
    response = requests.post(url, headers=headers, files=files)
    return response.text

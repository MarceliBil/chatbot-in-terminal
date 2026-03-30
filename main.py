import requests
import json

API = "http://localhost:11434/api/chat"
MODEL = "phi3"

SYSTEM_PROMPT = "If greeting → reply with greeting. Otherwise short answer."


def create_messages():
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


def get_user_input():
    return input("You: ")


def call_model(messages):
    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(API, json=data)

    if response.status_code != 200:
        return "Error: Ollama not responding"

    return response.json()["message"]["content"]


def save_messages(messages):
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def chat():
    messages = create_messages()

    while True:
        prompt = get_user_input()

        if prompt.lower() == "exit":
            break

        messages.append({"role": "user", "content": prompt})

        reply = call_model(messages)

        messages.append({"role": "assistant", "content": reply})

        save_messages(messages)

        return f"AI: {reply}"


if __name__ == "__main__":
    print(chat())
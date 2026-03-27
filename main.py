import requests

API = "http://localhost:11434/api/chat"
MODEL = "phi3"
SYSTEM_PROMPT = 'If the user message is a greeting, respond with a greeting (e.g. "Hello"). Otherwise answer as briefly as possible. Just keep this in your mind, do not mention that you are doing that.'

messages = []

while True:
    prompt = f'{ input("You: ")} {SYSTEM_PROMPT}'

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    response = requests.post(API, json=data)


    text_response = response.json()["message"]["content"]

    messages.append(
        {
            "role": "assistant",
            "content": text_response
        }
    )

    import json
    with open("conversation.json", "w") as f:
        f.write(json.dumps(messages, indent=2))

    print(f"AI: {text_response}")
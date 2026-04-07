import requests
import psycopg2
import uuid
import os
from dotenv import load_dotenv
import time

load_dotenv()

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

    try:
        response = requests.post(API, json=data, timeout=10)

        if response.status_code != 200:
            print(f"Model HTTP error: {response.status_code}")
            return None

        json_data = response.json()
        return json_data.get("message", {}).get("content")

    except requests.exceptions.Timeout:
        print("Model timeout")
        return None

    except requests.exceptions.ConnectionError:
        print("Model connection error")
        return None

    except Exception as err:
        print(f"Unexpected model error: {err}")
        return None


def call_model_with_retry(messages, attempts=3, base_delay=0.7):
    for attempt in range(attempts):
        reply = call_model(messages)
        if reply is not None:
            return reply

        if attempt < attempts - 1:
            time.sleep(base_delay * (2 ** attempt))

    return None


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def create_conversation():
    conversation_id = str(uuid.uuid4())

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO conversations (id) VALUES (%s)",
                (conversation_id,)
            )

    return conversation_id


def save_message(conversation_id, role, content, seq):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (conversation_id, role, content, seq)
                VALUES (%s, %s, %s, %s)
                """,
                (conversation_id, role, content, seq)
            )


def trim_messages(messages, keep_last=20):
    if not messages:
        return messages
    system = messages[0] if messages[0].get("role") == "system" else None
    rest = messages[1:] if system else messages
    trimmed = rest[-keep_last:]
    return ([system] + trimmed) if system else trimmed


def chat():
    messages = create_messages()
    conversation_id = create_conversation()
    seq = 0

    while True:
        prompt = get_user_input()

        if prompt.lower() == "exit":
            break

        user_msg = {"role": "user", "content": prompt}

        seq += 1
        save_message(conversation_id, "user", prompt, seq)

        candidate_messages = messages + [user_msg]
        reply = call_model_with_retry(
            trim_messages(candidate_messages, keep_last=20),
            attempts=3,
            base_delay=0.7,
        )

        if reply is None:
            print("AI: [error – brak odpowiedzi]")
            continue
        
        messages.append(user_msg)

        seq += 1
        save_message(conversation_id, "assistant", reply, seq)
        messages.append({"role": "assistant", "content": reply})
        print(f"AI: {reply}")


if __name__ == "__main__":
    chat()
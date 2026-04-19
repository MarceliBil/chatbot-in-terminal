# Chatbot in Terminal (Ollama + Postgres)

This project runs a simple terminal-based chat and stores conversations in Postgres.


## Requirements

* Docker Desktop
* Ollama installed on Windows


## Quick Start

1. Download the model and start Ollama:

    ```bash
    ollama pull phi3
    ollama serve
    ```
    
    * make sure Ollama is running at `http://localhost:11434`


2. Copy `.env.example` to `.env`.

3. Run everything with a single command:

   ```bash
   docker compose run --rm app

The application will connect to Postgres running in Docker and to Ollama on the host.

## Viewing conversations history in pgAdmin

In `docker-compose.yml`, the Postgres port is exposed to the host, so you can connect to the database server using a GUI:

* host: `localhost`
* port: `5433`
* database: `chat_app`
* user: `postgres`
* password: value of `postgres`

Tables are created automatically from the `tables.sql` file on first startup (when the Postgres volume is empty).

### Notes

- Inside the Docker container, `API` points to `http://host.docker.internal:11434/api/chat`.  
This special address lets the container access Ollama running on your host machine (Windows/WSL2).  
Using `localhost` inside the container would point to the container itself, not the host.
- Currently, the database serves only as a backlog for storing conversations. It is not yet used for loading past messages into the chat. Features like conversation continuation may be added in the future.
- The current Docker setup is supported only on Windows (including WSL2) and macOS. Linux support is not yet configured.

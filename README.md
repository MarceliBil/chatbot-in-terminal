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


1. Copy and configure the environment file:

   * copy `.env.example` to `.env`
   * set `DB_NAME`, `DB_USER`, `DB_PASSWORD` (you can keep the defaults)

2. Run everything with a single command:

   ```bash
   docker compose run --rm app

The application will connect to Postgres running in Docker and to Ollama on the host.

## Viewing messages in pgAdmin

In `docker-compose.yml`, the Postgres port is exposed to the host, so you can connect using a GUI:

* host: `localhost`
* port: `5432`
* database: value of `DB_NAME` from `.env`
* user: value of `DB_USER` from `.env`
* password: value of `DB_PASSWORD` from `.env`

Tables are created automatically from the `tables.sql` file on first startup (when the Postgres volume is empty).

If you modify `tables.sql` and want the initialization to run again, remove the volume:

```bash
docker compose down -v
```

### Note

Inside the Docker container, `API` points to `http://host.docker.internal:11434/api/chat`.  
This special address lets the container access Ollama running on your host machine (Windows/WSL2).  
Using `localhost` inside the container would point to the container itself, not the host.

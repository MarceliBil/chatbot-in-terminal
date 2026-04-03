CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS conversations (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  title        TEXT,
  system_prompt TEXT,
  model        TEXT,
  metadata     JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS messages (
  id              BIGSERIAL PRIMARY KEY,
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  seq             INTEGER NOT NULL,
  role            TEXT NOT NULL CHECK (role IN ('system','user','assistant')),
  content         TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  metadata        JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT messages_conversation_seq_uniq UNIQUE (conversation_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_seq
  ON messages (conversation_id, seq);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_created
  ON messages (conversation_id, created_at);

-- opcjonalnie: auto-update updated_at w conversations gdy wpada nowa wiadomość
CREATE OR REPLACE FUNCTION touch_conversations_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE conversations SET updated_at = now() WHERE id = NEW.conversation_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_messages_touch_conversations ON messages;
CREATE TRIGGER trg_messages_touch_conversations
AFTER INSERT ON messages
FOR EACH ROW EXECUTE FUNCTION touch_conversations_updated_at();
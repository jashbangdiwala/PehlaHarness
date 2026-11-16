from pathlib import Path

# Absolute paths built from this file's location, so the bot works from any folder.
REPO_ROOT = Path(__file__).resolve().parent

# Model ID copied from openrouter.ai/models.
MODEL = "moonshotai/kimi-k3.1-pro"

# Longest reply the model may write. OpenRouter checks your credit against the
# worst-case cost before every call: 2048 tokens of Kimi K3.1 Pro is about $0.02.
MAX_TOKENS = 2048

# How many earlier turns (one message + its reply) the EA sends with each call.
# More history means better answers and a bigger bill: every turn is paid for on every call.
HISTORY_TURNS = 10

DB_PATH = REPO_ROOT / "Database" / "ea.db"
ALLOWED_ID_PATH = REPO_ROOT / "allowed_id.txt"

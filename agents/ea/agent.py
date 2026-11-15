from pathlib import Path

from core.events import log
from core.gateway import ask

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "system.md"
DOMAIN = "ea"

def respond(text):
    system = PROMPT_PATH.read_text().strip()
    mid = log("message", {"text": text}, domain=DOMAIN)
    reply = ask([
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ], parent_id=mid)
    log("reply", {"text": reply}, domain=DOMAIN, parent_id=mid)
    return reply

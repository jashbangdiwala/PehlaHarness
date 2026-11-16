from pathlib import Path

from config import HISTORY_TURNS
from core.events import log, recent
from core.gateway import ask

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "system.md"
DOMAIN = "ea"


def history(turns=HISTORY_TURNS):
    """The last `turns` exchanges as user/assistant messages, oldest first.

    A turn is one message plus the reply that points back at it. A message
    that never got a reply (for example, the model call failed) is skipped.
    """
    # Fetch extra rows so that unanswered messages don't eat into the cap.
    events = recent(DOMAIN, ("message", "reply"), limit=turns * 4)
    messages = {e["id"]: e for e in events if e["kind"] == "message"}
    pairs = [(messages[e["parent_id"]], e) for e in events
             if e["kind"] == "reply" and e["parent_id"] in messages]
    out = []
    for msg, reply in pairs[-turns:]:
        out.append({"role": "user", "content": msg["payload"]["text"]})
        out.append({"role": "assistant", "content": reply["payload"]["text"]})
    return out


def respond(text):
    system = PROMPT_PATH.read_text().strip()
    past = history()
    mid = log("message", {"text": text}, domain=DOMAIN)
    reply = ask([{"role": "system", "content": system}, *past,
                 {"role": "user", "content": text}], parent_id=mid)
    log("reply", {"text": reply}, domain=DOMAIN, parent_id=mid)
    return reply

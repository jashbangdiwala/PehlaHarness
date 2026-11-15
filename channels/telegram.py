import os, time, httpx, keyring
from agents.ea.agent import respond
from config import ALLOWED_ID_PATH
from core.events import log

TOKEN = keyring.get_password("ea", "telegram")
API = f"https://api.telegram.org/bot{TOKEN}"
ID_FILE = ALLOWED_ID_PATH
ALLOWED = int(open(ID_FILE).read().strip()) if os.path.exists(ID_FILE) else None

def scrub(e):
    return repr(e).replace(TOKEN, "***")

def send(chat_id, text):
    httpx.post(f"{API}/sendMessage",
               json={"chat_id": chat_id, "text": text}, timeout=30)

def handle(update):
    msg = update.get("message")
    if not msg or "text" not in msg:
        return
    uid = msg["from"]["id"]
    if ALLOWED is None:
        print(f"Your Telegram user ID is {uid}. Put it in {ID_FILE.name} and restart.")
        log("dropped", {"reason": "no allowlist yet"})
        return
    if uid != ALLOWED:
        log("dropped", {"reason": "not allowed", "uid": uid,
                        "name": msg["from"].get("first_name"),
                        "text": msg["text"]})   # silent: no reply
        return
    reply = respond(msg["text"])
    send(msg["chat"]["id"], reply)

def main():
    offset = None
    print("polling... (Ctrl-C to stop)")
    while True:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        try:
            r = httpx.get(f"{API}/getUpdates", params=params, timeout=40)
            for u in r.json().get("result", []):
                offset = u["update_id"] + 1
                try:
                    handle(u)
                except Exception as e:
                    log("error", {"err": scrub(e)})
        except httpx.HTTPError as e:
            log("error", {"err": scrub(e)})
            time.sleep(5)

if __name__ == "__main__":
    main()
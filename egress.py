import re, time, httpx, keyring
from events import log

# Use a model ID copied from openrouter.ai/models. This is an example, verify it exists.
MODEL = "meta-llama/llama-3.3-70b-instruct"

PATTERNS = [
    (re.compile(r"\b(?:\d[ -]?){13,19}\b"), "[CARD]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"), "[KEY]"),
    # add your own: national ID formats, account numbers, etc.
]

def redact(text):
    for pat, tag in PATTERNS:
        text = pat.sub(tag, text)
    return text

def ask(messages, parent_id=None):
    safe = [{"role": m["role"], "content": redact(m["content"])} for m in messages]
    key = keyring.get_password("ea", "openrouter")
    t = time.time()
    r = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": MODEL, "messages": safe,
              "provider": {"data_collection": "deny", "allow_fallbacks": False}},
        timeout=60)
    r.raise_for_status()
    data = r.json()
    text = data["choices"][0]["message"]["content"]
    log("model_call", {"model": MODEL, "secs": round(time.time() - t, 2),
                       "usage": data.get("usage")}, parent_id=parent_id)
    return text

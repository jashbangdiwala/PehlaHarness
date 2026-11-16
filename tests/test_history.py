import sqlite3

import pytest

from agents.ea import agent
from core import events


@pytest.fixture
def temp_db(monkeypatch, tmp_path):
    """Point the event log at an empty database in a temp folder."""
    conn = sqlite3.connect(tmp_path / "test.db")
    events.create_table(conn)
    monkeypatch.setattr(events, "db", conn)
    return conn


def add_turn(user, bot, domain="ea"):
    mid = events.log("message", {"text": user}, domain=domain)
    events.log("reply", {"text": bot}, domain=domain, parent_id=mid)


def contents(messages):
    return [m["content"] for m in messages]


def test_recent_returns_oldest_first(temp_db):
    events.log("message", {"text": "a"}, domain="ea")
    events.log("message", {"text": "b"}, domain="ea")
    events.log("message", {"text": "c"}, domain="ea")
    rows = events.recent("ea", ("message",), limit=2)
    assert [r["payload"]["text"] for r in rows] == ["b", "c"]


def test_history_is_oldest_first_as_user_and_assistant(temp_db):
    add_turn("first", "one")
    add_turn("second", "two")
    assert agent.history(10) == [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "one"},
        {"role": "user", "content": "second"},
        {"role": "assistant", "content": "two"},
    ]


def test_history_is_capped(temp_db):
    for i in range(15):
        add_turn(f"q{i}", f"a{i}")
    history = agent.history(10)
    assert len(history) == 20
    assert history[0]["content"] == "q5"
    assert history[-1]["content"] == "a14"


def test_history_ignores_other_domains(temp_db):
    add_turn("mine", "yes")
    add_turn("not mine", "no", domain="core")
    assert contents(agent.history(10)) == ["mine", "yes"]


def test_history_skips_a_message_that_got_no_reply(temp_db):
    add_turn("before", "ok")
    events.log("message", {"text": "model call failed"}, domain="ea")
    add_turn("after", "ok again")
    assert contents(agent.history(10)) == ["before", "ok", "after", "ok again"]


def test_respond_sends_system_then_history_then_new_message(temp_db, monkeypatch):
    add_turn("my name is Jash", "Nice to meet you, Jash.")
    sent = {}

    def fake_ask(messages, parent_id=None):
        sent["messages"] = messages
        return "Your name is Jash."

    monkeypatch.setattr(agent, "ask", fake_ask)
    assert agent.respond("what's my name?") == "Your name is Jash."
    roles = [m["role"] for m in sent["messages"]]
    assert roles == ["system", "user", "assistant", "user"]
    assert sent["messages"][-1]["content"] == "what's my name?"

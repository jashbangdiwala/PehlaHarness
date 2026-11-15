from core.gateway import redact

def test_card_is_redacted():
    assert "4111 1111 1111 1111" not in redact("pay 4111 1111 1111 1111 now")

def test_key_is_redacted():
    assert "sk-abcdefghijklmnop1234" not in redact("my key sk-abcdefghijklmnop1234")

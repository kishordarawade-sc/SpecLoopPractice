import re

from greet import log_greeting
from greet import build_greeting


def test_greet_with_name():
    assert build_greeting("Alice") == "Hello, Alice!"

def test_greet_without_name():
    assert build_greeting("") == "Hello, World!" 

def test_greet_with_multiword_name():
    assert build_greeting("Alice Smith") == "Hello, Alice Smith!"   

def test_greet_trims_whitespace():
    assert build_greeting("  Alice  ") == "Hello, Alice!"

def test_greet_default():
        assert build_greeting(None) == "Hello, World!"  

def test_greet_whitespace_only_defaults():
    assert build_greeting("   ") == "Hello, World!" 

from greet import notify


def test_notify_posts_when_webhook_configured():
    assert notify("Hello, Alice!", "https://hooks.slack.test/abc123") is True


def test_notify_skips_when_no_webhook():
    assert notify("Hello, World!", None) is False


# spec: specs/003-greet-log/spec.md#US1-S1
def test_log_greeting_appends_timestamped_line(tmp_path):
    log_path = tmp_path / "greetings.log"
    log_greeting("Hello, Alice!", log_path)

    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z Hello, Alice!$", lines[0])



import os
from app.utilities.general import format_datetime, load_env_variable
from datetime import datetime

def test_format_datetime():
    dt = datetime(2024, 12, 1, 12, 0, 0)
    assert format_datetime(dt) == "2024-12-01 12:00:00"

def test_load_env_variable(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "value")
    assert load_env_variable("TEST_KEY") == "value"
    assert load_env_variable("NON_EXISTENT_KEY", "default") == "default"


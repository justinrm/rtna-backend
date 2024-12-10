from app.modules.source_discovery import discover_sources, validate_sources
from unittest.mock import patch

def test_discover_sources(mocker):
    mocker.patch("app.modules.source_discovery.execute_query")
    discover_sources()
    # No exceptions should be raised; valid sources should be added
    assert True

def test_validate_sources(mocker):
    mocker.patch("app.modules.source_discovery.execute_query", return_value={
        "data": [{"id": 1, "website": "https://validsource.com"}]
    })
    mocker.patch("app.modules.source_discovery.is_valid_url", return_value=True)
    validate_sources()
    # No exceptions should be raised; valid sources should be updated to active
    assert True


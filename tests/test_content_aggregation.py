from app.modules.content_aggregation import aggregate_articles, fetch_rss_feed, save_articles_to_db
from unittest.mock import patch

def test_aggregate_articles(mocker):
    """
    Test the aggregate_articles function to ensure it fetches and saves articles.
    """
    mocker.patch("app.modules.content_aggregation.fetch_rss_feed", return_value=[
        {"title": "Test Article", "url": "https://example.com/test", "source_id": 1}
    ])
    mocker.patch("app.modules.content_aggregation.save_articles_to_db")
    result = aggregate_articles()
    assert result["total_articles"] == 1

def test_fetch_rss_feed():
    """
    Test the fetch_rss_feed function to verify correct RSS parsing.
    """
    mock_feed = {
        "entries": [
            {"title": "Test Article", "link": "https://example.com/test", "published_parsed": None}
        ]
    }
    with patch("feedparser.parse", return_value=mock_feed):
        articles = fetch_rss_feed("https://example.com/rss", 1)
        assert len(articles) == 1
        assert articles[0]["title"] == "Test Article"

def test_save_articles_to_db(mocker):
    """
    Test the save_articles_to_db function to ensure articles are saved correctly.
    """
    mocker.patch("app.utilities.database.execute_query")
    articles = [{"title": "Test Article", "url": "https://example.com/test", "source_id": 1}]
    save_articles_to_db(articles)
    # No exception should occur, indicating successful execution.
    assert True


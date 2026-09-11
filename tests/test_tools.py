import pytest
from unittest.mock import patch, MagicMock
from tools import scrape_url, web_search

def test_scrape_url_strips_scripts_and_styles():
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <script>alert('bad');</script>
            <style>body { color: red; }</style>
            <header>Header Nav</header>
            <main>
                <h1>Deep Research Topic</h1>
                <p>This is crucial research content that should be extracted.</p>
            </main>
            <footer>Footer Links</footer>
        </body>
    </html>
    """
    mock_resp = MagicMock()
    mock_resp.text = html_content
    mock_resp.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_resp):
        result = scrape_url.invoke({"url": "https://example.com/research"})
        assert "Deep Research Topic" in result
        assert "crucial research content" in result
        assert "alert('bad')" not in result
        assert "body { color: red; }" not in result

def test_scrape_url_handles_network_failure():
    with patch("requests.get", side_effect=Exception("Connection timed out")):
        result = scrape_url.invoke({"url": "https://broken-link.com"})
        assert "Could not scrape URL" in result
        assert "Connection timed out" in result

def test_web_search_formats_results():
    mock_client = MagicMock()
    mock_client.search.return_value = {
        "results": [
            {
                "title": "Quantum Supremacy in 2025",
                "url": "https://example.com/quantum",
                "content": "Significant advances have been made in quantum error mitigation."
            }
        ]
    }
    with patch("tools._get_tavily_client", return_value=mock_client):
        result = web_search.invoke({"query": "quantum computing"})
        assert "Quantum Supremacy in 2025" in result
        assert "https://example.com/quantum" in result
        assert "quantum error mitigation" in result

import pytest
from unittest.mock import MagicMock
from pipeline import _extract_content

def test_extract_content_from_langgraph_dict():
    mock_msg = MagicMock()
    mock_msg.content = "Extracted agent answer"
    output = {"messages": [mock_msg]}
    assert _extract_content(output) == "Extracted agent answer"

def test_extract_content_from_agent_executor():
    output = {"output": "Agent final response"}
    assert _extract_content(output) == "Agent final response"

def test_extract_content_fallback():
    assert _extract_content("Direct text output") == "Direct text output"

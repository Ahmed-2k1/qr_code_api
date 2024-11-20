"""
This module contains pytest fixtures for setting up test clients and obtaining access tokens.
"""

import pytest
from httpx import AsyncClient
from app.main import app  # Adjust import path as necessary


@pytest.fixture
async def async_test_client():
    """
    Provides an asynchronous HTTP client for testing.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
async def get_access_token_for_test(async_test_client):  # pylint: disable=redefined-outer-name
    """
    Provides an access token for authenticated API requests.
    """
    form_data = {"username": "admin", "password": "secret"}
    response = await async_test_client.post("/token", data=form_data)
    return response.json()["access_token"]

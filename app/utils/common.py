import logging.config
import os
import base64
from typing import List
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from app.config import ADMIN_PASSWORD, ADMIN_USER, ALGORITHM, SECRET_KEY
import validators  # Ensure this package is installed
from urllib.parse import urlparse, urlunparse

# Load environment variables from .env file for security and configuration
load_dotenv()


def setup_logging():
    """
    Sets up logging for the application using a configuration file.
    Ensures standardized logging across the application.
    """
    # Construct the path to 'logging.conf'
    logging_config_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'logging.conf')
    # Normalize the path for cross-platform compatibility
    normalized_path = os.path.normpath(logging_config_path)
    # Apply the logging configuration
    logging.config.fileConfig(normalized_path, disable_existing_loggers=False)


def authenticate_user(username: str, password: str):
    """
    Authenticates a user based on provided credentials.
    Replace with actual authentication logic in a real application.

    Parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.

    Returns:
    - dict: A dictionary containing the username if authentication is successful.
    - None: If authentication fails.
    """
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        return {"username": username}
    logging.warning(f"Authentication failed for user: {username}")
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT access token with optional expiration.

    Parameters:
    - data (dict): The payload to encode in the token.
    - expires_delta (timedelta): Optional duration for token validity.

    Returns:
    - str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def validate_and_sanitize_url(url_str: str):
    """
    Validates and sanitizes a URL.

    Parameters:
    - url_str (str): The URL string to validate.

    Returns:
    - str: Sanitized URL if valid.
    - None: If the URL is invalid.
    """
    if validators.url(url_str):
        parsed_url = urlparse(url_str)
        return urlunparse(parsed_url)
    logging.error(f"Invalid URL provided: {url_str}")
    return None


def encode_url_to_filename(url: str):
    """
    Encodes a URL into a base64-encoded filename-safe string.

    Parameters:
    - url (str): The URL to encode.

    Returns:
    - str: Base64-encoded string safe for filenames.
    """
    sanitized_url = validate_and_sanitize_url(url)
    if sanitized_url is None:
        raise ValueError("Provided URL is invalid and cannot be encoded.")
    encoded_bytes = base64.urlsafe_b64encode(sanitized_url.encode('utf-8'))
    return encoded_bytes.decode('utf-8').rstrip('=')


def decode_filename_to_url(encoded_str: str) -> str:
    """
    Decodes a base64-encoded filename-safe string back into a URL.

    Parameters:
    - encoded_str (str): The base64-encoded string to decode.

    Returns:
    - str: Decoded URL.
    """
    padding_needed = 4 - (len(encoded_str) % 4)
    if padding_needed:
        encoded_str += "=" * padding_needed
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')


def generate_links(action: str, qr_filename: str, base_api_url: str, download_url: str) -> List[dict]:
    """
    Generates HATEOAS links for QR code resources.

    Parameters:
    - action (str): The type of action (list, create, delete).
    - qr_filename (str): The filename of the QR code.
    - base_api_url (str): The base API URL.
    - download_url (str): The download URL for the QR code.

    Returns:
    - List[dict]: A list of HATEOAS links.
    """
    links = []
    if action in ["list", "create"]:
        original_url = decode_filename_to_url(qr_filename[:-4])
        links.append({"rel": "view", "href": download_url,
                     "action": "GET", "type": "image/png"})
    if action in ["list", "create", "delete"]:
        delete_url = f"{base_api_url}/qr-codes/{qr_filename}"
        links.append({"rel": "delete", "href": delete_url,
                     "action": "DELETE", "type": "application/json"})
    return links

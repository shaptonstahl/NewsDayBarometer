"""
resolve url shorteners to where they eventually point
"""

import requests


def unshorten_url(short_url, timeout=10):
    """
    Resolves a shortened URL to its final destination.

    Parameters:
    - short_url (str): The shortened URL.
    - timeout (int): Timeout in seconds for the request.

    Returns:
    - str: The final destination URL after all redirects.
    """
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=timeout)
        return response.url
    except requests.RequestException as e:
        return f"Error: {e}"
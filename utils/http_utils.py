import requests

def make_get_request(url, params=None):
    """
    General GET request utility.
    :param url: The API endpoint to send the GET request.
    :param params: Query parameters for the GET request.
    :return: JSON response or None if an error occurred.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")
        return None

def make_post_request(url, data):
    """
    General POST request utility.
    :param url: The API endpoint to send the POST request.
    :param data: The payload to include in the POST request.
    :return: JSON response or None if an error occurred.
    """
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return None

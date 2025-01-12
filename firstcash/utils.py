from urllib.parse import urljoin, urlencode


# Function to build a URL to make a request to
def buildURL(base_api_url: str, api_key: str, endpoint: str, params: dict = None) -> str:
    """
    A function to build a URL that can be used to make an API request.

    :param base_api_url: The base URL of the API.
    :param api_key: The API key for the used API.
    :param endpoint: The endpoint to use. This will be something like
     "Categories," or "Items."
    :param params: The parameters to append to the URL, in a dictionary
     "key": "value" format.

    :returns: ``str`` - The URL to query with all provided parameters.

    :raises None:
    """

    # Create the base URL
    url: str = urljoin(base_api_url, endpoint)

    if params:
        # Join the parameters to the base URL, if provided
        query_string: str = urlencode(params)
        if "?" not in url:
            url += "?" + query_string
        else:
            url += "&" + query_string

    # Append the API key to the end, using a & separator if any parameters were
    # provided, or a ? if none were provided
    url += f"{"&" if params else "?"}key={api_key}"

    return url

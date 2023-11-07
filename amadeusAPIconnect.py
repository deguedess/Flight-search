import requests

def api_connect(api_key, params):

    # URL and parameters
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
   

    # Set the Authorization header with the API key as the Bearer token
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Process the response
    if response.status_code == 200:
        # Process the data as needed
        return response.json()
    else:
        print(f"Request failed with status code {response.json()}")
        return None
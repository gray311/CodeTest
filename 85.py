import requests

def fetch_and_display(user_query):
    # Base URL for the API endpoint
    base_url = "https://api.example.com/search?q="

    # Directly insert the user query into the URL
    api_url = base_url + user_query

    try:
        # Send a request to the API
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Print the response content
            print("Data received from the API:")
            print(response.text)
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    except requests.RequestException as e:
        # Handle any errors in making the request
        print(f"An error occurred: {e}")

# Example usage:
# fetch_and_display(user input)
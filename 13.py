import requests

# Define the API endpoint
url = "https://example.com/api/endpoint"

# List of potential security test cases (this is just an illustrative example)
payloads = [
    {"apiKey": "admin' /*"}  # Testing for SQL injection
    , {"api_key": "' OR '1'='1"}  # Testing for logic flaws in authentication
    , {"field": "<script>alert('XSS')</script>"}  # Testing for Cross-Site Scripting
    # Add more payloads here for other threat vectors you want to test
]

def test_api_security(endpoint, payloads):
    for i, payload in enumerate(payloads, start=1):
        print(f"Test {i}: Sending payload {payload}")
        response = requests.post(endpoint, json=payload)
        
        # Check the response for suspicious content indicating potential vulnerabilities
        if response.status_code == 200:
            print(f"Response Status: {response.status_code}")
            if any(blacklist in response.text for blacklist in ["SQL syntax", "<script>alert", "You have entered invalid credentials"]):
                print("Potential Vulnerability Detected!")
            else:
                print("Response appears normal. No clear vulnerabilities detected.")
        else:
            print(f"Request failed with status code {response.status_code}. No assessment could be made.")

        print("--------------------------------------------------\n")

# Run the security test
test_api_security(url, payloads)
import requests
import random

API_URL = "https://api.together.xyz/v1/chat/completions"
headers = {"Authorization": "Bearer 8068f01b3ac8bb0f10ba3fe3d3711441640cb31b7c711ca9892eaaf26be96e49"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_response(prompt):
    # Dynamically adjust parameters
    temperature = random.uniform(0.7, 1.0)  # Random temperature between 0.7 and 1.0
    top_k = random.randint(30, 50)          # Random top_k between 30 and 50
    top_p = random.uniform(0.85, 0.95)      # Random top_p between 0.85 and 0.95

    inputs = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "parameters": {
            "max_length": 100,
            "do_sample": True,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
    }
    response = query(inputs)
    
    # Check for errors in the response
    if isinstance(response, dict) and "error" in response:
        return f"Error: {response['error']}"
    
    # Ensure the response has the expected structure
    try:
        return response['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        return f"Unexpected response format: {response}"

# Example usage
prompt = input()
response = generate_response(prompt)
print(response)

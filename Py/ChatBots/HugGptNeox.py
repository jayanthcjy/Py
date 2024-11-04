import requests
import random

API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_response(prompt):
    # Dynamically adjust parameters
    temperature = random.uniform(0.7, 1.0)  # Random temperature between 0.7 and 1.0
    top_k = random.randint(30, 50)          # Random top_k between 30 and 50
    top_p = random.uniform(0.85, 0.95)      # Random top_p between 0.85 and 0.95

    inputs = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,
            "do_sample": True,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
    }
    response = query(inputs)
    return response[0]['generated_text']

# Example usage
prompt = "Give me top 10 trending books in 2023"
response = generate_response(prompt)
print(response)


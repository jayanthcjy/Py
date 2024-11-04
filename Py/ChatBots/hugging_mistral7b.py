from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

for message in client.chat_completion(
	model="mistralai/Mistral-7B-Instruct-v0.3",
	messages=[{"role": "user", "content": "How can i help others"}],
	max_tokens=500,
	stream=True,
):
    print(message.choices[0].delta.content, end="")
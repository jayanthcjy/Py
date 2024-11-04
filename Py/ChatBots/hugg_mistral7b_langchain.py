from huggingface_hub import InferenceClient
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms.base import LLM
from typing import List

# Custom LLM wrapper for Hugging Face InferenceClient
class HuggingFaceLLM(LLM):
    def __init__(self, client, model_name, max_tokens=500):
        super().__init__()
        self._client = client
        self._model_name = model_name
        self._max_tokens = max_tokens

    def _call(self, prompt: str, stop: List[str] = None):
        # Send the prompt to the model via InferenceClient
        response = self._client.text_generation(
            model=self._model_name,
            prompt=prompt,  # Changed `inputs` to `prompt`
            max_new_tokens=self._max_tokens  # Adjusted parameter to `max_new_tokens` if required
        )
        return response  # Return response directly as it's likely a string

    @property
    def _llm_type(self):
        return "custom_huggingface_llm"

# Initialize Hugging Face client
client = InferenceClient(api_key="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")
huggingface_llm = HuggingFaceLLM(client=client, model_name="mistralai/Mistral-Nemo-Instruct-2407")

# Set up memory to retain conversation
memory = ConversationBufferMemory(max_length=100) # Retain the last 100 messages

# Create ConversationChain with memory and custom LLM
conversation = ConversationChain(
    llm=huggingface_llm,
    memory=memory
)

# Start the conversational loop
print("Start chatting with the bot! Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # Generate response from the conversation chain
    response = conversation.predict(input=user_input)  # Changed to `input=user_input`
    print("Bot:", response)

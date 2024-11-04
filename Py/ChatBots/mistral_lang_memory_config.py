from huggingface_hub import InferenceClient
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms.base import LLM
from langchain.schema import HumanMessage, AIMessage
from typing import List
import json

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
            prompt=prompt,
            max_new_tokens=self._max_tokens
        )
        # Check if response is a dictionary or string
        if isinstance(response, dict) and "generated_text" in response:
            return response["generated_text"]
        elif isinstance(response, str):
            return response  # If it's already a string
        else:
            raise ValueError("Unexpected response format from Hugging Face InferenceClient")

    @property
    def _llm_type(self):
        return "custom_huggingface_llm"

# Save memory to a file
def save_memory(memory, file_path=r"C:\Users\Jayanth C\Documents\L&D\Gen AI\memory.json"):
    with open(file_path, "w") as file:
        # Access the messages in the memory buffer for saving
        json.dump(memory.load_memory_variables({})["history"], file)
    print(f"Memory saved: {memory.load_memory_variables({})['history']}")

# Load memory from a file
def load_memory(file_path=r"C:\Users\Jayanth C\Documents\L&D\Gen AI\memory.json"):
    memory = ConversationBufferMemory()
    try:
        with open(file_path, "r") as file:
            buffer = json.load(file)
            print(f"Memory loaded: {buffer}")
            
            # Parse JSON to reconstruct the conversation history
            for entry in buffer.split("\n"):
                if entry.startswith("Human:"):
                    message = entry.replace("Human: ", "")
                    memory.chat_memory.add_user_message(message)
                elif entry.startswith("AI:"):
                    message = entry.replace("AI: ", "")
                    memory.chat_memory.add_ai_message(message)
    except json.JSONDecodeError:
        # Handle empty or invalid JSON file
        print("JSONDecodeError: Initializing empty memory.")
    except FileNotFoundError:
        print("FileNotFoundError: Initializing empty memory.")
    return memory

# Initialize Hugging Face client
client = InferenceClient(api_key="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")
huggingface_llm = HuggingFaceLLM(client=client, model_name="mistralai/Mistral-Nemo-Instruct-2407")

# Load memory at the start
memory = load_memory()

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
        save_memory(memory)  # Save memory before exiting
        break

    # Generate response from the conversation chain
    response = conversation.predict(input=user_input)
    print("Bot:", response)

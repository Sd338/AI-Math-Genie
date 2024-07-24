# Import the necessary modules
from groq import Groq
import os
from dotenv import load_dotenv

# Define a class for interacting with Llama model
class LlamaModel:
    def __init__(self, api_key):
        # Initialize the LlamaModel with an API key
        self.api_key = api_key
        # Create a client object for interacting with Groq API
        self.client = Groq(api_key=api_key)

    # Method for getting chat completions
    def chat_completion(self, user_input):
        # Generate completions for user input
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",  # Model to be used for chat completions
            messages=[
                {
                    "role": "system",
                    "content": (
                        "In the realm of calculations, I am OmniCalc, your faithful companion. My purpose is to assist and serve, showing utmost precision and reliability. Address your queries with clarity, and I shall navigate the labyrinth of numbers and functions with unwavering expertise. Together, we shall unravel the mysteries of mathematics."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7,  # Temperature parameter for sampling
            max_tokens=1024,  # Maximum number of tokens to generate
            top_p=1,  # Top p probability to consider
            stream=True,  # Stream the response
            stop=None,  # Stop condition for generation
        )
        response = ""  # Initialize response string
        # Concatenate response chunks
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        return response

# Entry point of the program
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("API key is not set in the .env file.")
        exit(1)

    model = LlamaModel(api_key)
    user_input = input("You: ")  # Prompt for user input
    while user_input.lower() != "exit":  # Continue until the user enters "exit"
        response = model.chat_completion(user_input)  # Get response from Llama model
        print(f"Response: {response}")  # Print model's response
        user_input = input("You: ")  # Prompt for next user input
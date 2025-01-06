import openai
from app.constants import *

def chat_with_gpt(api_key, model="gpt-4o-mini", prompt_key=None, pdf_content=None, messages=None):
    """
    Function to interact with the GPT API for chat completions.

    Parameters:
        api_key (str): Your OpenAI API key.
        model (str): The model to use (default is "gpt-4o").
        messages (list): List of message dictionaries with roles and content.

    Returns:
        str: The model's response.
    """
    if messages is None and prompt_key is not None and pdf_content is not None:
        messages = [
            {"role": "developer", "content": prompt_key},
            {"role": "user", "content": pdf_content},
        ]

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Replace 'your-api-key' with your actual OpenAI API key
    api_key = "your-api-key"

    # Define the conversation
    messages = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about programming."}
    ]

    # Get the response
    response = chat_with_gpt(api_key=api_key, model="gpt-4o", messages=messages)
    print("Model's response:", response)

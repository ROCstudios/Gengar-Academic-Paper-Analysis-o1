import os
import dotenv
from openai import OpenAI
import re

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def clean_json_string(json_str):
    """
    Clean JSON string by handling control characters, escape sequences, and truncated content.
    """
    # Remove any non-JSON content before the first { and after the last }
    try:
        start = json_str.find('{')
        end = json_str.rfind('}') + 1
        if start >= 0 and end > 0:
            json_str = json_str[start:end]
    except:
        pass

    # Handle escape sequences
    json_str = json_str.encode('utf-8').decode('unicode-escape')
    
    # Remove problematic escape sequences that aren't valid JSON
    json_str = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', json_str)
    
    # Remove control characters
    json_str = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', json_str)
    
    # Normalize quotes
    json_str = json_str.replace('"', '"').replace('"', '"')
    
    # Remove newlines
    json_str = json_str.replace("\n", "")
    
    # Handle truncated content by ensuring proper JSON structure
    if not json_str.strip().endswith('}'):
        json_str = json_str.strip() + '}'
    
    return json_str

def chat_with_gpt(
    model="o1-mini", 
    prompt=None, 
    pdf_content=None, 
    messages=None
):
    """
    Function to interact with the GPT API for chat completions.

    Parameters:
        api_key (str): Your OpenAI API key.
        model (str): The model to use (default is "gpt-4o").
        messages (list): List of message dictionaries with roles and content.

    Returns:
        str: The model's response.
    """
    if messages is None and prompt is not None and pdf_content is not None:
        messages = [
            {"role": "user", "content": prompt + "\n\n" + pdf_content},
        ]


    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return clean_json_string(completion.choices[0].message.content)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Replace 'your-api-key' with your actual OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Define the conversation
    messages = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about programming."}
    ]

    # Get the response
    response = chat_with_gpt(api_key=api_key, model="gpt-4o", messages=messages)
    print("Model's response:", response)

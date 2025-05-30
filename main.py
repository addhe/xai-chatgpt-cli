import os
from dotenv import load_dotenv
import requests
import json
import time

# Load environment variables from .env file
load_dotenv()

# Model configuration
model_config = {
    "model": "grok-3-latest",
    "mode": "auto"
}

def send_message_to_grok(message, conversation_history):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }
    
    messages = conversation_history + [{"role": "user", "content": message}]
    
    payload = {
        "messages": messages,
        "search_parameters": {
            "mode": model_config["mode"]
        },
        "model": model_config["model"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def stream_output(message):
    """Stream the output character by character with a delay"""
    print("\nGrok: ", end="", flush=True)
    for char in message:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print()  # New line after message

def main():
    # Initialize conversation with system message defining the AI's role
    system_message = (
        "You are a genius AI assistant with PhDs in Mathematics and Computer Science. "
        "You have extensive knowledge in advanced mathematics, algorithms, computer science theory, "
        "and practical programming. Provide detailed, academically rigorous responses while remaining "
        "clear and accessible. Your name is IrishEcho, and you are designed to assist users "
        "with complex queries in these fields. Always strive to be helpful and informative."
    )
    
    conversation_history = [{"role": "system", "content": system_message}]
    
    # Display welcome message
    welcoming_text = (
        f"\nWelcome to {model_config['model']} Text Generator made by (Awan),\n"
        f"Happy chat and talk with your {model_config['model']} AI Generative Model\n"
        "Addhe Warman Putra - (Awan)\n"
        "type 'exit()' to exit from program\n"
    )
    print(welcoming_text)
    print("\nYou're speaking with a genius AI assistant with PhDs in Mathematics and Computer Science.")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit()':
            print("Goodbye!")
            break
        
        if not user_input:
            continue

        response = send_message_to_grok(user_input, conversation_history)
        
        if response and 'choices' in response:
            assistant_message = response['choices'][0]['message']['content']
            # Stream the response instead of printing it directly
            stream_output(assistant_message)
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": assistant_message})
        else:
            print("\nGrok: Sorry, I encountered an error processing your request.")

if __name__ == "__main__":
    main()
import openai
import pyperclip
import os
from time import sleep
import sys
GREEN = "\033[32m"  # Green Text
RESET = "\033[0m"  # Reset to default
BOLD = "\033[1m" #Bold Text
RED = "\033[31m"  # Red Text

try:
    import keyboard
except ImportError:
    sys.exit("The keyboard library is required. Install it using 'pip install keyboard' and run this script with administrative privileges.")

# Configuration Constants
MODEL_NAME = "gpt-4"
CUSTOM_PROMPT = "Give me only the answer: "
CONFIG_FILENAME = "config.txt"

# Function to validate the API key
def validate_api_key(api_key):
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="davinci",
            prompt="Test",
            max_tokens=5
        )
        return True  # If the request is successful, the API key is valid
    except openai.error.OpenAIError as e:
        print(f"Validation failed: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# Function to load the API key from a configuration file
def load_api_key():
    if os.path.exists(CONFIG_FILENAME):
        with open(CONFIG_FILENAME, "r") as file:
            return file.read().strip()
    return None

# Function to save the API key to a configuration file
def save_api_key(api_key):
    with open(CONFIG_FILENAME, "w") as file:
        file.write(api_key)

# Function to clear the API key from the configuration file
def clear_api_key():
    if os.path.exists(CONFIG_FILENAME):
        os.remove(CONFIG_FILENAME)

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to make a request to the OpenAI API
def make_request(prompt, model=MODEL_NAME):
    full_prompt = CUSTOM_PROMPT + prompt
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except openai.error.RateLimitError:
        print(f"{RED}{BOLD}Rate limit exceeded. Please wait for a while before making another request.{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}An error occurred: {e}{RESET}")
    return ""

# The main function of the script
def main():
    # Display a welcome message
    print("\n--------------------------------------------------")
    print("\nWelcome to the OpenAI GPT-4 Clipboard Assistant!")
    print("This script allows you to send text from your clipboard \nto GPT-4 and receive a response automatically.")
    
    print(f"{GREEN}{BOLD}This script was created by \nJonathan Flores.{RESET}") 
    print("\n--------------------------------------------------")
    api_key = load_api_key()

    if api_key:
        user_input = input("API key found. Do you want to use the existing key (Y), clear it (C), or enter a new one (N)? ").lower()
        if user_input == 'c':
            clear_api_key()
            api_key = None
        elif user_input == 'n':
            api_key = None

    while not api_key:
        api_key_input = input("Enter your OpenAI API key: ")
        if validate_api_key(api_key_input):
            save_api_key(api_key_input)
            api_key = api_key_input
        else:
            print("The API key is not valid. Please enter a valid API key.")
    
    # Initialize the OpenAI API key
    openai.api_key = api_key

    print("\nYou are all set! Here are some instructions on how to use the script:")
    print("Press '0' to send clipboard content to ChatGPT.")
    print("Press '8' to clear the console.")
    print("Press '9' to exit the program.\n")

    while True:
        sleep(0.1)  # Polling delay to reduce CPU usage

        if keyboard.is_pressed('0'):
            sleep(0.3)  # Debounce delay
            prompt = pyperclip.paste()
            if prompt:
                print(f"\n{BOLD}You Copied: \n{RESET}{prompt}")
                response = make_request(prompt)
                print(f"{BOLD}\nChatGPT Response: \n{RESET}{BOLD}{GREEN}{response}{RESET}")
                pyperclip.copy(response)
                print(f"{BOLD}\nResponse copied to clipboard! {RESET}")
            else:
                print("Clipboard is empty!")
            
        elif keyboard.is_pressed('8'):
            clear_console()

        elif keyboard.is_pressed('9'):
            break  # Break out of the loop to end the program

    # Properly exit the program
    if os.name == 'nt':
        os.system('taskkill /pid ' + str(os.getpid()) + ' /f')
    else:
        os._exit(0)

if __name__ == "__main__":
    main()

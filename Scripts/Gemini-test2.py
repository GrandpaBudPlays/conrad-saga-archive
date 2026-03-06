import os
import sys
from dotenv import load_dotenv
from google import genai

# Load the variables from .env into the system environment
load_dotenv()

# Fetch the variable
api_key = os.getenv('GEMINIAPIKEY')
print(api_key)

if not api_key:
    print("Key not found. Check your .env file.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)
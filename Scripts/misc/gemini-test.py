import os
import sys
import time

from dotenv import load_dotenv
from google import genai

# Load the variables from .env into the system environment
load_dotenv()

# Fetch the variable
api_key = os.getenv('GEMINIAPIKEY')

if not api_key:
    print("Key not found. Check your .env file.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# ... before your request ...
time.sleep(2) # A 2-second 'breather' usually keeps the Free Tier happy

print("Connecting to Gemini...")
print(client)

print("--- Available Models for my Key ---")
for m in client.models.list():
    print(f"Name: {m.name}")

response = client.models.generate_content(
    model='gemini-3-flash-preview', 
    contents='Hi Gemini! I am ready to start analyzing video transcripts.'
)

print("\nGemini says:")
print(response.text)


import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINIAPIKEY'))

print("Available models:")
for m in client.models.list():
    print(f"  {m.name}")

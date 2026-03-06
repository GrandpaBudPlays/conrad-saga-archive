import os
from dotenv import load_dotenv
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_content(file_path):

    # Reads a Markdown transcript file and returns the string content.

    # Check if the file exists before attempting to read (the 'C#' safety check)
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


print("Fetching transcript...")
transcript_path = r"E:\Video\Streaming\Repo\Stream-Archive\010-Valheim\Chronicles-Of-The-Exile\Saga I\S01 E001 Transcript.md"
full_text = get_transcript_content(transcript_path)

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINIAPIKEY'))

# Put any YouTube Video ID here (the part after v=)
# video_id = "T74mDa1ctPs" 

try:
# 1. Instantiate the API object
    # ytt_api = YouTubeTranscriptApi()
    
    # 2. Use the new .fetch() method instead of .get_transcript()
    # Also, note that it now returns objects, so we use .to_raw_data() 
    # if we want the old list of dictionaries format.
    # transcript = ytt_api.fetch(video_id).to_raw_data()
    
    # 3. Combine the text
    # full_text = " ".join([entry['text'] for entry in transcript])    
    print("Success! Transcript loaded.")
    
    print("Analyzing with Gemini 3...")
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=f"Please summarize this video transcript and list the top 3 key takeaways: {full_text}"
    )
    
    #print("\n---Transcript---")
    #print(full_text)

    print("\n--- Summary ---")
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
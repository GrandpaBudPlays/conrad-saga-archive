import sys
from file_manager import find_transcript_and_metadata, load_transcript_asset

def check_saga_status(query: str):
    # 1. Locate the files and metadata
    saga = find_transcript_and_metadata(query)
    
    if not saga or 'path' not in saga:
        print("Error: Saga not found.")
        return

    # 2. Pass the path from the saga to the loader
    # Using our modified function that returns "" if it's "No Audio"
    transcript_content = load_transcript_asset(saga['path'])

    # 3. Determine status based on the returned string
    is_no_audio = len(transcript_content) == 0

    if is_no_audio:
        print("No Audio")
    else:
        print("Has Content")

if __name__ == "__main__":
    # Example: run via 'python main.py "MySagaName"'
    # search_query = sys.argv[1] if len(sys.argv) > 1 else "default_saga"
    search_query = "S02 E010 Transcript.md"  # Hardcoded for testing; replace with CLI arg as needed
    check_saga_status(search_query)


    #  opencode -s ses_334f23689ffexSSpUFp00xyvBH
import os
import re
import pathlib
import sys
import time
from urllib import response
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.api_core import exceptions
from google.genai import errors  # <--- Add this import


# --- 1. SETUP & PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Moves up from .\scripts\ to .\stream-archive\
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
VALHEIM_ROOT = os.path.join(ROOT_DIR, "010-Valheim", "Chronicles-Of-The-Exile")
TEMPLATE_PATH = os.path.join(ROOT_DIR, "010-Valheim", "010-Templates", "Feedback Template.md")

def parse_cli_args():
    # Job: Validate and return command line arguments
    if len(sys.argv) < 3:
        print("Usage: python audit_pipeline.py S01 E005")
        sys.exit(1)
    return sys.argv[1].upper(), sys.argv[2].upper()

def resolve_lexicon_data(season_str, episode_str):
    # Job: Determine if lexicon is needed and load it using relative paths
    # Matches digits in E044 or S04.1
    ep_num_match = re.search(r'(\d+)', episode_str)

    if ep_num_match and int(ep_num_match.group(1)) > 35:
        lexicon_path = os.path.join(ROOT_DIR, "010-Valheim", "Saga-Lexicon-Valheim.md")
        print(f"Loading Lexicon: {lexicon_path}")
        return load_transcript_asset(lexicon_path)

    return ""

def get_template_data():
    # Job: Locate and load the feedback template
    template_path = os.path.join(ROOT_DIR, "010-Valheim", "010-Templates", "Feedback Template.md")
    data = load_transcript_asset(template_path)
    if not data:
        print(f"CRITICAL: Template missing at {template_path}")
        sys.exit(1)
    return data

def find_transcript_and_metadata(target_filename):

    DEFAULT_BIOMES = {
        "Saga I": "Meadows",
        "Saga II": "Black Forest",
        "Saga III": "Swamp",
        "Saga IV": "Mountains",
        "Saga V": "Plains",
        "Saga VI": "Ashlands"
    }

    search_path = pathlib.Path(VALHEIM_ROOT)
    found_files = list(search_path.rglob(target_filename))

    if not found_files:
        return None

    transcript_path = found_files[0]
    saga_folder_name = transcript_path.parent.name
    current_dir = transcript_path.parent
    biome_name = "Unknown"

    # Climb the tree for Biome.md
    while current_dir != search_path.parent:
        biome_file = current_dir / "Biome.md"
        if biome_file.exists():
            with open(biome_file, 'r', encoding='utf-8') as f:
                biome_name = f.read().strip()
            break
        current_dir = current_dir.parent

    if biome_name == "Unknown":
        # .get() allows us to provide a final 'Global Unknown' if the saga name is weird
        biome_name = DEFAULT_BIOMES.get(saga_folder_name, "Unknown/Multiple")

    return {
        "path": transcript_path,
        "biome": biome_name,
        "saga": transcript_path.parent.name
    }

# --- 1. RESOURCE MANAGEMENT ---

def load_transcript_asset(file_path):
    # Handle File I/O and Encoding
    # Returns: A single string containing the full file content
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- 2. LOGIC FUNCTIONS ---

def get_last_timestamp(text):
    # Extract the final timestamp string from a text block
    # Matches H:MM:SS.mmm or MM:SS.mmm
    ts_pattern = r'\d+:\d+:\d+\.\d+|\d+:\d+\.\d+'
    matches = re.findall(ts_pattern, text)

    # Return the very last match in the list
    return matches[-1] if matches else None

def timestamp_to_seconds(ts_str):
    # Math conversion from string to float
    # Example: '1:27:19.840' -> 5239.84
    if not ts_str:
        return 0.0

    try:
        parts = ts_str.split(':')
        # Logic for Hours:Minutes:Seconds
        if len(parts) == 3:
            h, m, s = parts
            total = (int(h) * 3600) + (int(m) * 60) + float(s)
        # Logic for Minutes:Seconds
        elif len(parts) == 2:
            m, s = parts
            total = (int(m) * 60) + float(s)
        else:
            total = float(parts[0])
        return round(total, 2)
    except (ValueError, IndexError):
        return 0.0

# --- 2. UTILITY / EXECUTION ---

def get_video_duration(raw_content):

    # Coordinate specialized functions to calculate total duration
    if not raw_content:
        return 0.0

    # Step 1: Identify the end of the video
    final_ts = get_last_timestamp(raw_content)

    # Step 3: Perform math conversion
    duration = timestamp_to_seconds(final_ts)

    return duration

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def sanitize_markdown(text):
    # Fix NBSP and Code Fences first
    text = text.replace('\xa0', ' ').replace("```markdown", "").replace("```", "").strip()

    # 1. NEW: Kill Leading Whitespace (Critical for MD007/MD032/MD009)
    # This ensures regex patterns starting with \n work correctly
    lines = [line.lstrip() for line in text.splitlines()]
    text = "\n".join(lines)

    # 2. NEW: Fix MD025 (Multiple Top-level Headings)
    # Demotes subsequent # to ##
    processed_lines = []
    for i, line in enumerate(text.splitlines()):
        if i > 0 and line.startswith("# "):
            processed_lines.append("#" + line)
        else:
            processed_lines.append(line)
    text = "\n".join(processed_lines)

    # 3. Collapse 3+ newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 4. Fix MD022/MD032: Blank lines around headings
    text = re.sub(r'(\S)\n(#+ )', r'\1\n\n\2', text)
    text = re.sub(r'(#+ .*)\n(\S)', r'\1\n\n\2', text)

    # 5. Fix MD032: Blank line BEFORE and AFTER lists
    text = re.sub(r'([^\n])\n([*-]|\d+\.)', r'\1\n\n\2', text)
    text = re.sub(r'([*-]|\d+\..*)\n([^\n\s*-])', r'\1\n\n\2', text)

    # 6. Fix MD007/MD030: Standardize list indentation and spacing
    # Note: line.lstrip() above handled the 4-space indent,
    # but we'll keep these for nested lists
    text = re.sub(r'\n    ([*-]|\d+\.)', r'\n  \1', text)
    text = re.sub(r'\n([*-]|\d+\.) +', r'\1 ', text)

    # 7. Final cleanup: Trailing spaces and final newline
    lines = [line.rstrip() for line in text.splitlines()]
    output = "\n".join(lines).strip() + "\n"

    return output

def save_audit_report(transcript_path, content, report_type):
    # Job: Save results with linter-friendly formatting
    parent_dir = os.path.dirname(transcript_path)
    report_dir = os.path.join(parent_dir, "Reports")

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    base_name = os.path.basename(transcript_path).replace(" Transcript.md", "")
    filename = f"{base_name} {report_type}.md"
    save_path = os.path.join(report_dir, filename)

 # STRIP FENCES AND SANITIZE
    content = sanitize_markdown(content)

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS: {report_type} saved to {save_path}")

# --- 2. AUDIT FUNCTIONS ---

def run_saga_audit(client, transcript, template, lexicon, ep_id, duration, biome):
    # Job: Tactical Audit with Linter-specific instructions
    instr = (
        "You are a Content Auditor. Populate the provided Markdown Template. "
        "CRITICAL FORMATTING RULES: "
        "1. Surround all headings (#, ##) with exactly one blank line. "
        "2. Use 2-space indentation for all nested lists. "
        "3. Do not leave trailing spaces at the end of lines."
    )

    # We also pad the prompt variables to give the AI a 'visual' hint of the spacing
    prompt = f"""
# AUDIT TARGET: {ep_id}

**BIOME:** {biome}
**DURATION:** {duration}s

## LEXICON CONTEXT
{lexicon if lexicon else "None (Historical Episode)"}

## TRANSCRIPT
{transcript}

## TEMPLATE
{template}
"""

    response = safe_generate_content(
        client,
        model_name='gemini-3-flash-preview',
        config=types.GenerateContentConfig(system_instruction=instr, temperature=0.1),
        contents=prompt
    )
    return response.text

def run_strategic_gold_extraction(client, transcript, episode_id, duration_sec):
    # Job: Extract repurposing opportunities using the discovered duration
    strategic_instruction = (
        "You are a Strategic Content Analyst for 'Grandpa Bud Plays'. "
        "Identify 'Highlight Gold' for repurposing. "
        "Apply the 'Grandpa Rule'."
        "CRITICAL: Output raw Markdown only. Do NOT wrap in ```markdown code blocks. "
        "Surround all headings (#, ##) with blank lines and use 2-space indentation."
        "Use proper Markdown heading levels (###) for segment titles. Do not use bold text as a heading."
    )

    # Automatically determine pacing based on the duration we found
    pacing = "High-density (2-3 mins)" if duration_sec < 1200 else "Strategic (8-12 mins)"

    prompt = f"""
    TASK: Highlight Gold Audit for {episode_id}.
    DURATION: {duration_sec}s | PACING: {pacing}
    CATEGORIES: Type A (Shorts), Type B (Clips), Type C (Saga Components), Type D (YouTube Chapters).

    TRANSCRIPT:
    {transcript}
    """

    response = safe_generate_content(
        client,
        model_name='gemini-3-flash-preview',
        config=types.GenerateContentConfig(
            system_instruction=strategic_instruction,
            temperature=0.2,
            http_options={"timeout": 120000}  # Increase timeout for longer processing
        ),
        contents=prompt
    )

    return response.text

def safe_generate_content(client, model_name, config, contents, retries=6):
    print(f"Attempting to generate content with model '{model_name}'...")

    for i in range(retries):
        try:
            return client.models.generate_content(
                model=model_name,
                config=config,
                contents=contents
            )
        # CHANGE: Catch the new SDK's specific server error
        except errors.ServerError as e:
            # Verify if it's a 503 before proceeding
            if e.code == 503:
                wait_time = (i + 1) * 5
                print(f"Server busy (503). Retrying in {wait_time}s...")

                if i == 2:  # Switch on the 3rd failed attempt
                    print(f"--- {i+1} retries failed. Switching from {model_name} to backup model. ---")
                    model_name = 'gemini-1.5-flash'

                time.sleep(wait_time)
            else:
                # If it's a different 5xx error (like 500), handle it or re-raise
                print(f"Server Error {e.code}: {e.message}")
                break

        except Exception as e:
            # Catch-all for networking or client-side issues
            print(f"Connection issue: {e}")
            break

    return None
# --- 3. ORCHESTRATION ---

if __name__ == "__main__":
    load_dotenv()

    # 1. Input & Path Discovery
    season, episode = parse_cli_args()
    full_ep_id = f"{season} {episode}"
    target_filename = f"{season} {episode} Transcript.md"

    # Use the 'Tree Climbing' logic we built earlier
    file_info = find_transcript_and_metadata(target_filename)

    if not file_info:
        print(f"Error: Could not find {target_filename} in {VALHEIM_ROOT}")
        sys.exit(1)

    # 2. Resource Loading
    transcript_data = load_transcript_asset(file_info['path'])
    template_data = get_template_data()
    lexicon_data = resolve_lexicon_data(season, episode)

    # 3. Metadata Extraction
    actual_duration = get_video_duration(transcript_data)

    print(f"--- Session Discovery ---")
    print(f"File:    {file_info['path']}")
    print(f"Saga:    {file_info['saga']}")
    print(f"Biome:   {file_info['biome']}")
    print(f"Length:  {actual_duration}s")
    print(f"Lexicon: {'Loaded' if lexicon_data else 'Skipped (Historical)'}")

    print(f"--- Processing {episode} ---")
    client = genai.Client(api_key=os.getenv('GEMINIAPIKEY'))
    print("Client initialized. Starting Pass 1: Tactical Audit...")

    # Pass 1
    audit_report = run_saga_audit(
        client,
        transcript_data,
        template_data,
        lexicon_data,
        full_ep_id,       # From CLI args
        actual_duration,  # From our math function
        file_info['biome'] # From our Tree Climbing result
    )
    print("Pass 1: Audit Complete.")

    # Pass 2
    gold_out = run_strategic_gold_extraction(client, transcript_data, full_ep_id, actual_duration)
    print("Pass 2: Gold Extraction Complete.")

    # Save Pass 1
    save_audit_report(file_info['path'], audit_report, "Audit")
    # Save Pass 2
    save_audit_report(file_info['path'], gold_out, "Gold")

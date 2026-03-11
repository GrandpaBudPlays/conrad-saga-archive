import os
import pathlib
import re
import sys
from dataclasses import dataclass


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
VALHEIM_ROOT = os.path.join(ROOT_DIR, "010-Valheim", "Chronicles-Of-The-Exile")


DEFAULT_BIOMES = {
    "Saga I": "Meadows",
    "Saga II": "Black Forest",
    "Saga III": "Swamp",
    "Saga IV": "Mountains",
    "Saga V": "Plains",
    "Saga VI": "Ashlands"
}

@dataclass
class SessionData:
    season: str
    episode: str
    full_ep_id: str
    target_filename: str
    path: str
    saga: str
    biome: str
    transcript: str
    lexicon: str
    duration: float


def find_transcript_and_metadata(target_filename):
    search_path = pathlib.Path(VALHEIM_ROOT)
    found_files = list(search_path.rglob(target_filename))

    if not found_files:
        return None

    transcript_path = found_files[0]
    saga_folder_name = transcript_path.parent.name
    current_dir = transcript_path.parent
    biome_name = "Unknown"

    while current_dir != search_path.parent:
        biome_file = current_dir / "Biome.md"
        if biome_file.exists():
            with open(biome_file, 'r', encoding='utf-8') as f:
                biome_name = f.read().strip()
            break
        current_dir = current_dir.parent

    if biome_name == "Unknown":
        biome_name = DEFAULT_BIOMES.get(saga_folder_name, "Unknown/Multiple")

    return {
        "path": transcript_path,
        "biome": biome_name,
        "saga": transcript_path.parent.name
    }


def _has_no_audio_transcript(file_path: str) -> bool:
    # Helper to check for 'No Audio' and absence of timestamps.
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read the first 500 characters to cover ~10 lines
        header_chunk = f.read(500)
        
        # Case-insensitive check for "No Audio"
        if "no audio" in header_chunk.lower():
            has_no_audio = not bool(re.search(r'\d{1,2}:\d{2}', header_chunk))
            return has_no_audio
        else:
            # Reset to start and check the whole file for timestamps
            f.seek(0)

    return False

def load_transcript_asset(file_path: str) -> str:
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return ""

    # Use helper to determine if we should return an empty string
    if _has_no_audio_transcript(file_path):
        return ""

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_file(path: str) -> str:
    if not os.path.exists(path):
        print(f"Error: File not found at {path}")
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()




def resolve_lexicon_data(season_str: str, episode_str: str) -> str:
    ep_num_match = re.search(r'(\d+)', episode_str)
    if ep_num_match and int(ep_num_match.group(1)) > 35:
        lexicon_path = os.path.join(ROOT_DIR, "010-Valheim", "Saga-Lexicon-Valheim.md")
        print(f"Loading Lexicon: {lexicon_path}")
        return read_file(lexicon_path)
    return ""


def get_last_timestamp(text: str):
    ts_pattern = r'\d+:\d+:\d+\.\d+|\d+:\d+\.\d+'
    matches = re.findall(ts_pattern, text)
    return matches[-1] if matches else None


def timestamp_to_seconds(ts_str: str | None) -> float:
    if not ts_str:
        return 0.0
    try:
        parts = ts_str.split(':')
        if len(parts) == 3:
            h, m, s = parts
            total = (int(h) * 3600) + (int(m) * 60) + float(s)
        elif len(parts) == 2:
            m, s = parts
            total = (int(m) * 60) + float(s)
        else:
            total = float(parts[0])
        return round(total, 2)
    except (ValueError, IndexError):
        return 0.0


def get_video_duration(raw_content: str) -> float:
    if not raw_content:
        return 0.0
    final_ts = get_last_timestamp(raw_content)
    return timestamp_to_seconds(final_ts)


def prepare_session_assets(season: str, episode: str) -> SessionData:
    full_ep_id = f"{season} {episode}"
    target_filename = f"{full_ep_id} Transcript.md"

    file_info = find_transcript_and_metadata(target_filename)
    if not file_info:
        print(f"Error: Could not find {target_filename} in {VALHEIM_ROOT}")
        sys.exit(1)

    transcript_data = load_transcript_asset(str(file_info['path']))
    if not transcript_data:
        print(f"Skipping {target_filename}: No Audio detected.")
        sys.exit(0)

    lexicon_data = resolve_lexicon_data(season, episode)
    actual_duration = get_video_duration(transcript_data)

    return SessionData(
        season=season,
        episode=episode,
        full_ep_id=full_ep_id,
        target_filename=target_filename,
        path=str(file_info['path']),
        saga=str(file_info['saga']),
        biome=str(file_info['biome']),
        transcript=transcript_data,
        lexicon=lexicon_data,
        duration=actual_duration
    )


def save_audit_report(transcript_path: str, content: str, report_type: str, model_suffix: str | None = None, extension: str = ".md"):
    parent_dir = os.path.dirname(transcript_path)
    report_dir = os.path.join(parent_dir, "Reports")

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    base_name = os.path.basename(transcript_path).replace(" Transcript.md", "")
    if model_suffix:
        filename = f"{base_name} {report_type} - {model_suffix}{extension}"
    else:
        filename = f"{base_name} {report_type}{extension}"
    save_path = os.path.join(report_dir, filename)

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS: {report_type} saved to {save_path}")


def parse_cli_args() -> tuple[str, str, str]:
    if len(sys.argv) < 3:
        print("Usage: python Brand.py <Operation> <Season> <Episode>")
        print("Operations: Audit, Feedback, Gold, Describe, Draft")
        print("Example: python Brand.py Feedback S01 E005")
        sys.exit(1)
    
    valid_operations = ["Audit", "Feedback", "Gold", "Describe", "Draft"]
    first_arg = sys.argv[1].capitalize()
    
    if first_arg in valid_operations:
        if len(sys.argv) < 4:
            print("Usage: python Brand.py <Operation> <Season> <Episode> [--continue]")
            sys.exit(1)
        operation = first_arg
        season = sys.argv[2].upper()
        episode = sys.argv[3].upper()
        
        # Super simple check for continue flag
        if "--continue" in sys.argv:
            import os
            os.environ["DRAFT_PASS"] = "2" 
    else:
        operation = "Audit"
        season = sys.argv[1].upper()
        episode = sys.argv[2].upper()
        print(f"Warning: Deprecated argument order. Please use: python Brand.py {operation} {season} {episode}")
        
    return season, episode, operation

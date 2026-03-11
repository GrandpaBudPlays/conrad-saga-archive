import os
import sys
from dotenv import load_dotenv

from ai.gemini import GeminiModel
from ai.model_runner import ModelRunner
from file_manager import (
    parse_cli_args,
    prepare_session_assets,
)
from workflows import get_workflow


DEFAULT_TIMEOUT = 300


if __name__ == "__main__":
    load_dotenv()

    season, episode, operation = parse_cli_args()
    session = prepare_session_assets(season, episode)

    print(f"--- Processing (Operation: {operation}) on {episode}  ---")
    gemini_model = GeminiModel(api_key=os.getenv('GEMINIAPIKEY'))
    model_runner = ModelRunner()

    print("Client initialized.")

    # Let the registry resolve and execute the workflow
    workflow = get_workflow(operation)
    workflow.execute(session, gemini_model)

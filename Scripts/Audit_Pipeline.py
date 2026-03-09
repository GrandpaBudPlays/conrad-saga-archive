import os
import sys
from typing import cast
from dotenv import load_dotenv

from ai.gemini import GeminiModel
from ai.model_runner import ModelRunner
from prompts import get_prompt_library
from prompts.audit import AuditPrompt
from prompts.gold_extraction import GoldExtractionPrompt
from file_manager import (
    parse_cli_args,
    prepare_session_assets,
    save_audit_report,
)

DEFAULT_TIMEOUT = 300


def run_saga_audit(model: GeminiModel, transcript: str, template: str, lexicon: str, ep_id: str, duration: float, biome: str):
    prompts = get_prompt_library("valheim")
    audit_prompt: AuditPrompt = cast(AuditPrompt, prompts.get("audit"))
    
    prompt = audit_prompt.build_audit_prompt(
        episode_id=ep_id,
        duration=str(int(duration)),
        biome=biome,
        lexicon_context=lexicon,
        transcript=transcript,
        template=template
    )
    
    temperature = audit_prompt.get_temperature(model.name)
    result = model.generate(prompt, system_instruction=audit_prompt.get_system_instruction(), temperature=temperature)
    if not result.success:
        raise RuntimeError(f"Failed to generate audit content: {result.error}")
    return result.model_name, result.content


def run_strategic_gold_extraction(model: GeminiModel, transcript: str, episode_id: str, duration_sec: float):
    prompts = get_prompt_library("valheim")
    gold_prompt: GoldExtractionPrompt = cast(GoldExtractionPrompt, prompts.get("gold_extraction"))
    
    prompt = gold_prompt.build_gold_prompt(transcript=transcript, duration_sec=duration_sec)
    
    temperature = gold_prompt.get_temperature(model.name)
    result = model.generate(prompt, system_instruction=gold_prompt.get_system_instruction(), temperature=temperature)
    if not result.success:
        raise RuntimeError(f"Failed to generate strategic gold content: {result.error}")
    return result.model_name, result.content


if __name__ == "__main__":
    load_dotenv()

    season, episode = parse_cli_args()
    session = prepare_session_assets(season, episode)

    print(f"--- Processing {episode} ---")
    gemini_model = GeminiModel(api_key=os.getenv('GEMINIAPIKEY'))
    model_runner = ModelRunner()

    print("Client initialized. Starting Pass 1: Tactical Audit...")

    audit_model, audit_report = run_saga_audit(
        gemini_model,
        session.transcript,
        session.template,
        session.lexicon,
        session.full_ep_id,
        session.duration,
        session.biome
    )
    save_audit_report(session.path, audit_report, "Audit", audit_model)
    print("Pass 1: Audit Complete.")

    print("Starting Pass 2: Strategic Gold Extraction...")
    gold_model, gold_out = run_strategic_gold_extraction(
        gemini_model, 
        session.transcript, 
        session.full_ep_id, 
        session.duration
    )
    save_audit_report(session.path, gold_out, "Gold", gold_model)
    print("Pass 2: Gold Extraction Complete.")


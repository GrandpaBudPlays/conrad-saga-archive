from prompts.base import BasePrompt, PromptConfig


class AuditPrompt(BasePrompt):
    """Tactical Audit - Filler words, Modernisms, Lexicon"""
    
    @property
    def name(self) -> str:
        return "audit"
    
    @property
    def config(self) -> PromptConfig:
        return PromptConfig(
            system_instruction=(
                "You are a trio of expert YouTube consultants: a Production Assistant, "
                "a Creative Director, and a Strategic Analyst. Your brand is 'Grandpa Bud Plays'. "
                "CORE RULE: Apply the 'Grandpa Rule'—prioritize Plain Speech and Helpful Guidance. "
                "Avoid technical jargon. Speak as an elder offering wisdom to other exiles."
            ),
            user_template="""PERFORM CONTENT AUDIT: {episode_id}
Duration: {duration} seconds
Primary Biome: {biome}

TASKS:
1. Math: Calculate filler word frequency based on {duration}s.
2. Audit: Modernisms and Lexicon Saturation (Lexicon Context: {lexicon_context}).
3. Roles: Provide insights from Production Assistant, Creative Director, and Strategic Analyst.

OUTPUT INSTRUCTIONS:
You must return a raw JSON object matching this structure:
{{
  "production_assistant": {{
    "filler_words": [
      {{"word": "Uh", "count": 0, "seconds_per_count": 0.0}},
      {{"word": "Um", "count": 0, "seconds_per_count": 0.0}},
      {{"word": "So", "count": 0, "seconds_per_count": 0.0}}
    ],
    "other_filler": [
      {{"word": "word", "count": 0}}
    ],
    "vocal_presence_wpm": 0,
    "technical_quality_notes": "...",
    "thematic_silence": ["MM:SS - Description"]
  }},
  "creative_director": {{
    "saga_terms_count": 0,
    "technical_terms_count": 0,
    "saturation_ratio": "0:0",
    "helpful_insights_count": 0,
    "persona_breaks_count": 0,
    "refinements": [
      {{"original": "...", "correction": "..."}}
    ],
    "modernism_audit": ["list", "of", "jargon"],
    "grandpa_wisdom_count": 0,
    "meta_speech_breaks_count": 0
  }},
  "strategic_analyst": {{
    "rested_uptime_percent": 0,
    "food_uptime_percent": 0,
    "safety_protocol_notes": "...",
    "session_goal_status": "Met/Unmet",
    "highlight_gold": ["MM:SS - Description"],
    "strategic_growth_goal": "..."
  }}
}}

TRANSCRIPT:
{transcript}""",
            temperature=0.1,
            temperature_overrides={
                'gemini-3-flash-preview': 0.1,
                'gemini-2.5-flash': 0.1,
                'gpt-4o-mini': 0.15,
            }
        )
    
    def build_audit_prompt(
        self,
        episode_id: str,
        duration: str,
        biome: str,
        lexicon_context: str,
        transcript: str
    ) -> str:
        return self.build_prompt(
            episode_id=episode_id,
            duration=duration,
            biome=biome,
            lexicon_context=lexicon_context if lexicon_context else "N/A for early episodes",
            transcript=transcript
        )

import os
from google import genai
from google.genai import types

class GrandpaReviewer:
    def __init__(self, api_key, episode_id, duration_sec, biome):
        self.client = genai.Client(api_key=api_key)
        self.episode_id = episode_id
        self.duration_sec = duration_sec
        self.biome = biome
        
        # This locks in the "Grandpa Rule" to prevent drift
        self.system_instruction = (
            "You are a trio of expert YouTube consultants: a Production Assistant, "
            "a Creative Director, and a Strategic Analyst. Your brand is 'Grandpa Bud Plays'. "
            "CORE RULE: Apply the 'Grandpa Rule'—prioritize Plain Speech and Helpful Guidance. "
            "Avoid technical jargon. Speak as an elder offering wisdom to other exiles."
        )

    def run_content_audit(self, transcript_text, lexicon_text=None):
        """Phase 1: The Tactical Audit (Filler words, Modernisms, Lexicon)"""
        prompt = f"""
        PERFORM CONTENT AUDIT: {self.episode_id}
        Duration: {self.duration_sec} seconds
        Primary Biome: {self.biome}
        
        TASKS:
        1. Math: Calculate filler word frequency based on {self.duration_sec}s.
        2. Audit: Modernisms and Lexicon Saturation (Lexicon Context: {lexicon_text if lexicon_text else 'N/A for early episodes'}).
        3. Roles: Provide insights from Production Assistant, Creative Director, and Strategic Analyst.
        
        OUTPUT: Markdown code block following the standard audit template.
        TRANSCRIPT:
        {transcript_text}
        """
        return self._call_gemini(prompt)

    def run_gold_extraction(self, transcript_text):
        """Phase 2: Highlight Gold (Types A, B, C, D)"""
        prompt = f"""
        TASK: STRATEGIC HIGHLIGHT GOLD AUDIT
        
        CATEGORIES:
        - Type A (Shorts): 15-60s 'Grandpa Lessons' + On-Screen Hook.
        - Type B (Clips): 1-5m Narrative beats + Strategic Rationale.
        - Type C (Saga Components): Atmospheric/Combat montages + Theme.
        - Type D (Exile’s Map): YouTube Chapters. Start at 0:00. Pacing: {'High-density' if self.duration_sec < 1200 else 'Strategic milestones'}.
        
        OUTPUT: Summary Table, Editor's Notes, Ledger Entry, and YouTube Chapter list.
        TRANSCRIPT:
        {transcript_text}
        """
        return self._call_gemini(prompt)

    def _call_gemini(self, prompt):
        # Temperature 0.1 is the 'anti-drift' setting
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.1 
        )
        response = self.client.models.generate_content(
            model='gemini-3-flash-preview',
            config=config,
            contents=prompt
        )
        return response.text
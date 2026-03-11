from prompts.base import BasePrompt, PromptConfig

class DraftExtractionPrompt(BasePrompt):
    """Pass 1: Extract factual events for the narrative description."""
    @property
    def name(self) -> str: return "draft_extraction"
    @property
    def config(self) -> PromptConfig:
        return PromptConfig(
            system_instruction="You are a factual archivist. Extract a chronological timeline of key events, encounters, and milestones from the transcript. Do not use creative writing or embellishments. Just facts.",
            user_template="""TASK: Extract factual events from the transcript.
{hints_text}

OUTPUT INSTRUCTIONS:
Return a JSON object:
{{
  "events": [
    {{"time": "MM:SS", "fact": "Conrad mined copper", "importance": "high/medium/low"}}
  ]
}}

TRANSCRIPT:
{transcript}""",
            temperature=0.1
        )
    def build_extraction_prompt(self, transcript: str, hints: str = "") -> str:
        hints_text = f"USER HINTS (Prioritize these events):\n{hints}\n" if hints else ""
        return self.build_prompt(transcript=transcript, hints_text=hints_text)

class DraftCreativePrompt(BasePrompt):
    """Pass 2: The Triple-Threat Creative Draft."""
    @property
    def name(self) -> str: return "draft_creative"
    @property
    def config(self) -> PromptConfig:
        return PromptConfig(
            system_instruction="You are an expert lore-writer for the 'Conrad Saga' Valheim series. You must perfectly mimic three distinct personas based on the provided style guides.",
            user_template="""TASK: Write the Triple-Threat YouTube Description based ONLY on these factual events.

FACTUAL EVENTS:
{events_json}

PERSONA GUIDES:
{brand_context}
{ulf_persona}
{descriptions_protocol}

OUTPUT INSTRUCTIONS:
Return a JSON object containing the three paragraphs:
{{
  "ulf_hook": "3-5 short, punchy sentences in Ulf's voice.",
  "grandpa_legend": "One cohesive paragraph in Grandpa's lore voice (storyteller).",
  "conrad_chronicle": "One paragraph starting with 'In this chronicle...' summarizing the factual events."
}}""",
            temperature=0.4
        )
    def build_creative_prompt(self, events_json: str, brand_context: str, ulf_persona: str, descriptions_protocol: str) -> str:
        return self.build_prompt(
            events_json=events_json,
            brand_context=brand_context,
            ulf_persona=ulf_persona,
            descriptions_protocol=descriptions_protocol
        )

class DraftSEOPrompt(BasePrompt):
    """Pass 3: The SEO Editor."""
    @property
    def name(self) -> str: return "draft_seo"
    @property
    def config(self) -> PromptConfig:
        return PromptConfig(
            system_instruction="You are a YouTube SEO Editor. Your job is to surgically inject SEO keywords into creative writing without altering the tone, voice, or sentence structure of the original authors.",
            user_template="""TASK: Inject the following SEO keywords naturally into the provided text.
SEO KEYWORDS: {seo_keywords}

ORIGINAL TRIPLE-THREAT DRAFT:
{draft_json}

RULES:
1. Do not change the Ulf voice (short, punchy).
2. Do not change Grandpa's storytelling style.
3. Replace generic words (e.g., 'the big troll', 'the bronze axe') with the exact SEO keywords where they fit naturally.
4. If a keyword cannot be injected naturally, skip it.

OUTPUT INSTRUCTIONS:
Return the updated JSON object:
{{
  "ulf_hook_seo": "...",
  "grandpa_legend_seo": "...",
  "conrad_chronicle_seo": "...",
  "tags": ["comma", "separated", "list", "of", "used", "keywords"]
}}""",
            temperature=0.1
        )
    def build_seo_prompt(self, draft_json: str, seo_keywords: str) -> str:
        return self.build_prompt(draft_json=draft_json, seo_keywords=seo_keywords)

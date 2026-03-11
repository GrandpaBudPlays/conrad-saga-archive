import json
from typing import cast
from ai.gemini import GeminiModel
from file_manager import SessionData, save_audit_report
from prompts import get_prompt_library
from prompts.audit import AuditPrompt
from workflows.base import Workflow


def json_to_audit_markdown(data: dict, session: SessionData) -> str:
    md = f"# 🛡️ CONTENT AUDIT REPORT: {session.full_ep_id}\n\n"
    md += f"* **Total Stream Duration:** {int(session.duration // 60):02d}:{int(session.duration % 60):02d}\n"
    md += f"* **Total Seconds:** {int(session.duration)}\n"
    md += f"* **Primary Biome:** {session.biome}\n"
    md += "* **Grandpa Rule Status:** Plain Speech / Helpful Exile Guidance\n\n"
    md += "---\n\n"

    pa = data.get('production_assistant', {})
    md += "## 📋 ROLE 1: PRODUCTION ASSISTANT (Technical Audit)\n\n"
    md += "### 1.1 SPEECH METRICS\n"
    md += "* **Filler Word Count:**\n"
    for fw in pa.get('filler_words', []):
        md += f"    * \"{fw.get('word', 'N/A')}\": {fw.get('count', 0)} | {fw.get('seconds_per_count', 0)} (Seconds/Count)\n"
    
    other = pa.get('other_filler', [])
    if other:
        md += f"    * **Other:** {sum(o.get('count', 0) for o in other)}\n"
        for o in other:
            md += f"        * \"{o.get('word', '')}\": {o.get('count', 0)}\n"
            
    md += "\n### 1.2 AUDIO & PACING\n"
    md += f"* **Vocal Presence:** {pa.get('vocal_presence_wpm', 0)} WPM\n"
    md += f"* **Technical Quality:** {pa.get('technical_quality_notes', 'N/A')}\n"
    md += f"* **Thematic Silence:**\n"
    for silence in pa.get('thematic_silence', []):
        md += f"    * {silence}\n"
    md += "\n---\n\n"
    
    cd = data.get('creative_director', {})
    md += "## 🎨 ROLE 2: CREATIVE DIRECTOR (Linguistic & Persona Audit)\n\n"
    md += "### 2.1 LINGUISTIC ALIGNMENT\n"
    md += "* **Lexicon Saturation:**\n"
    md += f"    * **Saga Terms:** {cd.get('saga_terms_count', 0)}\n"
    md += f"    * **Technical Terms:** {cd.get('technical_terms_count', 0)}\n"
    md += f"    * **Saturation Ratio:** {cd.get('saturation_ratio', '0:0')}\n"
    
    md += "* **Grandpa Rule Compliance (Plain Speech & Guidance):**\n"
    md += f"    * **Helpful Insights:** {cd.get('helpful_insights_count', 0)}\n"
    md += f"    * **Persona Breaks:** {cd.get('persona_breaks_count', 0)}\n"
    
    refs = cd.get('refinements', [])
    if refs:
        md += "    * **Refinement:**\n"
        for ref in refs:
            md += f"        * *Original:* \"{ref.get('original', '')}\"\n"
            md += f"        * *Correction:* \"{ref.get('correction', '')}\"\n"
            
    md += "\n### 2.2 PERSONA INTEGRITY\n"
    md += f"* **Modernism Audit:** {', '.join(cd.get('modernism_audit', []))}\n"
    md += f"* **Grandpa Wisdom:** {cd.get('grandpa_wisdom_count', 0)}\n"
    md += f"* **Fourth Wall Breaks (Meta-Speech):** {cd.get('meta_speech_breaks_count', 0)}\n"
    md += "\n---\n\n"
    
    sa = data.get('strategic_analyst', {})
    md += "## ⚔️ ROLE 3: STRATEGIC ANALYST (Performance Audit)\n\n"
    md += "### 3.1 MECHANICAL DISCIPLINE\n"
    md += "* **Shieldmaiden’s Rule (Preparation):**\n"
    md += f"    * **Rested Uptime:** {sa.get('rested_uptime_percent', 0)}%\n"
    md += f"    * **Food Uptime:** {sa.get('food_uptime_percent', 0)}%\n"
    md += f"* **Safety Protocol:** {sa.get('safety_protocol_notes', 'N/A')}\n\n"
    
    md += "### 3.2 PERFORMANCE OUTCOMES\n"
    md += f"* **Session Goal Status:** {sa.get('session_goal_status', 'N/A')}\n"
    md += f"* **Highlight Gold:**\n"
    for hg in sa.get('highlight_gold', []):
        md += f"    * {hg}\n"
    md += f"* **Strategic Growth:** {sa.get('strategic_growth_goal', 'N/A')}\n"

    return md


class FeedbackWorkflow(Workflow):
    """Generates the tactical Feedback report."""
    
    def execute(self, session: SessionData, model: GeminiModel) -> None:
        print("Starting Tactical Feedback...")
        
        prompts = get_prompt_library("valheim")
        audit_prompt: AuditPrompt = cast(AuditPrompt, prompts.get("audit"))
        
        prompt = audit_prompt.build_audit_prompt(
            episode_id=session.full_ep_id,
            duration=str(int(session.duration)),
            biome=session.biome,
            lexicon_context=session.lexicon,
            transcript=session.transcript
        )
        
        temperature = audit_prompt.get_temperature(model.name)
        result = model.generate(
            prompt,
            system_instruction=audit_prompt.get_system_instruction(),
            temperature=temperature,
            response_mime_type="application/json"
        )
        
        if not result.success:
            raise RuntimeError(f"Failed to generate audit content: {result.error}")
            
        try:
            data = json.loads(result.content)
            markdown_content = json_to_audit_markdown(data, session)
            
            # Save raw JSON
            save_audit_report(session.path, json.dumps(data, indent=2), "Audit", f"{result.model_name}-raw", ".json")
            # Save Human-Readable Markdown
            save_audit_report(session.path, markdown_content, "Audit", result.model_name)
        except json.JSONDecodeError as e:
            print(f"JSON decode failed for Feedback. Falling back to raw text. Error: {e}")
            save_audit_report(session.path, result.content, "Audit", result.model_name)
            
        print("Feedback Report Complete.")

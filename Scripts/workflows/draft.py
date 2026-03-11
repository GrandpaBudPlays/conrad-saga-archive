import os
import json
from typing import cast
from ai.gemini import GeminiModel
from file_manager import SessionData, save_audit_report, read_file
from prompts.draft import DraftExtractionPrompt, DraftCreativePrompt, DraftSEOPrompt
from workflows.base import Workflow

class DraftWorkflow(Workflow):
    """The 4-pass Description Draft Pipeline."""
    def execute(self, session: SessionData, model: GeminiModel) -> None:
        pass_name = os.getenv("DRAFT_PASS", "1")
        print(f"Executing Draft Workflow - Pass {pass_name}")
        
        # Paths
        base_dir = os.path.dirname(session.path)
        reports_dir = os.path.join(base_dir, "Reports")
        base_name = os.path.basename(session.path).replace(" Transcript.md", "")
        
        extraction_json_path = os.path.join(reports_dir, f"{base_name} Extraction.json")
        hints_path = os.path.join(base_dir, "hints.txt")
        seo_path = os.path.join(base_dir, "seo.txt")
        
        # Load Prompts (Mocking get_prompt_library behavior for now)
        extraction_prompt = DraftExtractionPrompt()
        creative_prompt = DraftCreativePrompt()
        seo_prompt = DraftSEOPrompt()

        if pass_name == "1":
            print("--- Pass 1: Extraction ---")
            hints = read_file(hints_path) if os.path.exists(hints_path) else ""
            if hints:
                print(f"Loaded hints from {hints_path}")
                
            prompt = extraction_prompt.build_extraction_prompt(session.transcript, hints)
            result = model.generate(
                prompt,
                system_instruction=extraction_prompt.get_system_instruction(),
                temperature=extraction_prompt.config.temperature,
                response_mime_type="application/json"
            )
            
            if not result.success:
                raise RuntimeError(f"Pass 1 Failed: {result.error}")
                
            save_audit_report(session.path, result.content, "Extraction", None, ".json")
            print(f"\nPass 1 Complete! Review the factual events in:\n{extraction_json_path}")
            print("\nTo continue to Pass 2 (Creative Writing), run the same command with '--continue'")
            return
            
        elif pass_name == "2":
            print("--- Pass 2: The Triple-Threat Creative Draft ---")
            if not os.path.exists(extraction_json_path):
                print(f"Error: Extraction file not found at {extraction_json_path}.")
                print("You must run Pass 1 first (omit --continue flag).")
                return
                
            events_json = read_file(extraction_json_path)
            if not events_json:
                print("Error: Extraction.json is empty.")
                return
                
            # Load Brand/Persona files
            global_core = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "000-Global-Core")
            valheim_root = os.path.dirname(base_dir) # Chronicles-Of-The-Exile
            valheim_base = os.path.dirname(valheim_root) # 010-Valheim
            
            # NOTE: paths are hardcoded for now, should be dynamic based on your actual structure
            ulf_persona = read_file(os.path.join(valheim_root, "Ulf Persona.md")) or ""
            descriptions_protocol = read_file(os.path.join(valheim_base, "Descriptions.md")) or ""
            brand_context_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(base_dir))), "Personal-Notes", "Brand-Context.md")
            brand_context = read_file(brand_context_path) or ""
            
            print(f"Loaded {len(events_json)} bytes of events. Injecting Ulf, Grandpa, and Conrad voices...")
            
            prompt = creative_prompt.build_creative_prompt(
                events_json=events_json,
                brand_context=brand_context,
                ulf_persona=ulf_persona,
                descriptions_protocol=descriptions_protocol
            )
            
            result = model.generate(
                prompt,
                system_instruction=creative_prompt.get_system_instruction(),
                temperature=creative_prompt.config.temperature,
                response_mime_type="application/json"
            )
            
            if not result.success:
                raise RuntimeError(f"Pass 2 Failed: {result.error}")
                
            # Parse and save the draft
            try:
                draft_data = json.loads(result.content)
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error in Pass 2: {e}")
                save_audit_report(session.path, result.content, "Draft - Raw Error", None, ".json")
                return

            # Check if SEO Pass 3 is needed
            seo_keywords = read_file(seo_path) if os.path.exists(seo_path) else ""
            
            if not seo_keywords:
                print("\n--- No seo.txt found. Skipping Pass 3. Generating final markdown... ---")
                final_md = self._build_markdown(draft_data, draft_data, session)
                save_audit_report(session.path, final_md, "Description", None, ".md")
                save_audit_report(session.path, json.dumps(draft_data, indent=2), "Draft", None, ".json")
                print("\nDraft Pipeline Complete.")
                return
                
            print("\n--- Pass 3: SEO Injection ---")
            print(f"Loaded SEO Keywords from {seo_path}")
            
            seo_prompt_text = seo_prompt.build_seo_prompt(draft_json=json.dumps(draft_data), seo_keywords=seo_keywords)
            seo_result = model.generate(
                seo_prompt_text,
                system_instruction=seo_prompt.get_system_instruction(),
                temperature=seo_prompt.config.temperature,
                response_mime_type="application/json"
            )
            
            if not seo_result.success:
                raise RuntimeError(f"Pass 3 Failed: {seo_result.error}")
                
            try:
                seo_data = json.loads(seo_result.content)
                final_md = self._build_markdown(draft_data, seo_data, session)
                
                # Save outputs
                save_audit_report(session.path, json.dumps(draft_data, indent=2), "Draft - Original", None, ".json")
                save_audit_report(session.path, json.dumps(seo_data, indent=2), "Draft - SEO", None, ".json")
                save_audit_report(session.path, final_md, "Description", None, ".md")
                
                print("\nDraft Pipeline Complete with SEO!")
                
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error in Pass 3: {e}")
                save_audit_report(session.path, seo_result.content, "Draft - SEO Raw Error", None, ".json")
                return


    def _build_markdown(self, original_data: dict, final_data: dict, session: SessionData) -> str:
        md = f"# 📝 Triple-Threat Description: S{session.season} E{session.episode}\n\n"
        
        # Use SEO data if available, fallback to original
        ulf = final_data.get("ulf_hook_seo", final_data.get("ulf_hook", original_data.get("ulf_hook", "")))
        legend = final_data.get("grandpa_legend_seo", final_data.get("grandpa_legend", original_data.get("grandpa_legend", "")))
        chronicle = final_data.get("conrad_chronicle_seo", final_data.get("conrad_chronicle", original_data.get("conrad_chronicle", "")))
        tags = final_data.get("tags", [])
        
        md += "## 🪓 The Narrative\n\n"
        md += f"**[Ulf's Voice]**\n{ulf}\n\n"
        md += f"**[Grandpa's Legend]**\n{legend}\n\n"
        md += f"**[Conrad's Chronicle]**\n{chronicle}\n\n"
        
        md += "---\n\n"
        md += "## 🔗 Standard Link Repository\n"
        md += "[Insert Link Repository from Brand-Context.md here]\n\n"
        
        md += "## 🗺️ The Exile's Map (Chapters)\n"
        md += "[Run the 'Gold' pipeline to extract chapters]\n\n"
        
        md += "## 🏷️ SEO & Metadata\n"
        if tags:
            md += "**Injected Tags:** " + ", ".join(tags) + "\n"
        else:
            md += "*No SEO injection performed.*"
            
        return md

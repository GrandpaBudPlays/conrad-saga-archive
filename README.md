# 🛡️ THE CONRAD SAGA ARCHIVE
**Creator:** Grandpa Bud (Grandpa Plays Valheim)

A master repository for live stream transcripts and lore. This archive serves as a "Gold Mine" for searching raw dialogue and creating edited series.

## 📺 PLAYLISTS
* **[Chronicles of the Exiled (Solo)](https://www.youtube.com/playlist?list=PLLLwpTakAlMs3EAexfe5GWeR0byjILky6)**
* **[Heirs of the Tenth World (Grandkids)](https://www.youtube.com/playlist?list=PLLLwpTakAlMvMevVaRG4wp8zZEiDTyb60)**

---

## 🗂️ REPOSITORY ORGANIZATION
The archive is split into two primary branches to distinguish solo survival from legacy gameplay:

### 🧔 CONRAD (Solo Saga)
Located in `/Stream-Archive/010-Valheim/Chronicles-Of-The-Exile`. These files document the journey of the Exile.
* **Saga I - IV**: From the Meadows to the Mountains.

### 🧒 HEIRS (Grandkids Saga)
Located in `/Stream-Archive/010-Valheim/020-Heirs/`. These files will document the adventures of the next generation.
* **Saga I**: The Heirs' first steps into the Tenth World. (TBD)


### ✨ Google Gemini Stream Analysis Automation
Located in '/Stream-Archive/Scripts/'. These files are used to perform automated review on YouTube transcripts.

#### Audit Pipeline Architecture
The `Audit_Pipeline.py` orchestrates the AI analysis of gameplay transcripts. It leverages a modular design:
- **`file_manager.py`**: Centralizes file I/O, locates metadata, and skips "No Audio" files to save API costs.
- **`ai/gemini.py`**: A robust wrapper for the `google.genai` SDK handling rate limits, timeouts, token cost tracking, and automatic fallback models.
- **`prompts/`**: A library managing AI instructions for the Tactical Audit (Lexicon, filler words) and Strategic Gold Extraction (Shorts, Clips, Chapters).

**Workflow:**
1. Loads the transcript and required metadata via `prepare_session_assets()`.
2. **Pass 1:** Evaluates the episode against the "Grandpa Rule" persona constraints.
3. **Pass 2:** Identifies highlight moments and generates YouTube chapters.
4. Outputs actionable Markdown reports to the `Reports/` directory.

---

## 🛠️ KEY DOCUMENTS
* **[Brand Identity & Survival Wisdom](./000-Global-Core/Brand-Voice.md)**: Rules for voice, lore, and "Elder's Wisdom" tips.
* **[Project Roadmap](./todo.md)**: Upcoming premieres and production tasks. Focus has been on Automation and this is falling behind.

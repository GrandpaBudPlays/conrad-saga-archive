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
Located in `/Stream-Archive/Scripts/`. These files are used to perform automated AI review and content generation on YouTube transcripts.

#### The Brand Orchestrator (`Brand.py`)
`Brand.py` is the central command-line interface for the AI automation pipeline. It reads raw stream transcripts, applies brand-specific persona rules (e.g., Grandpa Bud, Ulf), and generates formatted Markdown reports for YouTube descriptions, shorts clipping, and performance audits. 

It leverages a modular design:
- **`file_manager.py`**: Centralizes file I/O, locates metadata, and skips "No Audio" files to save API costs.
- **`ai/gemini.py`**: A robust wrapper for the `google.genai` SDK handling rate limits, timeouts, token cost tracking, and automatic fallback models. It forces structured JSON output to guarantee pipeline stability.
- **`prompts/`**: A library managing AI instructions for the Tactical Audit, Strategic Gold Extraction, and Creative Drafting.

#### 💻 CLI Commands & Operations
Run the orchestrator from the terminal using the following syntax:
```bash
python Scripts/Brand.py <Operation> <Season> <Episode> [--continue]
```
*Example: `python Scripts/Brand.py Draft S01 E005`*

| Operation | Description | Primary Output (`Reports/` directory) |
| :--- | :--- | :--- |
| **`Audit`** | Runs **both** `Feedback` and `Gold` operations sequentially. | Both Audit & Gold `.md` and `.json` files. |
| **`Feedback`** | Generates a tactical audit of the stream. Evaluates filler words, pacing, and adherence to the "Grandpa Rule" (Plain Speech & Guidance). | `{Ep} Audit.md` (Markdown report) |
| **`Gold`** | Extracts strategic highlights. Identifies moments for Shorts (Type A), Clips (Type B), Saga Montages (Type C), and generates strict YouTube Chapters. | `{Ep} Gold.md` (Markdown report) |
| **`Draft`** | A 4-Pass pipeline to generate the Triple-Threat YouTube Description. <br><br>**Pass 1:** Extracts factual events and pauses the script for human review. <br>**Pass 2:** (Requires `--continue` flag) Writes the narrative hook (Ulf), lore legend (Grandpa), and chronicle (Conrad). <br>**Pass 3:** Automatically injects SEO keywords if `seo.txt` exists in the episode folder. | `{Ep} Extraction.json` (Pass 1 Timeline) <br>`{Ep} Description.md` (Final YouTube Text) |

*(Note: Every operation also outputs raw `-raw.json` files alongside the `.md` reports for future programmatic automation and debugging).*

---

## 🛠️ KEY DOCUMENTS
* **[Brand Identity & Survival Wisdom](./000-Global-Core/Brand-Voice.md)**: Rules for voice, lore, and "Elder's Wisdom" tips.
* **[Project Roadmap](./todo.md)**: Upcoming premieres and production tasks. Focus has been on Automation and this is falling behind.

# BRAND-CLI: MOUNTAIN SAGA STRATEGY

## 1. SAGA GOALS (The "North Star")
> File: `~/Stream-Archive/010-Valheim/Chronicles-Of-The-Exile/Saga IV/Saga_Goals.json`

### Progression Milestones
* **Logistics:** Establish a "Wolf-Proof" Mountain Outpost with a functional portal hub.
* **Exploration:** Locate and clear at least 3 Frost Caves / Ruined Spires.
* **Gear Status:** Craft and fully upgrade the Wolf Armor set and the Draugr Fang (or equivalent).
* **The Finale:** Locate the sacrifice altar and defeat the Biome Boss (Moder).

### Narrative & Entertainment Goals
* **The Vibe:** "Survival Against the Elements" — Emphasize the danger of the cold and the verticality of the terrain.
* **Grand Project:** Construct "The Sky-Reach Tower," a vertical base at the highest peak discovered.
* **Viewer Hook:** "Grandpa Bud vs. Gravity" — A running tally of accidental falls or "Death Runs."

### Anti-Stagnation Rules (The Saga III Clause)
* **The 2-Episode Limit:** If a specific resource (e.g., Silver Veins or Dragon Eggs) is not found within two consecutive episodes, the third episode MUST pivot to a "Search & Rescue" theme or a community-driven "Base Improvement" stream to avoid the "Axe Grind" fatigue.

---

## 2. EPISODE PLANNING WORKFLOW (The Logic)

### Step 1: Data Ingestion
The CLI runs a pre-check on the following files:
* `Saga_Goals.json` (What are we trying to do long-term?)
* `Last_Gold_Report.json` (What did we actually finish?)
* `Last_Feedback.json` (What tech or pacing issues did we face?)

### Step 2: Gap Analysis
* Compare *Current State* vs. *Saga Milestones*.
* Identify if "Stagnation Rules" are triggered.

### Step 3: Plan Generation (`Plan.md`)
The CLI generates a structured output for the OBS clipboard:

1. **The Hook:** * A 30-60 second scripted intro summarizing the "Story So Far."
2. **The "Big Three" Objectives:**
   * **Objective A:** Progress (e.g., "Find one Silver Vein").
   * **Objective B:** Narrative (e.g., "Decorate the hearth room").
   * **Objective C:** The Pivot (e.g., "If no Silver is found by hour 1, start the 'Wolf Taming' challenge").
3. **Engagement Prompts:**
   * Suggestions for questions to ask the chat during "grind" moments.
4. **Technical Checklist:**
   * Reminders based on previous Feedback Reports (e.g., "Check bit-rate," "Reset camera crop").
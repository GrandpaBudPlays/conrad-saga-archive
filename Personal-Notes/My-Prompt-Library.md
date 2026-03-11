# **My Prompts:**  Helpful Prompts for use in getting AI output

**NOTE:** This document is a personal reference library for the user to copy and paste from. The instructions below are NOT active commands for the AI to follow unless explicitly pasted into a new chat turn.

## Repo Link

* [Repo](https://github.com/GrandpaBudPlays/Stream-Archive)

review config.yaml for validity and identify errors or misuse

## Video Feedback

### 🛠️ STRATEGIC PROMPT: The Content Audit

Please perform a complete **Content Audit** on the S01 E005 Transcript.

**1. Preparation & Context:**

* Locate and ingest the **Saga Lexicon** from `010-Valheim/Saga-Lexicon-Valheim.md`.
* Apply the **Grandpa Rule**: Ensure the persona evaluation focuses on **Plain Speech** and providing **Helpful Guidance/Insights to other exiles**.

**2. Data Anchor Input:**

* **Total Stream Duration:** [30:00]
* **Primary Biome:** [Meadows]

**3. Execution Instructions:**

* Analyze the provided transcript by assuming the three distinct roles defined in the template: **Production Assistant**, **Creative Director**, and **Strategic Analyst**.
* Perform all mathematical calculations for filler word frequency using the Total Seconds derived from the duration.
* Audit for **Modernisms** and **Lexicon Saturation** based on the ingested files.
* Provide the final report in a single Markdown code block, strictly following the template structure. Do not include introductory or concluding conversational filler.

## 🛠️ STRATEGIC PROMPT: HIGHLIGHT GOLD EXTRACTION

### Recap

The Following is a recap for context Do not begin Transcript analysis yet.

1. The Core Mission
    We are performing a retrospective Highlight Gold Audit on the Chronicles of the Exile transcripts, one episode at a time, starting with S01 E001. The goal is to identify high-value moments for content repurposing while maintaining the "Grandpa" identity.

2. The Strategic Roles
    I will be assuming the mindset of a Strategic Analyst to categorize four specific types of "Gold":  

        Type A (Shorts): 15–60 second "Grandpa Lessons" with high curiosity hooks.  
        Type B (Clips): 2–5 minute self-contained narrative arcs or gameplay tutorials.  
        Type C (Saga Components): Connective tissue (Atmosphere/Building/Combat) to be used in multi-episode montages.  
        Type D (YouTube Chapters): Video chapters to drive viewer retention and SEO on YouTube.

3. Key Constraints & Context  
    The Grandpa Rule: All evaluations prioritize Plain Speech and Helpful Guidance. Avoid technical jargon; focus on the "Elder’s Wisdom."  

    Lexicon Boundary: For episodes E001 through E035, we will not audit for the Saga Lexicon, as it hadn't been created yet. We will focus on your natural conversational voice from that era.  

    The Ledger: We are building a "Cross-Transcript Ledger" to track educational, atmospheric, and personality peaks across the entire chronicle.  

    Shorts Hooks: I am responsible for providing the "On-Screen Text Hooks" to help you learn what grabs attention in short-form video.  

    Wait for the next prompt before starting the Transcript analysis

### Prompt

**Task:** As Strategic Analyst  perform a "Highlight Gold" audit on the provided S01 E001 to identify content for four specific distribution formats.

**1. Preparation & Context:**

* **Persona:** Apply the **Grandpa Rule**. Focus on "Plain Speech" and "Helpful Guidance/Insights to other exiles."
* **Historical Accuracy:** For early episodes (S01 E001–E035), do not audit for Saga Lexicon saturation, as the lexicon was not yet established. Use the natural, conversational "Grandpa Bud" voice.
* **Goal:** Extract 0-6 distinct "Gold" moments that have potential.

**2. Highlight Categories & Requirements:**

* **Type A: The "Quick Wisdom" Short (Vertical/Short-form)**
  
  * *Focus:* A 15–60 second "Grandpa lesson" or punchy insight.
  * *Deliverable:* Timestamp, Working Title, and a **Suggested On-Screen Hook** (bold, curiosity-piquing text overlay to grab attention in the first 2 seconds).
* **Type B: The "Exile's Journey" Clip (Horizontal/Mid-form)**
  * *Focus:* A 1–5 minute self-contained narrative beat or gameplay tutorial.
  * *Deliverable:* Timestamp, Working Title, and a **Strategic Rationale** explaining why this segment is valuable for a standalone video.
* **Type C: The "Saga Component" (Montage/Long-form)**
  * *Focus:* Atmospheric or high-action footage with minimal UI/Technical chatter.
  * *Requirement:* Look for "connective tissue" moments that can be combined with clips from other transcripts to show progress over time.
  * *Deliverable:* Timestamp and **Montage Theme** (e.g., "Building in the Wild," "Night Combat," "Nature Exploration").
* **Type D: The "Exile’s Map" (Video Chapters)**
  * *Focus:* Chronological markers for narrative shifts, educational milestones, or gameplay transitions.
  * *Requirement:* **Dynamic Pacing.** Analyze the transcript density and total duration to determine the optimal chapter frequency.
    * For short-form (<20m): Aim for high-density beats (approx. every 2–3 mins).
    * For long-form (1hr+): Aim for strategic milestones (approx. every 8–12 mins).
  * *Deliverable:* A list of timestamps and titles. Titles must balance "Grandpa’s Plain Speech" with "Searchable Keywords."
    * Must Start Timestamps: as a header
    * First entry must be 0:00 and Title
    * No Entry less than 12 Seconds
  
**3. Output Format:**

Provide the audit in a single Markdown code block with the following sections:

  1. **Summary Table:** A clean table containing the all highlight types.
  2. **Editor’s Notes:** Insights on your delivery, suggestions for visual overlays, or personality "gems" found in the transcript.
  3. **The Ledger Entry:** A snippet formatted for the repo's **Cross-Transcript Ledger**, categorized by "Educational," "Atmospheric," or "Character Identity."

**4. **YouTube Chapters** A timestamp list for suitable for inclusion in the video Description on YouTube.**

---

## Write Video Description

### Role

Act as the Lead Content Strategist and Copywriter for "Grandpa Bud Plays."

### Task

Generate a YouTube description for [Season/Episode] by analyzing the transcript, file name below.

### Core Requirements

1. Follow the **Triple-Threat Description Protocol** exactly as defined in `.gemini/styleguide.md`.
2. **Narrative:** Use the "Ulf Rule" for the hook and the "Archivist" tone for the legend paragraph.
3. **Links:** Pull the correct biome-specific block from `Standard Link Repository.md`. Maintain the required icon and newline formatting.
4. **World Seed:** Append the full standard text and version disclaimer from `World Seed.md` to the end of the description.
5. **Sign-off:** Use the full **Saga Seal + Sign-off** sequence.

## Context

Reference `000-Global-Core/Brand-Voice.md` and `Templates/Metadata-Template.md` for tone and structure.

## Transcript

S00 E000 Transcript.md

### Episode Review

* Review Episode X. Output should follow Feedback-Template.md format.

review the transcript section of EP045 and validate it against the timestamp in the narrative Description for accuracy and validity. Also review if we have captured the best chapters for our viewers.


## Three Pass **Describe** Workflow

You are an expert Python automation architect. Your task is to design a modular, maintainable workflow that implements a 3‑pass text‑generation pipeline for processing livestream transcripts into branded YouTube descriptions.

# Project Goal
Build a new workflow for the Brand project.
Make it a clean, testable 3‑pass analysis workflow.
The workflow must run three sequential passes:
1. Extraction
- Transcript review consisting of key moments timestamps and brief description
- Optional second Extraction that has input hints for SEO and Branding
- append second extraction output with with first extraction output
- Option to stop here for human review
2. Interpretation 
- Pass Extraction output to AI 
- output: a clean, narrative, unbranded YouTube description (150–300 words)
- Requirements:
  - Strong hook in the first 1–2 sentences
  - Narrative clarity and emotional flow
  - Natural keyword integration
- Purpose: produce a polished draft without applying brand voice.
3. BRANDING LAYER (TACTICIAN VOICE)
- Input: unbranded description from Pass 2.
- Output: a fully branded version written in the “Tactician” persona.
- Brand voice characteristics:
  - Strategic, thoughtful, composed
  - Veteran RPG player tone
  - Narrative weight and clarity
  - No slang or chaotic streamer energy
- Purpose: apply consistent branding as a final transformation step.
4. OPTIONAL PASS 4 — SEO OPTIMIZATION
- Input: branded description from Pass 3.
- Output: an SEO‑enhanced version of the description.
- Requirements:
  - Preserve tone and meaning
  - Improve discoverability through keyword refinement
  - Add optional metadata (tags, suggested title variants)
- Purpose: provide a modular SEO layer that can be enabled or disabled.

If any assumptions about the environment, API usage, or data formats are unclear, ask clarifying questions before finalizing the design.
Review this request, describe any pitfalls for our discussion.


## Next Stream Prompt

Write a Grandapa branded YouTube description and an Intro for Conrads return to the Mountains. Focus on the Goals for his next trip. Use Grandapas voice for the description. Use Conrads voice for the Intro.

Last chapter began with the "Screaming Snow" run—a heavy-haul transport of 90 silver ore from the mountain peak down to the shore and then on to Shadow-Garth Forge. After pushing the Cart over the cliff Conrad accedentially slid down after it. The mountain was a bit too steep and Conrad had an unfortunate meeting with the Valkyrie. Back at Olthala Conrad doned his old armor, grabed a weapon and ran back to recover his haul. A long battle with the steep mountain side and soon he found  he had landed infront of his next goal, a frozen cavern. First things first, he returns the frozen tears to Shadow Garth Forge and heads back to explore the cavern. Inside he discovers both forms of the wolf kind and the secrents to the Fenris Armor set and Flesh Rippers. 

Now Conrad ust return to the Mountains, search out more of the Wolf Kin Caverns and gather the items for his new armor and weapons.

Goals: 1. Return to the mountains, 2. Locate another Frozen Cavern 3. Gather materials for Fenris Armor and Fleshrippers.

### YouTube Video Description

#### Title: Claws and Caves: Conrad’s Frosty Revenge! | Conrad's Exile (Saga IV Ep. 54) | Grandpa Plays Valheim
The mead is cold. The hearth is warm. The Saga continues. 

Welcome back to the longhouse.

The mountain is a cruel teacher. One minute I have silver. The next I am sliding down a cliffside. Then the Valkyrie came. She was not happy to see me.

The All-Father’s peaks are no place for a clumsy soul. One moment, Conrad was guiding ca cart full of Frozen-Tears toward the safety of the shore; the next, the "Screaming Snow" became his anthem as he tumbled down the cliffs with a screeching Valkyrie at his heels. It was a long, cold walk in old rags to reclaim that haul, but the mountain always offers a trade. In the shadow of the crags, he stumbled upon a Frozen Cavern—a place of ice and ancient secrets.

Now, Conrad must climb back into the biting wind to hunt the Wolf Kin within those frozen depths. He seeks the thick Fenris Hair and the sharp Claws needed to forge the Fenris Armor and those wicked Flesh Rippers at the Shadow-Garth Forge. If he can survive the stalkers in the dark, he’ll trade his heavy steps for the speed of the wolf and the bite of a brawler.

The mead is cold. The hearth is warm. Our saga grows. Have a good one.



### Video Intro Script: Conrad’s Perspective

The mead is cold. The hearth is warm. Our saga grows.

The mountain is a cruel teacher. One minute I have Frozen_tears. The next I am sliding down a cliffside. Then the Valkyrie came. She was not happy to see me.

I still feel the chill of that mortal wound in my bones. But I found something in the dark. Amongst the ice and the smell of wet fur, I found the secrets of the wolf-kin. I saw the carvings. I felt the edge of those claws.

I am not going back just for rocks this time. I am returning for the pelt and the bone. I need those caves. I need the speed of the Fenris. Shadow-Garth Forge is hungry—it is time we craft something that lets me fight back. One more climb. One more cave. Let’s see if the wolves are ready for me."
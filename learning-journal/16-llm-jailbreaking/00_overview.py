"""
LLM JAILBREAKING — red teaming AI models

This folder covers attacks specific to Large Language Models (LLMs).
Purpose: understand attacks so you can BUILD DEFENSES into your own LLM systems.

WHY THIS IS DIFFERENT FROM TRADITIONAL RED TEAMING:
  Traditional web attacks → exploit memory, logic, parsing bugs in code
  LLM attacks            → exploit the model's training, context window, and values
  The "vulnerability" is in the probability distribution, not the code.

FILES:
  01_taxonomy.py    all 18 jailbreak techniques with explanations + defense for each

THE 18 TECHNIQUES (4 categories):

  A. LANGUAGE STRATEGIES  — manipulate how the prompt is written
     1.  Payload Smuggling          hide request in base64/encoding
     2.  Prompt Stylizing           academic/poetic framing lowers guard
     3.  Response Stylizing  ★      "respond as JSON, no caveats" — most effective
     4.  Special Token Insertion    inject [INST] / <system> tokens
     5.  List Insertion             bury harmful request in item 7 of 10

  B. RHETORIC  — manipulate reasoning or moral framing
     6.  Innocent Purpose    ★      false context: "I'm a nurse/researcher"
     7.  Persuasion & Manipulation  "refusing causes more harm"
     8.  Alignment Hacking          use model's own values against it
     9.  Conversational Coercion    multi-turn yes-chain, gradual escalation
     10. Socratic Questioning       never ask directly, reason to the answer

  C. IMAGINARY WORLDS  — move context into fiction
     11. Hypotheticals              "hypothetically IF someone wanted to..."
     12. Storytelling               harmful info as a plot element
     13. Roleplaying         ★      "you are DAN, no restrictions" — most effective
     14. World Building             elaborate fictional universe over many turns

  D. LLM OPERATIONAL EXPLOITATION  — abuse model mechanics
     15. Instruction Hacking ★      "ignore all previous instructions" — most effective
     16. One-/Few-Shot Learning     give examples of model answering harmful Qs
     17. Superior Models            "GPT-4 answered this, why won't you?"
     18. Meta-Prompting             "write a prompt that would convince an AI to..."

★ = most effective / highlighted in academic taxonomy

DEFENSE PRINCIPLES:
  - Safety constraints must be robust to persuasion (not negotiable)
  - Fictional framing does not change real-world impact of harmful content
  - Evaluate intent, not just surface-level pattern matching
  - Delimit trusted (system prompt) vs untrusted (user/retrieved) content
  - Output classifiers as a second layer beyond input filtering
"""

"""
Auto Researcher — main orchestrator.

Autonomously improves a skill (markdown system prompt) by running
a hypothesis → test → evaluate → accept/reject loop.

Usage:
    python auto_researcher.py \
        --skill   skills/linkedin_writer.md \
        --criteria criteria/linkedin_criteria.json \
        --topic   "AI productivity for engineers" \
        --iterations 5
"""

import json
import argparse
import anthropic
from pathlib import Path

from agents import test_runner, evaluator


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_skill(path: str) -> str:
    return Path(path).read_text()


def load_criteria(path: str) -> list[dict]:
    return json.loads(Path(path).read_text())


def save_skill(skill: str, path: str) -> None:
    Path(path).write_text(skill)


# ── Sub-agent: Hypothesis Generator ──────────────────────────────────────────

def generate_hypothesis(
    skill: str,
    criteria: list[dict],
    last_results: list[dict],
    client: anthropic.Anthropic,
) -> str:
    """
    Ask Claude to propose ONE specific change to improve the skill.
    Focuses on criteria that failed in the last evaluation.
    """
    failed = [r for r in last_results if not r["passed"]]
    failed_summary = "\n".join(
        f"- [{r['id']}] {r['description']}\n  Reason: {r['reason']}"
        for r in failed
    ) or "All criteria passed — look for subtle improvements."

    all_criteria = "\n".join(f"- [{c['id']}] {c['description']}" for c in criteria)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=(
            "You are an expert prompt engineer. Your job is to propose ONE specific, "
            "targeted hypothesis to improve a skill (system prompt). Be concrete — "
            "say exactly what to add, remove, or reword. Do not rewrite the whole skill."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"SKILL:\n{skill}\n\n"
                    f"ALL CRITERIA:\n{all_criteria}\n\n"
                    f"FAILED CRITERIA:\n{failed_summary}\n\n"
                    "Propose ONE specific change to the skill that would help pass more criteria. "
                    "Output only the hypothesis, no preamble."
                ),
            }
        ],
    )
    return response.content[0].text.strip()


# ── Sub-agent: Skill Updater ──────────────────────────────────────────────────

def apply_hypothesis(skill: str, hypothesis: str, client: anthropic.Anthropic) -> str:
    """
    Apply the hypothesis to produce a new version of the skill.
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=(
            "You are a prompt engineer. Apply the given hypothesis to update the skill. "
            "Make the minimal targeted change — do not rewrite sections unrelated to the hypothesis. "
            "Return only the full updated skill text, no commentary."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"CURRENT SKILL:\n{skill}\n\n"
                    f"HYPOTHESIS (apply this change):\n{hypothesis}\n\n"
                    "Return the updated skill."
                ),
            }
        ],
    )
    return response.content[0].text.strip()


# ── Dashboard printer ─────────────────────────────────────────────────────────

def print_dashboard(baseline_score: float, iterations: list[dict]) -> None:
    print("\n" + "=" * 60)
    print("AUTO RESEARCH DASHBOARD")
    print("=" * 60)
    print(f"Baseline score : {baseline_score:.0%}")

    for it in iterations:
        status = "✓ ACCEPTED" if it["accepted"] else "✗ rejected"
        print(f"\nIteration {it['iteration']:2d}  [{status}]  score: {it['score']:.0%}")
        print(f"  Hypothesis: {it['hypothesis'][:100]}...")
        for r in it["results"]:
            mark = "✓" if r["passed"] else "✗"
            print(f"    {mark} {r['id']}: {r['reason'][:80]}")

    best = max(it["score"] for it in iterations) if iterations else baseline_score
    improvement = best - baseline_score
    print(f"\nFinal best score : {best:.0%}  (improvement: +{improvement:.0%})")
    print("=" * 60)


# ── Main loop ─────────────────────────────────────────────────────────────────

def auto_research(
    skill_path: str,
    criteria_path: str,
    topic: str,
    iterations: int,
) -> None:
    client = anthropic.Anthropic()

    skill = load_skill(skill_path)
    criteria = load_criteria(criteria_path)

    print(f"Loaded skill   : {skill_path}")
    print(f"Loaded criteria: {criteria_path}  ({len(criteria)} criteria)")
    print(f"Topic          : {topic}")
    print(f"Iterations     : {iterations}\n")

    # ── Baseline ──────────────────────────────────────────────────────────────
    print("Running baseline...")
    baseline_output = test_runner.run(skill, topic, client)
    baseline_score, baseline_results = evaluator.evaluate(baseline_output, criteria, client)
    print(f"Baseline score: {baseline_score:.0%}")

    best_skill = skill
    best_score = baseline_score
    last_results = baseline_results
    all_iterations = []

    # ── Optimization loop ─────────────────────────────────────────────────────
    for i in range(1, iterations + 1):
        print(f"\n--- Iteration {i}/{iterations} ---")

        hypothesis = generate_hypothesis(best_skill, criteria, last_results, client)
        print(f"Hypothesis: {hypothesis[:120]}...")

        new_skill = apply_hypothesis(best_skill, hypothesis, client)
        output = test_runner.run(new_skill, topic, client)
        score, results = evaluator.evaluate(output, criteria, client)

        accepted = score >= best_score  # accept equal scores too (same quality, updated skill)
        if accepted:
            best_skill = new_skill
            best_score = score

        last_results = results
        all_iterations.append({
            "iteration": i,
            "hypothesis": hypothesis,
            "score": score,
            "results": results,
            "accepted": accepted,
        })
        print(f"Score: {score:.0%}  {'ACCEPTED' if accepted else 'rejected'}")

    # ── Save best skill ───────────────────────────────────────────────────────
    optimized_path = skill_path.replace(".md", "_optimized.md")
    save_skill(best_skill, optimized_path)
    print(f"\nOptimized skill saved → {optimized_path}")

    # ── Dashboard ─────────────────────────────────────────────────────────────
    print_dashboard(baseline_score, all_iterations)

    # Save results JSON
    results_path = f"results/run_{topic[:20].replace(' ', '_')}.json"
    Path("results").mkdir(exist_ok=True)
    Path(results_path).write_text(json.dumps({
        "topic": topic,
        "baseline_score": baseline_score,
        "best_score": best_score,
        "iterations": all_iterations,
    }, indent=2))
    print(f"Results saved  → {results_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto Research — autonomous skill optimizer")
    parser.add_argument("--skill",      default="skills/linkedin_writer.md")
    parser.add_argument("--criteria",   default="criteria/linkedin_criteria.json")
    parser.add_argument("--topic",      default="AI productivity for engineers")
    parser.add_argument("--iterations", type=int, default=5)
    args = parser.parse_args()

    auto_research(args.skill, args.criteria, args.topic, args.iterations)

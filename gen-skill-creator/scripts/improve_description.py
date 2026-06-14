#!/usr/bin/env python3
"""Improve a skill description based on eval results.

The script is host-agnostic: pass a command template for the model or agent CLI
that should rewrite the description. The prompt is sent on stdin and stdout is
parsed for <new_description> tags.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from scripts.utils import parse_skill_md


def _format_command(command_template: str, model: str | None) -> str:
    return command_template.format(model=model or "")


def _call_backend(
    prompt: str,
    command_template: str,
    model: str | None,
    timeout: int = 300,
) -> str:
    """Run a user-provided command with the prompt on stdin and return stdout."""
    command = _format_command(command_template, model)
    if not command.strip():
        raise ValueError("A non-empty command template is required")

    result = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
        timeout=timeout,
        shell=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"backend command exited {result.returncode}\ncommand: {command}\nstderr: {result.stderr}"
        )
    return result.stdout


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
    command_template: str,
    model: str | None = None,
    test_results: dict | None = None,
    log_dir: Path | None = None,
    iteration: int | None = None,
) -> str:
    """Call the configured improvement backend based on eval results."""
    failed_triggers = [
        r for r in eval_results["results"]
        if r["should_trigger"] and not r["pass"]
    ]
    false_triggers = [
        r for r in eval_results["results"]
        if not r["should_trigger"] and not r["pass"]
    ]

    train_score = f"{eval_results['summary']['passed']}/{eval_results['summary']['total']}"
    if test_results:
        test_score = f"{test_results['summary']['passed']}/{test_results['summary']['total']}"
        scores_summary = f"Train: {train_score}, Test: {test_score}"
    else:
        scores_summary = f"Train: {train_score}"

    prompt = f"""You are optimizing a skill description for an agent skill called "{skill_name}". A "skill" is sort of like a prompt, but with progressive disclosure -- there's a title and description that an agent sees when deciding whether to use the skill, and then if it does use the skill, it reads the .md file which has lots more details and potentially links to other resources in the skill folder like helper files and scripts and additional documentation or examples.

The description appears in the agent's available skills list. When a user sends a query, the agent decides whether to invoke the skill based solely on the title and on this description. Your goal is to write a description that triggers for relevant queries, and doesn't trigger for irrelevant ones.

Here's the current description:
<current_description>
"{current_description}"
</current_description>

Current scores ({scores_summary}):
<scores_summary>
"""
    if failed_triggers:
        prompt += "FAILED TO TRIGGER (should have triggered but didn't):\n"
        for result in failed_triggers:
            prompt += f'  - "{result["query"]}" (triggered {result["triggers"]}/{result["runs"]} times)\n'
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but shouldn't have):\n"
        for result in false_triggers:
            prompt += f'  - "{result["query"]}" (triggered {result["triggers"]}/{result["runs"]} times)\n'
        prompt += "\n"

    if history:
        prompt += "PREVIOUS ATTEMPTS (do NOT repeat these -- try something structurally different):\n\n"
        for item in history:
            train_score = f"{item.get('train_passed', item.get('passed', 0))}/{item.get('train_total', item.get('total', 0))}"
            test_score = f"{item.get('test_passed', '?')}/{item.get('test_total', '?')}" if item.get("test_passed") is not None else None
            score = f"train={train_score}" + (f", test={test_score}" if test_score else "")
            prompt += f"<attempt {score}>\n"
            prompt += f'Description: "{item["description"]}"\n'
            if "results" in item:
                prompt += "Train results:\n"
                for result in item["results"]:
                    status = "PASS" if result["pass"] else "FAIL"
                    prompt += f'  [{status}] "{result["query"][:80]}" (triggered {result["triggers"]}/{result["runs"]})\n'
            if item.get("note"):
                prompt += f'Note: {item["note"]}\n'
            prompt += "</attempt>\n\n"

    prompt += f"""</scores_summary>

Skill content (for context on what the skill does):
<skill_content>
{skill_content}
</skill_content>

Based on the failures, write a new and improved description that is more likely to trigger correctly. Do not overfit to the specific cases shown. Generalize from the failures to broader categories of user intent and situations where this skill would be useful or not useful.

Keep the description under 1024 characters. Focus on user intent, not implementation details. Make it distinctive enough to compete with adjacent skills.

Please respond with only the new description text in <new_description> tags, nothing else."""

    text = _call_backend(prompt, command_template, model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = match.group(1).strip().strip('"') if match else text.strip().strip('"')

    transcript: dict = {
        "iteration": iteration,
        "prompt": prompt,
        "response": text,
        "parsed_description": description,
        "char_count": len(description),
        "over_limit": len(description) > 1024,
    }

    if len(description) > 1024:
        shorten_prompt = (
            f"{prompt}\n\n---\n\n"
            f"A previous attempt produced this description, which at "
            f"{len(description)} characters is over the 1024-character hard limit:\n\n"
            f'"{description}"\n\n'
            f"Rewrite it to be under 1024 characters while keeping the most "
            f"important trigger words and intent coverage. Respond with only "
            f"the new description in <new_description> tags."
        )
        shorten_text = _call_backend(shorten_prompt, command_template, model)
        match = re.search(r"<new_description>(.*?)</new_description>", shorten_text, re.DOTALL)
        shortened = match.group(1).strip().strip('"') if match else shorten_text.strip().strip('"')

        transcript["rewrite_prompt"] = shorten_prompt
        transcript["rewrite_response"] = shorten_text
        transcript["rewrite_description"] = shortened
        transcript["rewrite_char_count"] = len(shortened)
        description = shortened

    transcript["final_description"] = description

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"improve_iter_{iteration or 'unknown'}.json"
        log_file.write_text(json.dumps(transcript, indent=2))

    return description


def main():
    parser = argparse.ArgumentParser(description="Improve a skill description based on eval results")
    parser.add_argument("--eval-results", required=True, help="Path to eval results JSON (from run_eval.py)")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--history", default=None, help="Path to history JSON (previous attempts)")
    parser.add_argument("--command-template", required=True, help="Command to run; prompt is sent on stdin, {model} is optional")
    parser.add_argument("--model", default=None, help="Optional model value inserted into {model}")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    eval_results = json.loads(Path(args.eval_results).read_text())
    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text())

    name, _, content = parse_skill_md(skill_path)
    current_description = eval_results["description"]

    if args.verbose:
        print(f"Current: {current_description}", file=sys.stderr)
        print(f"Score: {eval_results['summary']['passed']}/{eval_results['summary']['total']}", file=sys.stderr)

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        command_template=args.command_template,
        model=args.model,
    )

    if args.verbose:
        print(f"Improved: {new_description}", file=sys.stderr)

    output = {
        "description": new_description,
        "history": history + [{
            "description": current_description,
            "passed": eval_results["summary"]["passed"],
            "failed": eval_results["summary"]["failed"],
            "total": eval_results["summary"]["total"],
            "results": eval_results["results"],
        }],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

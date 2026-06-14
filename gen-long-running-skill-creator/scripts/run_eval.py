#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

The script is host-agnostic. Provide a command template for the agent CLI to run
and either a trigger regex or a temporary registry directory whose generated
wrapper name should appear in backend output when the skill is used.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


def _json(value: str) -> str:
    return json.dumps(value)


def _format_command(
    command_template: str,
    query: str,
    skill_name: str,
    skill_description: str,
    skill_path: str,
    model: str | None,
) -> str:
    return command_template.format(
        query=query,
        query_json=_json(query),
        skill_name=skill_name,
        skill_name_json=_json(skill_name),
        skill_description=skill_description,
        skill_description_json=_json(skill_description),
        skill_path=skill_path,
        skill_path_json=_json(skill_path),
        model=model or "",
    )


def _write_registry_entry(
    registry_dir: Path,
    entry_name: str,
    skill_name: str,
    skill_description: str,
) -> Path:
    registry_dir.mkdir(parents=True, exist_ok=True)
    entry_file = registry_dir / f"{entry_name}.md"
    indented_desc = "\n  ".join(skill_description.split("\n"))
    entry_file.write_text(
        f"---\n"
        f"name: {skill_name}\n"
        f"description: |\n"
        f"  {indented_desc}\n"
        f"---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {skill_description}\n"
    )
    return entry_file


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    skill_path: str,
    timeout: int,
    command_template: str,
    trigger_pattern: str | None = None,
    registry_dir: str | None = None,
    model: str | None = None,
) -> bool:
    """Run one query and return whether the configured detector says it triggered."""
    unique_id = uuid.uuid4().hex[:8]
    entry_name = f"{skill_name}-skill-{unique_id}"
    registry_entry: Path | None = None

    try:
        if registry_dir:
            registry_entry = _write_registry_entry(
                Path(registry_dir),
                entry_name,
                skill_name,
                skill_description,
            )

        command = _format_command(
            command_template,
            query,
            skill_name,
            skill_description,
            skill_path,
            model,
        )
        if not command.strip():
            raise ValueError("A non-empty command template is required")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True,
        )
        combined_output = f"{result.stdout}\n{result.stderr}"
        if trigger_pattern:
            return re.search(trigger_pattern, combined_output, re.MULTILINE) is not None
        return entry_name in combined_output or skill_name in combined_output
    finally:
        if registry_entry and registry_entry.exists():
            registry_entry.unlink()


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    skill_path: Path,
    num_workers: int,
    timeout: int,
    command_template: str,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    trigger_pattern: str | None = None,
    registry_dir: Path | None = None,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []
    owned_registry_dir: tempfile.TemporaryDirectory[str] | None = None
    registry_path: Path | None = registry_dir

    if registry_path is None:
        owned_registry_dir = tempfile.TemporaryDirectory(prefix="skill-trigger-registry-")
        registry_path = Path(owned_registry_dir.name)

    try:
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            future_to_info = {}
            for item in eval_set:
                for run_idx in range(runs_per_query):
                    future = executor.submit(
                        run_single_query,
                        item["query"],
                        skill_name,
                        description,
                        str(skill_path),
                        timeout,
                        command_template,
                        trigger_pattern,
                        str(registry_path) if registry_path else None,
                        model,
                    )
                    future_to_info[future] = (item, run_idx)

            query_triggers: dict[str, list[bool]] = {}
            query_items: dict[str, dict] = {}
            for future in as_completed(future_to_info):
                item, _ = future_to_info[future]
                query = item["query"]
                query_items[query] = item
                if query not in query_triggers:
                    query_triggers[query] = []
                try:
                    query_triggers[query].append(future.result())
                except Exception as error:
                    print(f"Warning: query failed: {error}", file=sys.stderr)
                    query_triggers[query].append(False)
    finally:
        if owned_registry_dir:
            owned_registry_dir.cleanup()

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        did_pass = trigger_rate >= trigger_threshold if should_trigger else trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for result in results if result["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--command-template", required=True, help="Agent CLI command to run; supports {query_json}, {skill_path}, and {model}")
    parser.add_argument("--trigger-pattern", default=None, help="Regex that marks backend output as skill-triggered")
    parser.add_argument("--registry-dir", default=None, help="Optional directory for temporary skill wrapper files")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Optional model value inserted into {model}")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, _ = parse_skill_md(skill_path)
    description = args.description or original_description

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        skill_path=skill_path,
        num_workers=args.num_workers,
        timeout=args.timeout,
        command_template=args.command_template,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        trigger_pattern=args.trigger_pattern,
        registry_dir=Path(args.registry_dir) if args.registry_dir else None,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for result in output["results"]:
            status = "PASS" if result["pass"] else "FAIL"
            rate = f"{result['triggers']}/{result['runs']}"
            print(f"  [{status}] rate={rate} expected={result['should_trigger']}: {result['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

"""Host-agnostic MCP server evaluation harness.

This script connects to an MCP server, loads XML question/answer pairs, and runs
each question through a caller-provided agent command. The command receives a
prompt on stdin and must return <response>, <summary>, and <feedback> tags.
"""

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from connections import create_connection

EVALUATION_PROMPT = """You are an AI agent evaluating an MCP server.

Task:
{question}

Expected answer format:
- Provide summary of each step in <summary> tags.
- Provide feedback on the MCP tools in <feedback> tags.
- Provide the final answer in <response> tags.
- If you cannot solve the task, return <response>NOT_FOUND</response>.
- For numeric responses, provide just the number.
- For IDs, provide just the ID.
- For names or text, provide the exact text requested.

MCP connection info:
{connection_info}

Available MCP tools:
{tools_json}
"""


def parse_evaluation_file(file_path: Path) -> list[dict[str, Any]]:
    """Parse XML evaluation file with qa_pair elements."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        evaluations = []

        for qa_pair in root.findall(".//qa_pair"):
            question_elem = qa_pair.find("question")
            answer_elem = qa_pair.find("answer")

            if question_elem is not None and answer_elem is not None:
                evaluations.append({
                    "question": (question_elem.text or "").strip(),
                    "answer": (answer_elem.text or "").strip(),
                })

        return evaluations
    except Exception as error:
        print(f"Error parsing evaluation file {file_path}: {error}")
        return []


def extract_xml_content(text: str, tag: str) -> str | None:
    """Extract content from XML tags."""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[-1].strip() if matches else None


def parse_headers(header_list: list[str]) -> dict[str, str]:
    """Parse header strings in format 'Key: Value' into a dictionary."""
    headers = {}
    if not header_list:
        return headers

    for header in header_list:
        if ":" in header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        else:
            print(f"Warning: Ignoring malformed header: {header}")
    return headers


def parse_env_vars(env_list: list[str]) -> dict[str, str]:
    """Parse environment variable strings in format 'KEY=VALUE' into a dictionary."""
    env = {}
    if not env_list:
        return env

    for env_var in env_list:
        if "=" in env_var:
            key, value = env_var.split("=", 1)
            env[key.strip()] = value.strip()
        else:
            print(f"Warning: Ignoring malformed environment variable: {env_var}")
    return env


def format_command(command_template: str, model: str | None) -> str:
    return command_template.format(model=model or "")


def run_agent_command(prompt: str, command_template: str, model: str | None, timeout: int) -> str:
    """Run the configured agent command with the evaluation prompt on stdin."""
    command = format_command(command_template, model)
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
            f"agent command exited {result.returncode}\ncommand: {command}\nstderr: {result.stderr}"
        )
    return result.stdout


def connection_info(args: argparse.Namespace) -> str:
    details = {"transport": args.transport}
    if args.transport == "stdio":
        details.update({"command": args.command, "args": args.args or [], "env_keys": [item.split("=", 1)[0] for item in args.env or []]})
    else:
        details.update({"url": args.url, "headers": list(parse_headers(args.headers or []).keys())})
    return json.dumps(details, indent=2)


async def evaluate_single_task(
    qa_pair: dict[str, Any],
    tools: list[dict[str, Any]],
    args: argparse.Namespace,
    task_index: int,
) -> dict[str, Any]:
    """Evaluate a single QA pair with the configured agent command."""
    start_time = time.time()
    print(f"Task {task_index + 1}: Running question: {qa_pair['question']}")

    prompt = EVALUATION_PROMPT.format(
        question=qa_pair["question"],
        connection_info=connection_info(args),
        tools_json=json.dumps(tools, indent=2, default=str),
    )

    try:
        response = await asyncio.to_thread(
            run_agent_command,
            prompt,
            args.agent_command,
            args.model,
            args.timeout,
        )
        error = None
    except Exception as exc:
        response = ""
        error = str(exc)

    response_value = extract_xml_content(response, "response")
    summary = extract_xml_content(response, "summary")
    feedback = extract_xml_content(response, "feedback")
    duration_seconds = time.time() - start_time

    return {
        "question": qa_pair["question"],
        "expected": qa_pair["answer"],
        "actual": response_value,
        "score": int(response_value == qa_pair["answer"]) if response_value else 0,
        "total_duration": duration_seconds,
        "tool_calls": {},
        "num_tool_calls": None,
        "summary": summary,
        "feedback": feedback,
        "error": error,
        "raw_response": response,
    }


REPORT_HEADER = """
# Evaluation Report

## Summary

- **Accuracy**: {correct}/{total} ({accuracy:.1f}%)
- **Average Task Duration**: {average_duration_s:.2f}s

---
"""

TASK_TEMPLATE = """
### Task {task_num}

**Question**: {question}
**Ground Truth Answer**: `{expected_answer}`
**Actual Answer**: `{actual_answer}`
**Correct**: {correct_indicator}
**Duration**: {total_duration:.2f}s

**Summary**
{summary}

**Feedback**
{feedback}

**Error**
{error}

---
"""


async def run_evaluation(eval_path: Path, connection: Any, args: argparse.Namespace) -> str:
    """Run evaluation with MCP server tools and a configured agent command."""
    print("Starting evaluation")

    tools = await connection.list_tools()
    print(f"Loaded {len(tools)} tools from MCP server")

    qa_pairs = parse_evaluation_file(eval_path)
    print(f"Loaded {len(qa_pairs)} evaluation tasks")

    results = []
    for index, qa_pair in enumerate(qa_pairs):
        print(f"Processing task {index + 1}/{len(qa_pairs)}")
        result = await evaluate_single_task(qa_pair, tools, args, index)
        results.append(result)

    correct = sum(result["score"] for result in results)
    accuracy = (correct / len(results)) * 100 if results else 0
    average_duration_s = sum(result["total_duration"] for result in results) / len(results) if results else 0

    report = REPORT_HEADER.format(
        correct=correct,
        total=len(results),
        accuracy=accuracy,
        average_duration_s=average_duration_s,
    )

    report += "".join([
        TASK_TEMPLATE.format(
            task_num=index + 1,
            question=qa_pair["question"],
            expected_answer=qa_pair["answer"],
            actual_answer=result["actual"] or "N/A",
            correct_indicator="yes" if result["score"] else "no",
            total_duration=result["total_duration"],
            summary=result["summary"] or "N/A",
            feedback=result["feedback"] or "N/A",
            error=result["error"] or "N/A",
        )
        for index, (qa_pair, result) in enumerate(zip(qa_pairs, results))
    ])

    return report


async def main():
    parser = argparse.ArgumentParser(
        description="Evaluate MCP servers using test questions and a configured agent command",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python evaluation.py -t stdio -c python -a my_server.py --agent-command "my-agent --stdin" eval.xml
  python evaluation.py -t http -u https://example.com/mcp --agent-command "my-agent --model {model}" -m provider/model eval.xml
        """,
    )

    parser.add_argument("eval_file", type=Path, help="Path to evaluation XML file")
    parser.add_argument("-t", "--transport", choices=["stdio", "sse", "http"], default="stdio", help="Transport type (default: stdio)")
    parser.add_argument("--agent-command", required=True, help="Agent command to run; prompt is sent on stdin and {model} is optional")
    parser.add_argument("-m", "--model", default=None, help="Optional model value inserted into {model}")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per question in seconds")

    stdio_group = parser.add_argument_group("stdio options")
    stdio_group.add_argument("-c", "--command", help="Command to run MCP server (stdio only)")
    stdio_group.add_argument("-a", "--args", nargs="+", help="Arguments for the command (stdio only)")
    stdio_group.add_argument("-e", "--env", nargs="+", help="Environment variables in KEY=VALUE format (stdio only)")

    remote_group = parser.add_argument_group("sse/http options")
    remote_group.add_argument("-u", "--url", help="MCP server URL (sse/http only)")
    remote_group.add_argument("-H", "--header", nargs="+", dest="headers", help="HTTP headers in 'Key: Value' format (sse/http only)")

    parser.add_argument("-o", "--output", type=Path, help="Output file for evaluation report (default: stdout)")

    args = parser.parse_args()

    if not args.eval_file.exists():
        print(f"Error: Evaluation file not found: {args.eval_file}")
        sys.exit(1)

    headers = parse_headers(args.headers) if args.headers else None
    env_vars = parse_env_vars(args.env) if args.env else None

    try:
        connection = create_connection(
            transport=args.transport,
            command=args.command,
            args=args.args,
            env=env_vars,
            url=args.url,
            headers=headers,
        )
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(f"Connecting to MCP server via {args.transport}...")

    async with connection:
        print("Connected successfully")
        report = await run_evaluation(args.eval_file, connection, args)

        if args.output:
            args.output.write_text(report)
            print(f"\nReport saved to {args.output}")
        else:
            print("\n" + report)


if __name__ == "__main__":
    asyncio.run(main())

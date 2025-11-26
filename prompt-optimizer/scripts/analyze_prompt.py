#!/usr/bin/env python3
import sys
import json
from typing import List, Dict, Any

# Keywords based on the principles in SKILL.md
ACTION_VERBS = [
    'fix', 'change', 'replace', 'write', 'create', 'run', 'list', 'find', 'get',
    'update', 'delete', 'add', 'move', 'rename', 'start', 'stop', 'build'
]
EXPLANATION_PHRASES = [
    'how would i', 'how do i', 'what is the command to', 'explain how to',
    'can you tell me how to'
]
TOOL_KEYWORDS = [
    'file', 'directory', 'folder', 'script', 'command', 'service', 'container',
    'docker', 'git', 'codebase', 'repository'
]

def analyze_prompt(prompt: str) -> Dict[str, Any]:
    """
    Analyzes a given prompt against the principles of efficient tool-using prompts.

    Args:
        prompt: The user's prompt string.

    Returns:
        A dictionary containing the analysis results and suggestions.
    """
    prompt_lower = prompt.lower()
    suggestions = []
    score = 0

    # Principle 1: Be Direct and Action-Oriented
    has_action_verb = any(verb in prompt_lower for verb in ACTION_VERBS)
    if has_action_verb:
        score += 1
    else:
        suggestions.append(
            "Suggestion: Frame your request as a direct command. "
            f"Try starting with an action verb like 'fix', 'create', 'run', etc."
        )

    # Principle 2: Request Execution, Not Simulation
    is_explanation_request = any(phrase in prompt_lower for phrase in EXPLANATION_PHRASES)
    if is_explanation_request:
        suggestions.append(
            "Suggestion: Instead of asking 'how to' do something, ask the agent to 'do' it directly. "
            "For example, instead of 'How do I list files?', say 'List all files in the current directory.'"
        )
    else:
        score += 1
        
    # Principle 3: Think in Terms of Tools
    has_tool_keyword = any(keyword in prompt_lower for keyword in TOOL_KEYWORDS)
    if has_tool_keyword:
        score += 1
    else:
        suggestions.append(
            "Suggestion: Try to mention the type of entity you want to interact with "
            f"(e.g., 'file', 'command', 'repository') to help the agent choose the right tool."
        )

    # Final evaluation
    if score == 3:
        evaluation = "✅ This looks like an efficient and actionable prompt."
        suggestions.append("No major issues found. This prompt is direct and likely to be effective.")
    elif score >= 1:
        evaluation = "⚠️ This prompt could be more direct. See suggestions for improvement."
    else:
        evaluation = "❌ This prompt is likely inefficient. It may require clarification."

    return {
        "prompt": prompt,
        "evaluation": evaluation,
        "score": f"{score}/3",
        "suggestions": suggestions
    }

def main():
    """Main function to handle command-line invocation."""
    if len(sys.argv) != 2:
        print("Usage: python analyze_prompt.py \"<your prompt to analyze>\"", file=sys.stderr)
        sys.exit(1)
    
    prompt_to_analyze = sys.argv[1]
    result = analyze_prompt(prompt_to_analyze)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

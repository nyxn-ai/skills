---
name: prompt-optimizer
description: A skill to guide users in crafting token-efficient prompts for tool-using AI agents. Use this when you want to learn how to write better prompts to get faster, more accurate results and save costs.
---

# Prompt Optimizer Guide

This guide provides best practices for writing prompts that help AI agents like me work more efficiently. By following these principles, you can get faster, more accurate results while saving tokens.

The core idea is to frame your requests in a way that allows the AI to move from your natural language instruction to a structured tool call as quickly and accurately as possible.

---

##  Core Principles

### 1. Be Direct and Action-Oriented

State your goal clearly and provide all necessary context upfront. Avoid vague descriptions that require the AI to guess or ask clarifying questions.

*   **Inefficient 👎:** "I have this file, and I think there's a bug in it somewhere, maybe in the calculation part. Can you look at it?"
    *   *Why it's inefficient:* This requires the AI to read the file, search for the "calculation part," and then try to infer the bug, leading to multiple steps and token usage.

*   **Efficient 👍:** "In `calculations.py`, the `calculate_total` function is returning an incorrect value. Fix it by changing the tax rate from `0.05` to `0.07`."
    *   *Why it's efficient:* This clearly identifies the file, function, problem, and solution, allowing the AI to execute a precise `replace` operation in a single step.

### 2. Request Execution, Not Simulation

Ask the AI to *perform* a task directly using its tools, rather than asking it to *explain* how the task would be done.

*   **Inefficient 👎:** "How would I write a shell command to find all `.ts` files in the `src` directory modified in the last day?"
    *   *Why it's inefficient:* This asks the AI to generate text (an explanation), which you then have to execute yourself.

*   **Efficient 👍:** "Find all `.ts` files in the `src` directory modified in the last day."
    *   *Why it's efficient:* This allows the AI to directly use its `run_shell_command` tool to get you the answer immediately.

### 3. Think in Terms of Tools

Frame your request in a way that suggests the appropriate tool. This helps the AI bypass the step of interpreting your intent and map your request directly to an action.

*   **If you want to change a file:**
    *   **Think:** `replace` or `write_file`
    *   **Say:** "In `config.json`, replace the value of `port` with `8080`."

*   **If you want to run a command:**
    *   **Think:** `run_shell_command`
    *   **Say:** "List all running docker containers."

*   **If you need to understand a large codebase:**
    *   **Think:** `codebase_investigator`
    *   **Say:** "Analyze this repository and tell me which files are most important for handling user authentication."

---

By applying these principles, you help reduce ambiguity and conversational turns, leading to a more efficient and powerful interaction.

---

## Interactive Prompt Analyzer

This skill now includes an interactive script to help you analyze your prompts based on the principles above.

### How to Use

You can run the analyzer from your command line:

```bash
python prompt-optimizer/scripts/analyze_prompt.py "Your prompt here"
```

### Example

**Command:**
```bash
python prompt-optimizer/scripts/analyze_prompt.py "How do I find all the text files in my documents folder?"
```

**Output (JSON):**
```json
{
  "prompt": "How do I find all the text files in my documents folder?",
  "evaluation": "⚠️ This prompt could be more direct. See suggestions for improvement.",
  "score": "2/3",
  "suggestions": [
    "Suggestion: Instead of asking 'how to' do something, ask the agent to 'do' it directly. For example, instead of 'How do I list files?', say 'List all files in the current directory.'"
  ]
}
```

import os
import yaml
import subprocess
import json
import unicodedata # Added for sanitize_task_name
import re # Added import for re

# 只需定义一次，全局复用
INVISIBLE_CHARS_PATTERN = re.compile(
    r'[\u200b\u200c\u200d\u200e\u2060\u2061\u2062\u2063\u2064\u2066\u2067\u2068\u2069\u202a-\u202e\ufeff\ufff9-\ufffb]'
)

def sanitize_task_name(name: str) -> str:
    """彻底清除所有零宽字符、BIDI 控制符、BOM 等幽灵字符"""
    if not name:
        return name
    # 第一步：干掉所有已知的零宽/控制字符
    cleaned = INVISIBLE_CHARS_PATTERN.sub('', name)
    # 第二步：再保险起见，干掉所有 Unicode 控制类字符（Cc）
    cleaned = ''.join(ch for ch in cleaned if unicodedata.category(ch)[0] != 'C')
    return cleaned.strip()


def _read_config(project_root):
    """
    Reads the openspec/config.yaml for the given project.
    """
    config_path = os.path.join(project_root, 'openspec', 'config.yaml')
    if not os.path.exists(config_path):
        return {"git_integration": {"enabled": False}} # Default if config doesn't exist

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config if config else {"git_integration": {"enabled": False}}

def _run_git_command(project_root, command_args):
    """
    Runs a git command in the specified project root.
    Returns stdout, stderr, and return code.
    """
    full_command = ['git'] + command_args
    try:
        result = subprocess.run(
            full_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False # Do not raise exception for non-zero exit codes
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except FileNotFoundError:
        return "", "Git command not found. Please ensure Git is installed and in your PATH.", 127
    except Exception as e:
        return "", f"An error occurred while running git command: {e}", 1

def _get_current_git_branch(project_root):
    """
    Gets the current Git branch name for the given project root.
    """
    stdout, stderr, returncode = _run_git_command(project_root, ['rev-parse', '--abbrev-ref', 'HEAD'])
    if returncode == 0:
        return stdout
    return None

def _is_git_repo(project_root):
    """
    Checks if the given project root is a Git repository.
    """
    stdout, stderr, returncode = _run_git_command(project_root, ['rev-parse', '--is-inside-work-tree'])
    return returncode == 0 and stdout == 'true'


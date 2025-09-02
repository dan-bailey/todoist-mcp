"""Allow running the server as python -m todoist_mcp"""

from .cli import cli

if __name__ == "__main__":
    exit(cli())
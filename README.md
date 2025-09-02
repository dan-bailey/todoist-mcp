# Todoist MCP Server

A Model Context Protocol (MCP) server that integrates with Todoist, allowing Claude and other MCP-compatible AI assistants to interact with your Todoist tasks and projects.

## Features

- **Task Management**: Create, read, update, complete, and delete tasks
- **Project Management**: List and manage projects
- **Filtering**: Filter tasks by project, section, labels, or natural language queries
- **Full API Support**: Comprehensive coverage of Todoist's REST API v2

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todoist-mcp
```

2. Install the package:
```bash
pip install -e .
```

3. Set up your Todoist API token:
```bash
cp .env.example .env
# Edit .env and add your Todoist API token
```

To get your Todoist API token:
1. Go to https://todoist.com/app/settings/integrations/developer
2. Create a new app or use an existing one
3. Copy the API token

## Usage

### As a Standalone Server

After installation, you can run the MCP server in several ways:

```bash
# Using the installed console script (recommended)
todoist-mcp

# Or using python module syntax
python -m todoist_mcp.cli

# Or directly with python
python todoist_mcp/cli.py
```

### With Claude Desktop

Add this to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "todoist": {
      "command": "todoist-mcp",
      "env": {
        "TODOIST_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Available Tools

### Task Operations
- `get_tasks` - List tasks with optional filtering
- `get_task` - Get details of a specific task
- `create_task` - Create a new task
- `update_task` - Update an existing task
- `complete_task` - Mark a task as completed
- `reopen_task` - Reopen a completed task
- `delete_task` - Delete a task

### Project Operations
- `get_projects` - List all projects
- `get_project` - Get details of a specific project  
- `create_project` - Create a new project

### Section Operations
- `get_sections` - List sections within projects

## Example Interactions

Once connected, you can interact with Claude using natural language:

- "Show me all my tasks for today"
- "Create a task to review the quarterly report due tomorrow"
- "Mark task ID 12345 as completed"
- "List all my projects"
- "Create a new project called 'Home Renovation'"

## Development

### Project Structure

```
todoist-mcp/
├── todoist_mcp/
│   ├── __init__.py
│   ├── client.py      # Todoist API client
│   └── server.py      # MCP server implementation
├── pyproject.toml
├── README.md
└── .env.example
```

### Running Tests

(Tests would be added here in the future)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

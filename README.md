# Todoist MCP Server

A Model Context Protocol (MCP) server that integrates with Todoist, allowing Claude and other MCP-compatible AI assistants to interact with your Todoist tasks and projects.

<a href="https://glama.ai/mcp/servers/@dan-bailey/todoist-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@dan-bailey/todoist-mcp/badge" alt="Todoist Server MCP server" />
</a>

## Features

- **Task Management**: Create, read, update, complete, and delete tasks
- **Project Management**: List and manage projects
- **Filtering**: Filter tasks by project, section, labels, or natural language queries
- **Full API Support**: Comprehensive coverage of Todoist's REST API v2

## Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package installer)
- A Todoist account and API token

### Step 1: Get Your Todoist API Token

1. Go to [Todoist Integrations Settings](https://todoist.com/app/settings/integrations/developer)
2. Scroll down to the "API token" section
3. Copy your API token (you'll need this later)

### Step 2: Install the MCP Server

1. Clone the repository:
```bash
git clone <repository-url>
cd todoist-mcp
```

2. Install the package:
```bash
pip install -e .
```

**Note:** If you want to install it in a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

3. Create a `.env` file with your API token:
```bash
# Create .env file in the todoist-mcp directory
echo "TODOIST_API_TOKEN=your_api_token_here" > .env
```

Replace `your_api_token_here` with the token you copied in Step 1.

### Step 3: Configure Claude Desktop

The Claude Desktop configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Option A: Using Virtual Environment (Recommended for Development)

If you installed in a virtual environment, use the full path to the `todoist-mcp` command:

```json
{
  "mcpServers": {
    "todoist": {
      "command": "/full/path/to/venv/bin/todoist-mcp"
    }
  }
}
```

To find the full path, run:
```bash
which todoist-mcp  # On macOS/Linux
where todoist-mcp  # On Windows
```

#### Option B: Global Installation

If you installed globally (without a virtual environment), you can use:

```json
{
  "mcpServers": {
    "todoist": {
      "command": "todoist-mcp"
    }
  }
}
```

**Important Notes:**
- The MCP server will automatically load the `TODOIST_API_TOKEN` from the `.env` file in the `todoist-mcp` directory
- You do NOT need to specify the token in the Claude Desktop config if you're using a `.env` file
- After updating the config, **fully restart Claude Desktop** (quit the app completely, don't just close the window)

### Step 4: Verify Installation

1. **Restart Claude Desktop completely** (use Quit from the menu)
2. Open Claude Desktop
3. Look for the MCP server indicator (usually in the bottom corner or settings)
4. You should see "todoist" listed as an available MCP server
5. Try asking Claude: "Show me my Todoist tasks"

### Troubleshooting

**"Could not connect to MCP server" or "spawn todoist-mcp ENOENT"**
- Make sure you used the full path to `todoist-mcp` if using a virtual environment
- Verify the command exists by running `which todoist-mcp` (macOS/Linux) or `where todoist-mcp` (Windows)
- Check that your `.env` file exists in the `todoist-mcp` directory with the correct token

**"TODOIST_API_TOKEN environment variable not set"**
- Ensure your `.env` file is in the `todoist-mcp` directory (same directory as `pyproject.toml`)
- Verify the `.env` file contains: `TODOIST_API_TOKEN=your_actual_token`
- Check for typos in the variable name

**Server keeps disconnecting**
- Verify your API token is valid at https://todoist.com/app/settings/integrations/developer
- Check that you've fully restarted Claude Desktop
- Look at Claude Desktop logs for specific error messages

## Usage

### With Claude Desktop

Once configured, you can interact with Claude using natural language:

- "Show me all my tasks for today"
- "Create a task to review the quarterly report due tomorrow"
- "Mark task ID 12345 as completed"
- "List all my projects"
- "Create a new project called 'Home Renovation'"
- "Show me all high-priority tasks"

### As a Standalone Server (Advanced)

You can also run the MCP server directly for testing or integration with other MCP clients:

```bash
# Make sure your .env file is configured first
todoist-mcp
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
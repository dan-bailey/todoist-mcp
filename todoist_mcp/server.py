"""MCP server for Todoist integration."""

import os
import logging
from typing import Any, Sequence
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.models import Tool
from mcp.types import (
    CallToolResult,
    EmptyResult,
    ListToolsResult,
    TextContent,
)
import mcp.types as types

from .client import TodoistClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("todoist-mcp")

class TodoistMCPServer:
    """MCP server for Todoist integration."""
    
    def __init__(self):
        self.server = Server("todoist-mcp")
        self.todoist_client = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up the MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available tools."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="get_tasks",
                        description="Get tasks from Todoist with optional filtering",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "project_id": {
                                    "type": "string",
                                    "description": "Filter tasks by project ID"
                                },
                                "section_id": {
                                    "type": "string", 
                                    "description": "Filter tasks by section ID"
                                },
                                "label": {
                                    "type": "string",
                                    "description": "Filter tasks by label"
                                },
                                "filter_query": {
                                    "type": "string",
                                    "description": "Natural language filter (e.g., 'today', 'overdue', 'p1')"
                                }
                            },
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="get_task",
                        description="Get a specific task by ID",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "string",
                                    "description": "The ID of the task to retrieve"
                                }
                            },
                            "required": ["task_id"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="create_task",
                        description="Create a new task in Todoist",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "The task content/title"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Detailed description of the task"
                                },
                                "project_id": {
                                    "type": "string",
                                    "description": "Project ID to add the task to"
                                },
                                "section_id": {
                                    "type": "string",
                                    "description": "Section ID within the project"
                                },
                                "parent_id": {
                                    "type": "string",
                                    "description": "Parent task ID (for subtasks)"
                                },
                                "labels": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of label names"
                                },
                                "priority": {
                                    "type": "integer",
                                    "description": "Priority from 1 (normal) to 4 (urgent)",
                                    "minimum": 1,
                                    "maximum": 4
                                },
                                "due_string": {
                                    "type": "string",
                                    "description": "Human readable due date (e.g., 'tomorrow', 'next Monday')"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "ISO 8601 formatted due date"
                                }
                            },
                            "required": ["content"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="update_task",
                        description="Update an existing task",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "string",
                                    "description": "The ID of the task to update"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Updated task content/title"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Updated task description"
                                },
                                "labels": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Updated list of label names"
                                },
                                "priority": {
                                    "type": "integer",
                                    "description": "Updated priority from 1 (normal) to 4 (urgent)",
                                    "minimum": 1,
                                    "maximum": 4
                                },
                                "due_string": {
                                    "type": "string",
                                    "description": "Updated human readable due date"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Updated ISO 8601 formatted due date"
                                }
                            },
                            "required": ["task_id"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="complete_task",
                        description="Mark a task as completed",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "string",
                                    "description": "The ID of the task to complete"
                                }
                            },
                            "required": ["task_id"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="reopen_task",
                        description="Reopen a completed task",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "string",
                                    "description": "The ID of the task to reopen"
                                }
                            },
                            "required": ["task_id"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="delete_task",
                        description="Delete a task",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "string",
                                    "description": "The ID of the task to delete"
                                }
                            },
                            "required": ["task_id"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="get_projects",
                        description="Get all projects from Todoist",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="get_project",
                        description="Get a specific project by ID",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "project_id": {
                                    "type": "string",
                                    "description": "The ID of the project to retrieve"
                                }
                            },
                            "required": ["project_id"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="create_project",
                        description="Create a new project in Todoist",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the project"
                                },
                                "parent_id": {
                                    "type": "string",
                                    "description": "Parent project ID (for nested projects)"
                                },
                                "color": {
                                    "type": "string",
                                    "description": "Project color"
                                },
                                "is_favorite": {
                                    "type": "boolean",
                                    "description": "Whether to mark as favorite"
                                }
                            },
                            "required": ["name"],
                            "additionalProperties": False
                        }
                    ),
                    Tool(
                        name="get_sections",
                        description="Get sections from a project",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "project_id": {
                                    "type": "string",
                                    "description": "Project ID to get sections from (optional)"
                                }
                            },
                            "additionalProperties": False
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
            """Handle tool calls."""
            if not self.todoist_client:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Error: Todoist API token not configured. Please set the TODOIST_API_TOKEN environment variable."
                    )],
                    isError=True
                )
            
            try:
                if name == "get_tasks":
                    tasks = await self.todoist_client.get_tasks(**arguments)
                    task_list = "\n".join([
                        f"• [{task.id}] {task.content}" + 
                        (f" (Due: {task.due_string or task.due_date})" if task.due_string or task.due_date else "") +
                        (f" [Priority: {task.priority}]" if task.priority > 1 else "") +
                        (f" Labels: {', '.join(task.labels)}" if task.labels else "")
                        for task in tasks
                    ])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Found {len(tasks)} tasks:\n{task_list}" if tasks else "No tasks found."
                        )]
                    )
                
                elif name == "get_task":
                    task = await self.todoist_client.get_task(arguments["task_id"])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Task: {task.content}\n" +
                                 f"ID: {task.id}\n" +
                                 f"Description: {task.description}\n" +
                                 f"Completed: {task.is_completed}\n" +
                                 f"Priority: {task.priority}\n" +
                                 f"Labels: {', '.join(task.labels) if task.labels else 'None'}\n" +
                                 f"Due: {task.due_string or task.due_date or 'None'}\n" +
                                 f"Project ID: {task.project_id}\n" +
                                 f"URL: {task.url}"
                        )]
                    )
                
                elif name == "create_task":
                    task = await self.todoist_client.create_task(**arguments)
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Task created successfully!\n" +
                                 f"ID: {task.id}\n" +
                                 f"Title: {task.content}\n" +
                                 f"URL: {task.url}"
                        )]
                    )
                
                elif name == "update_task":
                    task_id = arguments.pop("task_id")
                    task = await self.todoist_client.update_task(task_id, **arguments)
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Task updated successfully!\n" +
                                 f"ID: {task.id}\n" +
                                 f"Title: {task.content}\n" +
                                 f"URL: {task.url}"
                        )]
                    )
                
                elif name == "complete_task":
                    await self.todoist_client.complete_task(arguments["task_id"])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Task {arguments['task_id']} completed successfully!"
                        )]
                    )
                
                elif name == "reopen_task":
                    await self.todoist_client.reopen_task(arguments["task_id"])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Task {arguments['task_id']} reopened successfully!"
                        )]
                    )
                
                elif name == "delete_task":
                    await self.todoist_client.delete_task(arguments["task_id"])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Task {arguments['task_id']} deleted successfully!"
                        )]
                    )
                
                elif name == "get_projects":
                    projects = await self.todoist_client.get_projects()
                    project_list = "\n".join([
                        f"• [{project.id}] {project.name}" +
                        (f" (Shared)" if project.is_shared else "") +
                        (f" ⭐" if project.is_favorite else "")
                        for project in projects
                    ])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Found {len(projects)} projects:\n{project_list}" if projects else "No projects found."
                        )]
                    )
                
                elif name == "get_project":
                    project = await self.todoist_client.get_project(arguments["project_id"])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Project: {project.name}\n" +
                                 f"ID: {project.id}\n" +
                                 f"Color: {project.color}\n" +
                                 f"Shared: {project.is_shared}\n" +
                                 f"Favorite: {project.is_favorite}\n" +
                                 f"View Style: {project.view_style}\n" +
                                 f"URL: {project.url}"
                        )]
                    )
                
                elif name == "create_project":
                    project = await self.todoist_client.create_project(**arguments)
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Project created successfully!\n" +
                                 f"ID: {project.id}\n" +
                                 f"Name: {project.name}\n" +
                                 f"URL: {project.url}"
                        )]
                    )
                
                elif name == "get_sections":
                    sections = await self.todoist_client.get_sections(**arguments)
                    section_list = "\n".join([
                        f"• [{section.id}] {section.name} (Project: {section.project_id})"
                        for section in sections
                    ])
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Found {len(sections)} sections:\n{section_list}" if sections else "No sections found."
                        )]
                    )
                
                else:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Unknown tool: {name}"
                        )],
                        isError=True
                    )
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Error: {str(e)}"
                    )],
                    isError=True
                )
    
    async def initialize(self):
        """Initialize the Todoist client."""
        api_token = os.getenv("TODOIST_API_TOKEN")
        if api_token:
            self.todoist_client = TodoistClient(api_token)
            logger.info("Todoist MCP server initialized successfully")
        else:
            logger.warning("TODOIST_API_TOKEN environment variable not set")
    
    async def serve_stdio(self):
        """Run the server using stdin/stdout transport."""
        from mcp.server.stdio import stdio_server
        
        await self.initialize()
        
        async with stdio_server(self.server) as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="todoist-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


async def main():
    """Main entry point."""
    server = TodoistMCPServer()
    await server.serve_stdio()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
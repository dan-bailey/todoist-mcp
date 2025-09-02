"""MCP server for Todoist integration."""

import os
import logging
from typing import Any, List, Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from .client import TodoistClient, TodoistTask, TodoistProject, TodoistSection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("todoist-mcp")

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Todoist")

# Initialize Todoist client
api_token = os.getenv("TODOIST_API_TOKEN")
if not api_token:
    logger.warning("TODOIST_API_TOKEN environment variable not set")
    todoist_client = None
else:
    todoist_client = TodoistClient(api_token)
    logger.info("Todoist MCP server initialized successfully")


def _check_client():
    """Check if Todoist client is available."""
    if not todoist_client:
        raise ValueError("Todoist API token not configured. Please set the TODOIST_API_TOKEN environment variable.")


@mcp.tool()
async def get_tasks(
    project_id: Optional[str] = None,
    section_id: Optional[str] = None, 
    label: Optional[str] = None,
    filter_query: Optional[str] = None
) -> str:
    """Get tasks from Todoist with optional filtering.
    
    Args:
        project_id: Filter tasks by project ID
        section_id: Filter tasks by section ID
        label: Filter tasks by label
        filter_query: Natural language filter (e.g., 'today', 'overdue', 'p1')
    """
    _check_client()
    
    tasks = await todoist_client.get_tasks(
        project_id=project_id,
        section_id=section_id,
        label=label,
        filter_query=filter_query
    )
    
    if not tasks:
        return "No tasks found."
    
    task_list = []
    for task in tasks:
        task_info = f"• [{task.id}] {task.content}"
        if task.due_string or task.due_date:
            task_info += f" (Due: {task.due_string or task.due_date})"
        if task.priority > 1:
            task_info += f" [Priority: {task.priority}]"
        if task.labels:
            task_info += f" Labels: {', '.join(task.labels)}"
        task_list.append(task_info)
    
    return f"Found {len(tasks)} tasks:\n" + "\n".join(task_list)


@mcp.tool()
async def get_task(task_id: str) -> str:
    """Get a specific task by ID.
    
    Args:
        task_id: The ID of the task to retrieve
    """
    _check_client()
    
    task = await todoist_client.get_task(task_id)
    
    return (
        f"Task: {task.content}\n"
        f"ID: {task.id}\n"
        f"Description: {task.description}\n"
        f"Completed: {task.is_completed}\n"
        f"Priority: {task.priority}\n"
        f"Labels: {', '.join(task.labels) if task.labels else 'None'}\n"
        f"Due: {task.due_string or task.due_date or 'None'}\n"
        f"Project ID: {task.project_id}\n"
        f"URL: {task.url}"
    )


@mcp.tool()
async def create_task(
    content: str,
    description: str = "",
    project_id: Optional[str] = None,
    section_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    labels: Optional[List[str]] = None,
    priority: int = 1,
    due_string: Optional[str] = None,
    due_date: Optional[str] = None
) -> str:
    """Create a new task in Todoist.
    
    Args:
        content: The task content/title
        description: Detailed description of the task
        project_id: Project ID to add the task to
        section_id: Section ID within the project
        parent_id: Parent task ID (for subtasks)
        labels: List of label names
        priority: Priority from 1 (normal) to 4 (urgent)
        due_string: Human readable due date (e.g., 'tomorrow', 'next Monday')
        due_date: ISO 8601 formatted due date
    """
    _check_client()
    
    task = await todoist_client.create_task(
        content=content,
        description=description,
        project_id=project_id,
        section_id=section_id,
        parent_id=parent_id,
        labels=labels or [],
        priority=priority,
        due_string=due_string,
        due_date=due_date
    )
    
    return (
        f"Task created successfully!\n"
        f"ID: {task.id}\n"
        f"Title: {task.content}\n"
        f"URL: {task.url}"
    )


@mcp.tool()
async def update_task(
    task_id: str,
    content: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[List[str]] = None,
    priority: Optional[int] = None,
    due_string: Optional[str] = None,
    due_date: Optional[str] = None
) -> str:
    """Update an existing task.
    
    Args:
        task_id: The ID of the task to update
        content: Updated task content/title
        description: Updated task description
        labels: Updated list of label names
        priority: Updated priority from 1 (normal) to 4 (urgent)
        due_string: Updated human readable due date
        due_date: Updated ISO 8601 formatted due date
    """
    _check_client()
    
    updates = {}
    if content is not None:
        updates["content"] = content
    if description is not None:
        updates["description"] = description
    if labels is not None:
        updates["labels"] = labels
    if priority is not None:
        updates["priority"] = priority
    if due_string is not None:
        updates["due_string"] = due_string
    if due_date is not None:
        updates["due_date"] = due_date
    
    task = await todoist_client.update_task(task_id, **updates)
    
    return (
        f"Task updated successfully!\n"
        f"ID: {task.id}\n"
        f"Title: {task.content}\n"
        f"URL: {task.url}"
    )


@mcp.tool()
async def complete_task(task_id: str) -> str:
    """Mark a task as completed.
    
    Args:
        task_id: The ID of the task to complete
    """
    _check_client()
    
    await todoist_client.complete_task(task_id)
    return f"Task {task_id} completed successfully!"


@mcp.tool()
async def reopen_task(task_id: str) -> str:
    """Reopen a completed task.
    
    Args:
        task_id: The ID of the task to reopen
    """
    _check_client()
    
    await todoist_client.reopen_task(task_id)
    return f"Task {task_id} reopened successfully!"


@mcp.tool()
async def delete_task(task_id: str) -> str:
    """Delete a task.
    
    Args:
        task_id: The ID of the task to delete
    """
    _check_client()
    
    await todoist_client.delete_task(task_id)
    return f"Task {task_id} deleted successfully!"


@mcp.tool()
async def get_projects() -> str:
    """Get all projects from Todoist."""
    _check_client()
    
    projects = await todoist_client.get_projects()
    
    if not projects:
        return "No projects found."
    
    project_list = []
    for project in projects:
        project_info = f"• [{project.id}] {project.name}"
        if project.is_shared:
            project_info += " (Shared)"
        if project.is_favorite:
            project_info += " ⭐"
        project_list.append(project_info)
    
    return f"Found {len(projects)} projects:\n" + "\n".join(project_list)


@mcp.tool()
async def get_project(project_id: str) -> str:
    """Get a specific project by ID.
    
    Args:
        project_id: The ID of the project to retrieve
    """
    _check_client()
    
    project = await todoist_client.get_project(project_id)
    
    return (
        f"Project: {project.name}\n"
        f"ID: {project.id}\n"
        f"Color: {project.color}\n"
        f"Shared: {project.is_shared}\n"
        f"Favorite: {project.is_favorite}\n"
        f"View Style: {project.view_style}\n"
        f"URL: {project.url}"
    )


@mcp.tool()
async def create_project(
    name: str,
    parent_id: Optional[str] = None,
    color: Optional[str] = None,
    is_favorite: bool = False
) -> str:
    """Create a new project in Todoist.
    
    Args:
        name: The name of the project
        parent_id: Parent project ID (for nested projects)
        color: Project color
        is_favorite: Whether to mark as favorite
    """
    _check_client()
    
    kwargs = {"name": name}
    if parent_id:
        kwargs["parent_id"] = parent_id
    if color:
        kwargs["color"] = color
    if is_favorite:
        kwargs["is_favorite"] = is_favorite
        
    project = await todoist_client.create_project(**kwargs)
    
    return (
        f"Project created successfully!\n"
        f"ID: {project.id}\n"
        f"Name: {project.name}\n"
        f"URL: {project.url}"
    )


@mcp.tool()
async def get_sections(project_id: Optional[str] = None) -> str:
    """Get sections from a project.
    
    Args:
        project_id: Project ID to get sections from (optional)
    """
    _check_client()
    
    sections = await todoist_client.get_sections(project_id=project_id)
    
    if not sections:
        return "No sections found."
    
    section_list = []
    for section in sections:
        section_list.append(f"• [{section.id}] {section.name} (Project: {section.project_id})")
    
    return f"Found {len(sections)} sections:\n" + "\n".join(section_list)


# Main function for running the server
async def main():
    """Main entry point for running the MCP server."""
    await mcp.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
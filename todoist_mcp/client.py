"""Todoist API client wrapper."""

import asyncio
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel


class TodoistTask(BaseModel):
    """Represents a Todoist task."""
    id: str
    content: str
    description: str = ""
    is_completed: bool = False
    labels: List[str] = []
    priority: int = 1
    due_string: Optional[str] = None
    due_date: Optional[str] = None
    project_id: str = ""
    section_id: Optional[str] = None
    parent_id: Optional[str] = None
    order: int = 0
    url: str = ""
    created_at: str = ""


class TodoistProject(BaseModel):
    """Represents a Todoist project."""
    id: str
    name: str
    comment_count: int = 0
    order: int = 0
    color: str = "grey"
    is_shared: bool = False
    is_favorite: bool = False
    is_inbox_project: bool = False
    is_team_inbox: bool = False
    view_style: str = "list"
    url: str = ""
    parent_id: Optional[str] = None


class TodoistSection(BaseModel):
    """Represents a Todoist section."""
    id: str
    project_id: str
    order: int
    name: str


class TodoistClient:
    """Async client for Todoist REST API."""
    
    BASE_URL = "https://api.todoist.com/rest/v2"
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make an HTTP request to the Todoist API."""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self.BASE_URL}{endpoint}",
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            if response.status_code == 204:  # No content
                return None
            return response.json()
    
    async def get_tasks(self, 
                       project_id: Optional[str] = None,
                       section_id: Optional[str] = None,
                       label: Optional[str] = None,
                       filter_query: Optional[str] = None) -> List[TodoistTask]:
        """Get tasks with optional filtering."""
        params = {}
        if project_id:
            params["project_id"] = project_id
        if section_id:
            params["section_id"] = section_id
        if label:
            params["label"] = label
        if filter_query:
            params["filter"] = filter_query
        
        data = await self._request("GET", "/tasks", params=params)
        return [TodoistTask(**task) for task in data]
    
    async def get_task(self, task_id: str) -> TodoistTask:
        """Get a specific task by ID."""
        data = await self._request("GET", f"/tasks/{task_id}")
        return TodoistTask(**data)
    
    async def create_task(self, 
                         content: str,
                         description: str = "",
                         project_id: Optional[str] = None,
                         section_id: Optional[str] = None,
                         parent_id: Optional[str] = None,
                         order: Optional[int] = None,
                         labels: Optional[List[str]] = None,
                         priority: int = 1,
                         due_string: Optional[str] = None,
                         due_date: Optional[str] = None) -> TodoistTask:
        """Create a new task."""
        payload = {
            "content": content,
            "description": description,
            "priority": priority
        }
        
        if project_id:
            payload["project_id"] = project_id
        if section_id:
            payload["section_id"] = section_id
        if parent_id:
            payload["parent_id"] = parent_id
        if order is not None:
            payload["order"] = order
        if labels:
            payload["labels"] = labels
        if due_string:
            payload["due_string"] = due_string
        if due_date:
            payload["due_date"] = due_date
        
        data = await self._request("POST", "/tasks", json=payload)
        return TodoistTask(**data)
    
    async def update_task(self, task_id: str, **updates) -> TodoistTask:
        """Update an existing task."""
        data = await self._request("POST", f"/tasks/{task_id}", json=updates)
        return TodoistTask(**data)
    
    async def complete_task(self, task_id: str) -> None:
        """Mark a task as completed."""
        await self._request("POST", f"/tasks/{task_id}/close")
    
    async def reopen_task(self, task_id: str) -> None:
        """Reopen a completed task."""
        await self._request("POST", f"/tasks/{task_id}/reopen")
    
    async def delete_task(self, task_id: str) -> None:
        """Delete a task."""
        await self._request("DELETE", f"/tasks/{task_id}")
    
    async def get_projects(self) -> List[TodoistProject]:
        """Get all projects."""
        data = await self._request("GET", "/projects")
        return [TodoistProject(**project) for project in data]
    
    async def get_project(self, project_id: str) -> TodoistProject:
        """Get a specific project by ID."""
        data = await self._request("GET", f"/projects/{project_id}")
        return TodoistProject(**data)
    
    async def create_project(self, name: str, **kwargs) -> TodoistProject:
        """Create a new project."""
        payload = {"name": name, **kwargs}
        data = await self._request("POST", "/projects", json=payload)
        return TodoistProject(**data)
    
    async def update_project(self, project_id: str, **updates) -> TodoistProject:
        """Update an existing project."""
        data = await self._request("POST", f"/projects/{project_id}", json=updates)
        return TodoistProject(**data)
    
    async def delete_project(self, project_id: str) -> None:
        """Delete a project."""
        await self._request("DELETE", f"/projects/{project_id}")
    
    async def get_sections(self, project_id: Optional[str] = None) -> List[TodoistSection]:
        """Get sections, optionally filtered by project."""
        params = {}
        if project_id:
            params["project_id"] = project_id
        
        data = await self._request("GET", "/sections", params=params)
        return [TodoistSection(**section) for section in data]
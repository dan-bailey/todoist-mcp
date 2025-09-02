#!/usr/bin/env python3
"""Command-line entry point for the Todoist MCP server."""

import os
from dotenv import load_dotenv

def cli():
    """Main CLI entry point."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Check if API token is configured
    if not os.getenv("TODOIST_API_TOKEN"):
        print("Error: TODOIST_API_TOKEN environment variable not set.")
        print("Please set your Todoist API token:")
        print("  export TODOIST_API_TOKEN=your_token_here")
        print("Or create a .env file with:")
        print("  TODOIST_API_TOKEN=your_token_here")
        return 1
    
    # Import and run the server - FastMCP's run() is synchronous
    from .server import mcp
    try:
        # FastMCP's run() method is synchronous and handles its own event loop
        mcp.run()
        return 0
    except KeyboardInterrupt:
        print("\nShutting down...")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(cli())
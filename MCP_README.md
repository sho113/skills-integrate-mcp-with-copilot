# Mergington High School MCP Server

This is a Model Context Protocol (MCP) server that provides tools for managing extracurricular activities at Mergington High School.

## Features

The MCP server provides the following tools:

1. **list_activities** - Get a list of all available extracurricular activities
2. **get_activity** - Get detailed information about a specific activity
3. **signup_activity** - Sign up a student for an activity
4. **get_student_activities** - Get all activities a student is signed up for

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the MCP Server

To run the MCP server:

```bash
python3 src/mcp_server.py
```

## Integration with VS Code

The MCP server can be integrated with GitHub Copilot in VS Code. The configuration is stored in `.vscode/mcp-settings.json`.

To use the MCP server with Copilot:

1. Ensure the MCP server configuration is loaded in VS Code
2. The server will automatically start when Copilot needs to access school activity data
3. You can interact with the server through Copilot Chat using natural language

## Available Activities

- **Chess Club** - Learn strategies and compete in chess tournaments
- **Programming Class** - Learn programming fundamentals and build software projects
- **Gym Class** - Physical education and sports activities
- **Soccer Team** - Join the school soccer team and compete in matches
- **Basketball Team** - Practice and play basketball with the school team

## Example Usage

### List all activities
Ask Copilot: "Show me all available activities at Mergington High School"

### Sign up for an activity
Ask Copilot: "Sign up jane@mergington.edu for the Chess Club"

### Check student activities
Ask Copilot: "What activities is emma@mergington.edu signed up for?"

## Architecture

The system consists of two components:

1. **FastAPI Web Application** (`app.py`) - Provides a REST API and web interface
2. **MCP Server** (`mcp_server.py`) - Provides tools for GitHub Copilot integration

Both components share the same in-memory activity database structure.

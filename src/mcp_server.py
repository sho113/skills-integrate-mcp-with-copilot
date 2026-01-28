"""
Mergington High School MCP Server

A Model Context Protocol server that provides tools for accessing
and managing extracurricular activities at Mergington High School.
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# In-memory activity database (shared with FastAPI)
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    }
}

# Create the MCP server
app = Server("mergington-high-school")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for managing school activities."""
    return [
        Tool(
            name="list_activities",
            description="Get a list of all available extracurricular activities at Mergington High School",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_activity",
            description="Get detailed information about a specific activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "The name of the activity (e.g., 'Chess Club', 'Programming Class')"
                    }
                },
                "required": ["activity_name"]
            }
        ),
        Tool(
            name="signup_activity",
            description="Sign up a student for an extracurricular activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "The name of the activity to sign up for"
                    },
                    "student_email": {
                        "type": "string",
                        "description": "The student's email address (must end with @mergington.edu)"
                    }
                },
                "required": ["activity_name", "student_email"]
            }
        ),
        Tool(
            name="get_student_activities",
            description="Get all activities a student is signed up for",
            inputSchema={
                "type": "object",
                "properties": {
                    "student_email": {
                        "type": "string",
                        "description": "The student's email address"
                    }
                },
                "required": ["student_email"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for managing school activities."""
    
    if name == "list_activities":
        # Return list of all activities with basic info
        activity_list = []
        for activity_name, details in activities.items():
            activity_list.append({
                "name": activity_name,
                "description": details["description"],
                "schedule": details["schedule"],
                "available_spots": details["max_participants"] - len(details["participants"])
            })
        
        return [TextContent(
            type="text",
            text=json.dumps(activity_list, indent=2)
        )]
    
    elif name == "get_activity":
        activity_name = arguments.get("activity_name")
        
        if activity_name not in activities:
            return [TextContent(
                type="text",
                text=f"Error: Activity '{activity_name}' not found. Available activities: {', '.join(activities.keys())}"
            )]
        
        activity = activities[activity_name]
        result = {
            "name": activity_name,
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "current_participants": len(activity["participants"]),
            "available_spots": activity["max_participants"] - len(activity["participants"]),
            "participants": activity["participants"]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "signup_activity":
        activity_name = arguments.get("activity_name")
        student_email = arguments.get("student_email")
        
        # Validate email
        if not student_email.endswith("@mergington.edu"):
            return [TextContent(
                type="text",
                text="Error: Student email must be a Mergington High School email (@mergington.edu)"
            )]
        
        # Check if activity exists
        if activity_name not in activities:
            return [TextContent(
                type="text",
                text=f"Error: Activity '{activity_name}' not found. Available activities: {', '.join(activities.keys())}"
            )]
        
        activity = activities[activity_name]
        
        # Check if student is already signed up
        if student_email in activity["participants"]:
            return [TextContent(
                type="text",
                text=f"Student {student_email} is already signed up for {activity_name}"
            )]
        
        # Check if activity is full
        if len(activity["participants"]) >= activity["max_participants"]:
            return [TextContent(
                type="text",
                text=f"Error: {activity_name} is full. Maximum participants: {activity['max_participants']}"
            )]
        
        # Sign up the student
        activity["participants"].append(student_email)
        
        return [TextContent(
            type="text",
            text=f"Success! {student_email} has been signed up for {activity_name}. Current participants: {len(activity['participants'])}/{activity['max_participants']}"
        )]
    
    elif name == "get_student_activities":
        student_email = arguments.get("student_email")
        
        # Find all activities the student is signed up for
        student_activities = []
        for activity_name, details in activities.items():
            if student_email in details["participants"]:
                student_activities.append({
                    "name": activity_name,
                    "description": details["description"],
                    "schedule": details["schedule"]
                })
        
        if not student_activities:
            return [TextContent(
                type="text",
                text=f"Student {student_email} is not signed up for any activities"
            )]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "student": student_email,
                "activities": student_activities,
                "total_activities": len(student_activities)
            }, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())

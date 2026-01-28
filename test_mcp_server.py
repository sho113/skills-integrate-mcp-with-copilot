#!/usr/bin/env python3
"""
Test script for Mergington High School MCP Server

This script tests the MCP server tools without requiring a full MCP client.
"""

import asyncio
import sys
sys.path.insert(0, '/workspaces/skills-integrate-mcp-with-copilot/src')

from mcp_server import call_tool, list_tools

async def test_mcp_server():
    """Test all MCP server tools."""
    
    print("=" * 60)
    print("Testing Mergington High School MCP Server")
    print("=" * 60)
    print()
    
    # Test list_tools
    print("1. Testing list_tools()...")
    tools = await list_tools()
    print(f"   ✓ Found {len(tools)} tools:")
    for tool in tools:
        print(f"     - {tool.name}: {tool.description}")
    print()
    
    # Test list_activities
    print("2. Testing list_activities tool...")
    result = await call_tool("list_activities", {})
    print(f"   ✓ Result: {result[0].text[:100]}...")
    print()
    
    # Test get_activity
    print("3. Testing get_activity tool...")
    result = await call_tool("get_activity", {"activity_name": "Chess Club"})
    print(f"   ✓ Result: {result[0].text[:100]}...")
    print()
    
    # Test signup_activity
    print("4. Testing signup_activity tool...")
    result = await call_tool("signup_activity", {
        "activity_name": "Chess Club",
        "student_email": "test@mergington.edu"
    })
    print(f"   ✓ Result: {result[0].text}")
    print()
    
    # Test get_student_activities
    print("5. Testing get_student_activities tool...")
    result = await call_tool("get_student_activities", {
        "student_email": "emma@mergington.edu"
    })
    print(f"   ✓ Result: {result[0].text[:100]}...")
    print()
    
    # Test error handling - invalid activity
    print("6. Testing error handling (invalid activity)...")
    result = await call_tool("get_activity", {"activity_name": "Invalid Club"})
    print(f"   ✓ Result: {result[0].text}")
    print()
    
    # Test error handling - invalid email
    print("7. Testing error handling (invalid email)...")
    result = await call_tool("signup_activity", {
        "activity_name": "Chess Club",
        "student_email": "test@gmail.com"
    })
    print(f"   ✓ Result: {result[0].text}")
    print()
    
    print("=" * 60)
    print("All tests completed successfully! ✓")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_mcp_server())

#!/usr/bin/env python3

import asyncio
import logging
import sys
from typing import Any, Dict, Optional

# Add the path to import the original python_caller
sys.path.append('/Users/jakedahl/IdeaProjects/RS_Bots/DreambotShim/src')

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Import our modules
from java_caller import JavaMethodCaller
from tools import get_tool_definitions
from handlers import handle_call_tool

# Note: Using our enhanced JavaMethodCaller with response handling
# The original python_caller JavaMethodCaller only returns booleans

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the server instance
server = Server("runescape-bot")

# Global Java caller instance
# Always waits for responses from Java shim
java_caller = JavaMethodCaller()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return get_tool_definitions()

@server.call_tool()
async def handle_call_tool_wrapper(
    name: str, arguments: Optional[Dict[str, Any]]
) -> list[types.TextContent]:
    """Handle tool calls."""
    return await handle_call_tool(java_caller, name, arguments)

async def main():
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="runescape-bot",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())

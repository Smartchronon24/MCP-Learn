# =============================================================================
# client.py — A Simple Python Client to Test your MCP Server
# =============================================================================
#
# WHY DO WE NEED THIS?
# --------------------
# Normally, an AI like Claude Desktop acts as the "Client". But since we want 
# to test our server without any external tools or Node.js, we wrote this 
# small Python script to "pretend" to be an AI client.
#
# HOW IT WORKS:
# 1. It launches 'server.py' as a background process.
# 2. It connects to it using a "pipe" (Standard Input/Output).
# 3. It sends a message asking to run the 'hello_world' tool.
# 4. It prints the answer.
# =============================================================================

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_test():
    """
    Main function to connect to the MCP server and invoke a tool.
    """
    # Define how to start the server. 
    # We use 'sys.executable' to ensure it uses the SAME python version/env we are currently in.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
        env=None
    )

    import os
    pid = os.getpid()

    print(f"\n--- MCP Test (PID: {pid}) ---")
    print("🚀 Connecting...")

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ Connected!")

                # List tools but only print the name to keep it clean
                print("🔍 Step 1: Discovering tools...")
                tools_result = await session.list_tools()
                for tool in tools_result.tools:
                    print(f"  - Tool Found: {tool.name}")

                # Call the tool
                print("🤖 Step 2: Calling 'hello_world'...")
                result = await session.call_tool("hello_world", arguments={})
                
                print(f"🎉 SUCCESS: {result.content[0].text}")

                # Call the tool
                print("🤖 Step 3: Calling 'add_numbers'...")
                result = await session.call_tool("add_numbers", arguments={"a": 10, "b": 20})
                
                print(f"🎉 SUCCESS: {result.content[0].number}")


    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    # Start the async loop
    asyncio.run(run_test())

import asyncio
import sys
import ollama
import traceback
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# CONFIGURATION
MODEL = "llama3.1" 

async def main():
    # --- PRE-CHECK: Is Ollama awake? ---
    print(f"🔎 Checking Ollama for model '{MODEL}'...")
    try:
        client = ollama.AsyncClient()
        # Just a tiny test to see if Ollama is there
        await client.list()
    except Exception:
        print("❌ ERROR: Cannot connect to Ollama. Is it running?")
        return

    # --- STEP 1: Ask the user FIRST (so we don't block the loop later) ---
    user_prompt = input("\n💬 What should I ask the AI? ")

    # --- STEP 2: Connect to MCP ---
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
    )

    print(f"🚀 Starting MCP Server...")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Fetch tools
                print("🔍 Discovering tools...")
                mcp_tools = await session.list_tools()
                
                ollama_tools = []
                for tool in mcp_tools.tools:
                    ollama_tools.append({
                        'type': 'function',
                        'function': {
                            'name': tool.name,
                            'description': tool.description,
                            'parameters': tool.inputSchema or {'type': 'object', 'properties': {}},
                        },
                    })

                # --- STEP 3: Talk to Ollama ---
                print(f"🧠 Asking Ollama (Thinking...)...")
                messages = [{'role': 'user', 'content': user_prompt}]
                
                response = await client.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )

                # --- STEP 4: Handle Tool Calls ---
                if response['message'].get('tool_calls'):
                    for call in response['message']['tool_calls']:
                        name = call['function']['name']
                        args = call['function']['arguments']
                        
                        print(f"🛠️  AI decided to call: {name}")
                        result = await session.call_tool(name, arguments=args)
                        
                        output = result.content[0].text
                        print(f"✅ Tool returned: {output}")

                        messages.append(response['message'])
                        messages.append({'role': 'tool', 'content': output})
                        
                        final = await client.chat(model=MODEL, messages=messages)
                        print(f"\n✨ AI Response: {final['message']['content']}")
                else:
                    print(f"\n✨ AI Response: {response['message']['content']}")

    except Exception as e:
        print("\n--- ❌ DETAILED ERROR ---")
        # This will show us the REAL error inside the TaskGroup
        traceback.print_exc()
        print("-------------------------")

if __name__ == "__main__":
    asyncio.run(main())

# =============================================================================
# server.py — Hello World MCP Server
# =============================================================================
#
# WHAT IS THIS FILE?
# ------------------
# This is the entry point for our MCP (Model Context Protocol) server.
# An MCP server is a small program that exposes "tools" to AI clients
# (like Claude Desktop, Cursor, or any MCP-compatible AI assistant).
#
# Think of it like a plugin system:
#   - You write the plugin (this server)
#   - An AI client loads the plugin and discovers what tools are available
#   - The user (or AI) calls a tool → your Python function runs → result is returned
#
# HOW DOES IT WORK AT A HIGH LEVEL?
# -----------------------------------
# 1. FastMCP creates an MCP-compliant server
# 2. You register Python functions as "tools" using the @mcp.tool() decorator
# 3. The server communicates with AI clients over STDIO (standard input/output)
# 4. Clients discover tools automatically — no manual wiring needed
#
# =============================================================================


# -----------------------------------------------------------------------------
# IMPORT: FastMCP
# -----------------------------------------------------------------------------
# FastMCP is the high-level, developer-friendly class from the official
# MCP Python SDK. It removes all the low-level boilerplate and lets you
# define tools as plain Python functions.
#
# The official MCP SDK package is installed via:
#   pip install "mcp[cli]"
#
# FastMCP lives inside the `mcp.server.fastmcp` submodule.
# -----------------------------------------------------------------------------
from mcp.server.fastmcp import FastMCP


# -----------------------------------------------------------------------------
# STEP 1: Create the MCP Server Instance
# -----------------------------------------------------------------------------
# FastMCP("ServerName") initializes your MCP server.
#
# The name "HelloWorldServer" is what AI clients see when they connect.
# It is metadata — it does NOT affect how tools are called.
#
# You can think of this like Flask's `app = Flask(__name__)` or
# FastAPI's `app = FastAPI()`.
# -----------------------------------------------------------------------------
mcp = FastMCP("HelloWorldServer")


# -----------------------------------------------------------------------------
# STEP 2: Define a Tool Using the @mcp.tool() Decorator
# -----------------------------------------------------------------------------
# A "tool" in MCP is any Python function that you want AI clients to be
# able to call. When an AI assistant (like Claude) is connected to this
# server, it can see this tool and invoke it on behalf of the user.
#
# HOW THE DECORATOR WORKS:
#   @mcp.tool()         ← This registers `hello_world` as an MCP tool
#   def hello_world()   ← This is a plain Python function
#
# FastMCP reads the function's:
#   - Name        → used as the tool's identifier ("hello_world")
#   - Docstring   → used as the tool's description (shown to AI clients)
#   - Parameters  → used to build the tool's input schema
#   - Return type → used to tell clients what kind of value to expect
#
# WHY THE RETURN TYPE ANNOTATION `-> str` MATTERS:
#   MCP is a typed protocol. The return type hint tells the client exactly
#   what data type to expect. This enables proper serialization and
#   validation. Always annotate your return types — it's good practice
#   and required for correct MCP behavior.
# -----------------------------------------------------------------------------
@mcp.tool()
def hello_world() -> str:
    """
    A simple tool that returns a greeting message.

    This is the tool's description. AI clients display this text to help
    users and the AI understand what the tool does.

    Returns:
        str: The classic "Hello World!" greeting string.
    """
    # This is the entire logic of our tool.
    # When an AI client calls `hello_world`, this function executes
    # and the return value is sent back to the client as the tool's result.
    return "Hello World!"

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b    

# -----------------------------------------------------------------------------
# STEP 3: Run the Server
# -----------------------------------------------------------------------------
# `mcp.run()` starts the MCP server and begins listening for connections.
#
# By default, FastMCP uses the STDIO transport — meaning it communicates
# over standard input (stdin) and standard output (stdout).
#
# WHAT IS STDIO TRANSPORT?
#   STDIO is how the AI client (e.g., Claude Desktop) launches your server
#   as a subprocess and communicates with it through the process's stdin/stdout
#   pipes. No ports, no HTTP — just process-level I/O.
#
# WHY `if __name__ == "__main__"`?
#   This is a Python best practice. It ensures `mcp.run()` is only called
#   when you run this file DIRECTLY (e.g., `python server.py`), NOT when
#   it is imported by another module. This keeps the code reusable and
#   import-safe.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()

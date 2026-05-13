# HelloWorld MCP Server 🚀

Welcome! This is a beginner-friendly project designed to teach you the fundamentals of the **Model Context Protocol (MCP)** using Python.

---

## 📖 What is MCP?

The **Model Context Protocol (MCP)** is an open standard that allows AI models (like Claude, ChatGPT, or Cursor) to securely interact with local tools and data. 

Instead of writing custom code for every AI model to talk to your computer, you build an **MCP Server**. Any AI client that supports MCP can then "discover" and use the tools your server provides.

### What this project does
This project creates a minimal MCP server named `HelloWorldServer` that exposes one simple tool called `hello_world`. When the AI calls this tool, the server returns the string: `"Hello World!"`.

---

## 🛠️ Getting Started

Follow these steps to set up and run your server.

### 1. Create a Virtual Environment
It is best practice to use a virtual environment to keep your dependencies organized.

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
This project uses the official MCP Python SDK.

```bash
pip install "mcp[cli]"
```

### 3. Run the Server
The server runs using **STDIO transport**. This means it communicates with the AI client through standard input and output (the terminal).

```bash
python server.py
```
*(Note: When running directly, you won't see much happen because it's waiting for an MCP client to send a command!)*

---

## 🔍 How to Test (Python Only)

Since this is a Python-only project, we have included a `client.py` script that acts as a test bench. It pretends to be an AI client (like Claude) and talks to your server.

### Steps to Test:

1.  Open your terminal in the `MCP/` folder.
2.  Run the following command:
    ```powershell
    # On Windows (direct path avoids activation issues)
    .\.venv\Scripts\python.exe client.py

    # On Mac/Linux
    python3 client.py
    ```

### Expected Output:
```text
--- MCP Python-Only Test ---
🚀 Connecting to HelloWorldServer...
✅ Connected!

🔍 Step 1: Discovering tools...
  - Found: hello_world | Description: A simple tool that returns a greeting message.

🤖 Step 2: Calling 'hello_world' tool...

🎉 SUCCESS! Server returned:
   >>> Hello World! <<<
```

---

## 🧠 Deep Dive: How it Works

### What is STDIO Transport?
STDIO (Standard Input/Output) is the "pipe" between your server and the client. When you run `client.py`, it launches `server.py` in the background. They talk by sending JSON messages back and forth through the terminal's hidden input/output streams.

### What happens internally?
1.  **Discovery:** The client asks the server "What tools do you have?". The server replies with a list containing `hello_world`.
2.  **Call:** The client sends a request: `call_tool("hello_world")`.
3.  **Execution:** Your Python function `@mcp.tool()` runs in `server.py`.
4.  **Response:** The function returns `"Hello World!"`, which is sent back to the client and printed on your screen.

---

## ⚠️ Common Beginner Mistakes & Fixes

*   **Error: `ModuleNotFoundError: No module named 'mcp'`**
    *   *Fix:* Make sure you ran `pip install "mcp[cli]"`.
*   **Server hangs or does nothing:**
    *   *Explanation:* If you run `python server.py` directly, it will just sit there. This is **normal**. MCP servers are meant to be controlled by a client (like our `client.py`).
*   **PowerShell Execution Policy Error:**
    *   *Fix:* Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in your terminal to allow the `.venv` to work properly.

---

## 📁 Project Structure
```text
MCP/
│
├── server.py           # The MCP Server logic
├── client.py           # The Test Client (Python-only)
├── requirements.txt    # List of installed packages
└── README.md           # This guide
```


Happy coding! 🚀

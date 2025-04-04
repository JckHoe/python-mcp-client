import asyncio
import logging
import json
from typing import Dict, Any, List

from src.server import Server
from src.config import Configuration
from src.tool import Tool

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def display_tools(tools: List[Tool]) -> None:
    """Display available tools in a formatted way."""
    print("\nAvailable Tools:")
    print("-" * 50)
    for tool in tools:
        print(f"\nTool: {tool.name}")
        print(f"Description: {tool.description}")
        if "properties" in tool.input_schema:
            print("Arguments:")
            for arg_name, arg_info in tool.input_schema["properties"].items():
                required = "(required)" if arg_name in tool.input_schema.get("required", []) else "(optional)"
                print(f"  - {arg_name}: {arg_info.get('description', 'No description')} {required}")
    print("\nEnter '/bye' to exit the program")
    print("-" * 50)

async def get_tool_arguments(tool: Tool) -> Dict[str, Any]:
    """Interactively get arguments for a tool from user input."""
    arguments = {}
    if "properties" not in tool.input_schema:
        return arguments

    print(f"\nEnter arguments for {tool.name}:")
    for arg_name, arg_info in tool.input_schema["properties"].items():
        required = arg_name in tool.input_schema.get("required", [])
        prompt = f"{arg_name}"
        if required:
            prompt += " (required)"
        else:
            prompt += " (optional, press Enter to skip)"
        
        value = input(f"{prompt}: ").strip()
        
        if value or required:
            arguments[arg_name] = value

    return arguments

async def main() -> None:
    """Initialize and run the chat session."""
    config = Configuration()
    server_config = config.load_config("servers_config.json")
    servers = [
        Server(name, srv_config)
        for name, srv_config in server_config["mcpServers"].items()
    ]

    for server in servers:
        try:
            await server.initialize()
        except Exception as e:
            logging.error(f"Failed to initialize server: {e}")
            return

    all_tools = []
    tool_map = {} 
    for server in servers:
        tools = await server.list_tools()
        all_tools.extend(tools)
        for tool in tools:
            tool_map[tool.name] = (server, tool)

    while True:
        display_tools(all_tools)
        tool_name = input("\nEnter tool name to use (or /bye to exit): ").strip()
        
        if tool_name.lower() == '/bye':
            print("Goodbye!")
            break
        
        if tool_name not in tool_map:
            print(f"Tool '{tool_name}' not found. Please try again.")
            continue
        
        server, tool = tool_map[tool_name]
        try:
            arguments = await get_tool_arguments(tool)
            result = await server.execute_tool(tool_name, arguments)

            if isinstance(result, dict) and "progress" in result:
                progress = result["progress"]
                total = result["total"]
                percentage = (progress / total) * 100
                logging.info(
                    f"Progress: {progress}/{total} "
                    f"({percentage:.1f}%)"
                )

            print(f"\nTool execution result:")
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            error_msg = f"Error executing tool: {str(e)}"
            logging.error(error_msg)
            print(f"\nError: {error_msg}")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")

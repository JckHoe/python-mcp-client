import asyncio
import logging

from server import Server
from src.config import Configuration

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
            # await self.cleanup_servers()
            return

    all_tools = []
    for server in servers:
        tools = await server.list_tools()
        all_tools.extend(tools)

    tools_description = "\n".join([tool.format_for_llm() for tool in all_tools])

    logging.info(tools_description)

    # # Update the tool call tool to be from cli
    # for server in servers:
    #     tools = await server.list_tools()
    #     if any(tool.name == tool_call["tool"] for tool in tools):
    #         try:
    #             result = await server.execute_tool(
    #                 tool_call["tool"], tool_call["arguments"]
    #             )
    #
    #             if isinstance(result, dict) and "progress" in result:
    #                 progress = result["progress"]
    #                 total = result["total"]
    #                 percentage = (progress / total) * 100
    #                 logging.info(
    #                     f"Progress: {progress}/{total} "
    #                     f"({percentage:.1f}%)"
    #                 )
    #
    #             return f"Tool execution result: {result}"
    #         except Exception as e:
    #             error_msg = f"Error executing tool: {str(e)}"
    #             logging.error(error_msg)
    #             return error_msg
    #


if __name__ == "__main__":
    asyncio.run(main())

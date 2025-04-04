# MCP CLI Tool

A command-line interface for interacting with MCP (Model Control Protocol) servers. This tool allows you to easily interact with various AI models through a simple command-line interface.

## Features

- Interactive CLI interface
- Support for multiple MCP servers
- Easy-to-use argument prompts
- Progress tracking for long-running operations
- Configurable server settings

## Installation

You can install the package directly from GitHub using pip:

```bash
pip install git+https://github.com/yourusername/mcp-cli.git
```

Or from PyPI:

```bash
pip install mcp-cli
```

## Configuration

Create a `servers_config.json` file with your MCP server configuration:

```json
{
  "mcpServers": {
    "mcp-hfspace": {
      "command": "npx",
      "args": [
        "-y",
        "@llmindset/mcp-hfspace",
        "shuttleai/shuttle-jaguar",
        "styletts2/styletts2",
        "Qwen/QVQ-72B-preview"
      ]
    }
  }
}
```

## Usage

Run the CLI tool:

```bash
mcp-cli
```

Or specify a custom configuration file:

```bash
mcp-cli -c path/to/config.json
```

Enable verbose logging:

```bash
mcp-cli -v
```

## Available Tools

The tool will display all available tools from your configured MCP servers. Each tool will show:
- Name
- Description
- Required and optional arguments

## Interactive Usage

1. The tool will display a list of available tools
2. Enter the name of the tool you want to use
3. Follow the prompts to enter required and optional arguments
4. View the results of the tool execution
5. Type '/bye' to exit the program

## Development

To set up the development environment:

```bash
git clone https://github.com/yourusername/mcp-cli.git
cd mcp-cli
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## License

MIT License

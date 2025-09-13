#!/usr/bin/env python3
"""
Test the simplified MCP server
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_simple_mcp_server():
    """Test the simplified MCP server"""
    print("🧪 Testing Simple Twitter MCP Server...")

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "main.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                # Initialize
                await session.initialize()
                print("✅ Server initialized")

                # List tools
                tools = await session.list_tools()
                print(f"📋 Found {len(tools.tools)} tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}")

                # Test with nossa_ym handle
                print(f"\n🐦 Testing with @nossa_ym (2 tweets)...")
                result = await session.call_tool(
                    "scrape_twitter_handles",
                    arguments={
                        "twitterHandles": ["nossa_ym"],
                        "maxItems": 2
                    }
                )

                print("✅ Raw JSON Response:")
                if result.content:
                    text = result.content[0].text
                    # Show first 500 chars for brevity
                    if len(text) > 500:
                        print(text[:500] + "\n... [truncated] ...")
                    else:
                        print(text)
                else:
                    print("No content returned")

            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_mcp_server())
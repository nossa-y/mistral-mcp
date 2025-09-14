#!/usr/bin/env python3
"""
Test the Social Media Cold Outreach MCP Server
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_simple_mcp_server():
    """Test the Social Media Cold Outreach MCP Server"""
    print("🧪 Testing Social Media Cold Outreach MCP Server...")

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

                # Test Twitter handle
                print(f"\n🐦 Testing Twitter with @elonmusk...")
                twitter_result = await session.call_tool(
                    "scrape_twitter_handles",
                    arguments={
                        "twitterHandle": "elonmusk",
                        "maxItems": 3
                    }
                )

                print("✅ Twitter Response:")
                if twitter_result.content:
                    text = twitter_result.content[0].text
                    # Show first 500 chars for brevity
                    if len(text) > 500:
                        print(text[:500] + "\n... [truncated] ...")
                    else:
                        print(text)
                else:
                    print("No Twitter content returned")

                # Test LinkedIn profile
                print(f"\n💼 Testing LinkedIn with satyanadella...")
                linkedin_result = await session.call_tool(
                    "scrape_linkedin_profile",
                    arguments={
                        "username": "satyanadella",
                        "limit": 5
                    }
                )

                print("✅ LinkedIn Response:")
                if linkedin_result.content:
                    text = linkedin_result.content[0].text
                    # Show first 500 chars for brevity
                    if len(text) > 500:
                        print(text[:500] + "\n... [truncated] ...")
                    else:
                        print(text)
                else:
                    print("No LinkedIn content returned")

            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_mcp_server())
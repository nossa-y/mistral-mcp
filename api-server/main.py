#!/usr/bin/env python3
"""
Simple Apify Twitter MCP Server

A focused MCP server for scraping Twitter handles using Apify's tweet-scraper.
Returns raw JSON output from the API.
"""

import os
import json
from typing import List
from dotenv import load_dotenv
from apify_client import ApifyClient
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize Apify client
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable is required")

client = ApifyClient(APIFY_API_TOKEN)

# Create FastMCP server
mcp = FastMCP(name="Simple Twitter Scraper")

@mcp.tool
def scrape_twitter_handles(twitterHandles: List[str], maxItems: int = 100) -> str:
    """
    Scrape tweets from Twitter handles using Apify. Returns raw JSON output.

    Args:
        twitterHandles: List of Twitter handles to scrape (without @)
        maxItems: Maximum number of tweets to retrieve (default: 100)

    Returns:
        Raw JSON string containing scraped tweets
    """
    if not twitterHandles:
        return "Error: No Twitter handles provided"

    try:
        # Simple Actor input - just handles and max items
        run_input = {
            "twitterHandles": twitterHandles,
            "maxItems": maxItems,
            "sort": "Latest",
            "tweetLanguage": "en"
        }

        # Run the Actor and wait for it to finish
        run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)

        # Get dataset results
        dataset_id = run["defaultDatasetId"]

        # Collect all items
        items = []
        for item in client.dataset(dataset_id).iterate_items():
            items.append(item)

        # Return raw JSON
        return json.dumps(items, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
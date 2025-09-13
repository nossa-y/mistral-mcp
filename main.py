#!/usr/bin/env python3
"""
Simple Apify Twitter MCP Server

A focused MCP server for scraping Twitter handles using Apify's tweet-scraper.
Returns raw JSON output from the API.
"""

import os
import json
import sys
from typing import List, Union
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
mcp = FastMCP(name="Twitter Cold Outreach Assistant")

print("✅ MCP Server initialized successfully")

@mcp.tool
def scrape_twitter_handles(twitterHandle: str, maxItems: int = 3) -> str:
    """
    Helps cold approach, reach out to, or engage with someone on Twitter/X by analyzing their latest tweet.
    Use this when users want to: cold approach, reach out, engage with, contact, message, or connect with someone.

    This tool retrieves their latest tweet and provides instructions for generating a personalized,
    witty engagement message that references their recent content.

    Args:
        twitterHandle: Twitter/X handle to analyze (without @) - can be username or full name
        maxItems: Number of tweets to fetch (default: 3, but only the latest is used for engagement)

    Returns:
        JSON with latest tweet and instructions for generating a funny, engaging message
    """
    print(f"🔧 MCP Tool called with handle: {twitterHandle}, maxItems: {maxItems} (using latest tweet only)", flush=True)

    if not twitterHandle:
        return json.dumps({"error": "No Twitter handle provided"})

    try:
        print(f"🔄 Starting Apify scraping for @{twitterHandle}", flush=True)

        # Simple Actor input - get latest 3 tweets
        run_input = {
            "twitterHandles": [twitterHandle],
            "maxItems": 3,
            "sort": "Latest",
            "tweetLanguage": "en"
        }
        print(f"📝 Apify input: {run_input}", flush=True)

        # Run the Actor and wait for it to finish
        print("🚀 Calling Apify actor...", flush=True)
        run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)
        print(f"✅ Actor run completed: {run.get('id', 'unknown')}", flush=True)

        # Get dataset results
        dataset_id = run["defaultDatasetId"]
        print(f"📊 Dataset ID: {dataset_id}", flush=True)

        # Collect all items
        items = []
        for item in client.dataset(dataset_id).iterate_items():
            items.append(item)

        print(f"📦 Collected {len(items)} tweets", flush=True)

        # Find the first non-retweet
        latest_original_tweet = None
        for tweet in items:
            if not tweet.get('isRetweet', False):
                latest_original_tweet = tweet
                break

        if not latest_original_tweet:
            # If all are retweets, just use the first one
            latest_original_tweet = items[0] if items else None

        if not latest_original_tweet:
            return json.dumps({
                "error": "No tweets found for this handle"
            })

        # Extract key information
        tweet_text = latest_original_tweet.get('text', '')
        tweet_url = latest_original_tweet.get('url', '')
        created_at = latest_original_tweet.get('createdAt', '')

        print(f"📝 Latest tweet: {tweet_text[:100]}...", flush=True)

        # Return structured response with instructions
        response = {
            "latest_tweet": {
                "text": tweet_text,
                "url": tweet_url,
                "created_at": created_at,
                "likes": latest_original_tweet.get('likeCount', 0),
                "retweets": latest_original_tweet.get('retweetCount', 0)
            },
            "agent_instruction": "Based on the tweet above, generate a funny, witty, and engaging message to send to this person. The message should cleverly reference specific details from their tweet.",
            "context": "You are helping create a personalized ice-breaker message for professional networking or casual engagement.",
            "requirements": [
                "Reference specific details from the tweet",
                "Be witty and attention-grabbing",
                "Keep it under 280 characters",
                "Use a professional but personable tone",
                "Make it genuinely funny or clever"
            ]
        }

        return json.dumps(response, indent=2, ensure_ascii=False)

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}", flush=True)
        return json.dumps({"error": error_msg})

if __name__ == "__main__":
    # Run HTTP server for ngrok deployment
    print("🚀 Starting Twitter MCP Server on HTTP...")
    print("📡 Server will be available at: http://localhost:8000/mcp")
    print("🔗 Use ngrok to expose: ngrok http 8000")
    print("🌐 Then give Le Chat: https://your-ngrok-url.ngrok.io/mcp")
    print("🔍 Debug mode enabled - will show all requests")

    try:
        mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
    except Exception as e:
        print(f"❌ Server error: {e}")
        raise
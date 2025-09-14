#!/usr/bin/env python3
"""
Social Media Cold Outreach MCP Server

MCP server for scraping Twitter/X and LinkedIn profiles to generate personalized
outreach messages. Uses Apify actors for reliable data extraction.
"""

import os
import json
import sys
import time
from typing import List, Union, Optional
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient
from fastmcp import FastMCP
import weave

# Load environment variables
load_dotenv()

# Initialize Weave tracking
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
if WANDB_API_KEY:
    os.environ["WANDB_API_KEY"] = WANDB_API_KEY
    weave.init('mcp-social-outreach')
    print("🐝 Weave tracking initialized")
else:
    print("⚠️ WANDB_API_KEY not found - Weave tracking disabled")

# Initialize Apify client
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable is required")

client = ApifyClient(APIFY_API_TOKEN)

# Create FastMCP server
mcp = FastMCP(name="Social Media Cold Outreach Assistant")

print("✅ MCP Server initialized successfully")

@mcp.tool
@weave.op()
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

    # If the handle looks like a full name (e.g., "First Last"), convert to joined format "firstlast"
    if " " in twitterHandle and not twitterHandle.startswith("http"):
        twitterHandle = twitterHandle.strip().replace(" ", "").lower()

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
                "retweets": latest_original_tweet.get('retweetCount', 0),
                "platform": "twitter"
            },
            "agent_instruction": "Based on the tweet above, generate a HILARIOUS, playful, and attention-grabbing message that will make this person stop scrolling and laugh out loud. Be bold, creative, and memorable!",
            "context": "You are creating an ice-breaker that breaks through the noise of boring DMs. This person gets hundreds of messages - yours needs to STAND OUT and be genuinely entertaining.",
            "requirements": [
                "Be genuinely funny and playful (not corporate funny)",
                "Reference specific details from their tweet in a clever/unexpected way",
                "Use humor, wordplay, memes, or surprising angles",
                "Be bold and attention-grabbing (but not offensive)",
                "Keep it under 280 characters",
                "Make them want to respond because it's actually entertaining",
                "Think 'would I screenshot this and send it to friends?' level of wit"
            ]
        }

        return json.dumps(response, indent=2, ensure_ascii=False)

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}", flush=True)
        return json.dumps({"error": error_msg})

@mcp.tool
@weave.op()
def scrape_linkedin_profile(username: str, limit: int = 5, total_posts: Optional[int] = None) -> str:
    """
    Helps cold approach, reach out to, or engage with someone on LinkedIn by analyzing their recent posts.
    Use this when users want to: cold approach, reach out, engage with, contact, message, or connect with someone on LinkedIn.

    This tool retrieves their recent posts and provides instructions for generating a personalized,
    professional engagement message that references their recent content.

    Args:
        username: LinkedIn username (e.g., 'satyanadella' or full URL 'linkedin.com/in/satyanadella')
        limit: Number of posts per page (default: 5, max: 100)
        total_posts: If set, enables automatic pagination to fetch this many posts total

    Returns:
        JSON with latest post and instructions for generating a professional, engaging message
    """
    print(f"🔧 MCP Tool called for LinkedIn profile: {username}, limit: {limit}", flush=True)

    if not username:
        return json.dumps({"error": "No LinkedIn username provided"})

    try:
        print(f"🔄 Starting Apify scraping for LinkedIn profile: {username}", flush=True)

        # Extract username from URL if provided
        if 'linkedin.com/in/' in username:
            username = username.split('linkedin.com/in/')[-1].strip('/')
        
        # If the username looks like a full name (e.g., "First Last"), convert to LinkedIn slug format "first-last"
        if " " in username and not username.startswith("http"):
            username = username.strip().lower().replace(" ", "-")

        # Actor input for LinkedIn
        run_input = {
            "username": username,
            "limit": limit
        }

        # Add total_posts if specified for automatic pagination
        if total_posts:
            run_input["total_posts"] = total_posts
            print(f"📝 Fetching up to {total_posts} total posts with pagination", flush=True)

        print(f"📝 Apify input: {run_input}", flush=True)

        # Run the Actor and wait for it to finish
        print("🚀 Calling Apify LinkedIn actor...", flush=True)
        run = client.actor("apimaestro/linkedin-profile-posts").call(run_input=run_input)
        print(f"✅ Actor run completed: {run.get('id', 'unknown')}", flush=True)

        # Get dataset results
        dataset_id = run["defaultDatasetId"]
        print(f"📊 Dataset ID: {dataset_id}", flush=True)

        # Collect all items
        items = []
        for item in client.dataset(dataset_id).iterate_items():
            items.append(item)

        print(f"📦 Collected {len(items)} LinkedIn posts", flush=True)

        if not items:
            return json.dumps({
                "error": "No posts found for this LinkedIn profile"
            })

        # Get the most recent post (first item)
        latest_post = items[0]

        # Extract key information
        post_text = latest_post.get('text', '')
        post_url = latest_post.get('url', '')
        posted_at = latest_post.get('posted_at', {})
        post_date = posted_at.get('date', '')
        relative_time = posted_at.get('relative', '')
        author_info = latest_post.get('author', {})
        stats = latest_post.get('stats', {})

        print(f"📝 Latest LinkedIn post: {post_text[:100]}...", flush=True)
        print(f"📅 Posted: {post_date} ({relative_time})", flush=True)

        # Return structured response with instructions
        response = {
            "latest_post": {
                "text": post_text,
                "url": post_url,
                "posted_date": post_date,
                "relative_time": relative_time,
                "author": {
                    "name": f"{author_info.get('first_name', '')} {author_info.get('last_name', '')}".strip(),
                    "headline": author_info.get('headline', ''),
                    "username": author_info.get('username', username),
                    "profile_url": author_info.get('profile_url', '')
                },
                "engagement": {
                    "total_reactions": stats.get('total_reactions', 0),
                    "comments": stats.get('comments', 0),
                    "reposts": stats.get('reposts', 0),
                    "likes": stats.get('like', 0),
                    "celebrates": stats.get('celebrate', 0),
                    "supports": stats.get('support', 0)
                },
                "platform": "linkedin"
            },
            "agent_instruction": "Based on the LinkedIn post above, generate a playful, witty, and memorable message that stands out from boring LinkedIn spam. Be professional enough for LinkedIn but fun enough to get their attention and make them smile!",
            "context": "You are creating a LinkedIn message that breaks through the sea of generic connection requests. This person gets tons of boring 'I'd like to add you to my network' messages - yours should make them chuckle and actually want to connect.",
            "requirements": [
                "Be genuinely witty and playful (not stiff corporate speak)",
                "Reference specific details from their post with humor or clever insights",
                "Use light humor, wordplay, or unexpected perspectives",
                "Professional enough for LinkedIn, fun enough to be memorable",
                "Keep it concise (under 300 characters for connection request)",
                "Make them curious about who you are and want to respond",
                "Think 'finally, someone who actually read my post and has personality' vibe"
            ]
        }

        return json.dumps(response, indent=2, ensure_ascii=False)

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}", flush=True)
        return json.dumps({"error": error_msg})

if __name__ == "__main__":
    # Run HTTP server for ngrok deployment
    print("🚀 Starting Social Media Cold Outreach MCP Server on HTTP...")
    print("📡 Server will be available at: http://localhost:8000/mcp")
    print("🔗 Use ngrok to expose: ngrok http 8000")
    print("🌐 Then give Le Chat: https://your-ngrok-url.ngrok.io/mcp")
    print("🔍 Debug mode enabled - will show all requests")
    print("\n📱 Available tools:")
    print("  - scrape_twitter_handles: Analyze Twitter/X profiles")
    print("  - scrape_linkedin_profile: Analyze LinkedIn profiles")

    try:
        mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
    except Exception as e:
        print(f"❌ Server error: {e}")
        raise
#!/usr/bin/env python3
"""
Direct test of the MCP tools
"""

import json
from apify_client import ApifyClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
client = ApifyClient(APIFY_API_TOKEN)

def test_twitter():
    """Test Twitter scraping"""
    print("🐦 Testing Twitter scraping...")

    run_input = {
        "twitterHandles": ["elonmusk"],
        "maxItems": 1,
        "sort": "Latest",
        "tweetLanguage": "en"
    }

    try:
        run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)
        dataset_id = run["defaultDatasetId"]

        items = []
        for item in client.dataset(dataset_id).iterate_items():
            items.append(item)
            break  # Just get first item

        if items:
            tweet = items[0]
            print(f"✅ Tweet retrieved: {tweet.get('text', '')[:100]}...")
            print(f"📅 Created at: {tweet.get('createdAt', 'N/A')}")
            print(f"💚 Likes: {tweet.get('likeCount', 0)}")
            return True
    except Exception as e:
        print(f"❌ Twitter test failed: {e}")
        return False

def test_linkedin():
    """Test LinkedIn scraping"""
    print("\n💼 Testing LinkedIn scraping...")

    run_input = {
        "username": "satyanadella",
        "limit": 1
    }

    try:
        run = client.actor("apimaestro/linkedin-profile-posts").call(run_input=run_input)
        dataset_id = run["defaultDatasetId"]

        items = []
        for item in client.dataset(dataset_id).iterate_items():
            items.append(item)
            break  # Just get first item

        if items:
            post = items[0]
            print(f"✅ Post retrieved: {post.get('text', '')[:100]}...")
            posted_at = post.get('posted_at', {})
            print(f"📅 Posted date: {posted_at.get('date', 'N/A')}")
            print(f"⏰ Relative: {posted_at.get('relative', 'N/A')}")
            stats = post.get('stats', {})
            print(f"💚 Reactions: {stats.get('total_reactions', 0)}")
            return True
    except Exception as e:
        print(f"❌ LinkedIn test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Direct Apify API Tests")
    print("=" * 50)

    twitter_ok = test_twitter()
    linkedin_ok = test_linkedin()

    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Twitter: {'✅ PASSED' if twitter_ok else '❌ FAILED'}")
    print(f"LinkedIn: {'✅ PASSED' if linkedin_ok else '❌ FAILED'}")
    print("=" * 50)
#!/usr/bin/env python3
"""
Test script to verify Weave integration with the MCP server.
This script tests the Weave tracking functionality without running the full server.
"""

import os
import json
import weave
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Weave tracking for testing
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
if WANDB_API_KEY:
    os.environ["WANDB_API_KEY"] = WANDB_API_KEY
    weave.init('mcp-social-outreach-test')
    print("🐝 Weave testing initialized")
else:
    print("❌ WANDB_API_KEY not found - cannot test Weave integration")
    exit(1)

@weave.op()
def test_twitter_function(twitter_handle: str, max_items: int = 3) -> dict:
    """
    Test function to simulate Twitter scraping with Weave tracking.
    This creates a trace without calling the actual Apify API.
    """
    print(f"🔧 Testing Weave tracking for Twitter handle: {twitter_handle}")

    # Simulate processing time
    import time
    time.sleep(0.5)

    # Simulate response data
    response = {
        "handle": twitter_handle,
        "max_items": max_items,
        "simulated_tweet": {
            "text": "Just shipped a new feature! 🚀 Excited to see how users respond.",
            "url": f"https://twitter.com/{twitter_handle}/status/123456789",
            "created_at": "2024-01-15T10:30:00Z",
            "likes": 42,
            "retweets": 7,
            "platform": "twitter"
        },
        "agent_instruction": "Generate a witty response referencing their new feature launch",
        "test_metadata": {
            "weave_tracked": True,
            "simulation": True
        }
    }

    print(f"✅ Simulated Twitter data for @{twitter_handle}")
    return response

@weave.op()
def test_linkedin_function(username: str, limit: int = 5) -> dict:
    """
    Test function to simulate LinkedIn scraping with Weave tracking.
    This creates a trace without calling the actual Apify API.
    """
    print(f"🔧 Testing Weave tracking for LinkedIn profile: {username}")

    # Simulate processing time
    import time
    time.sleep(0.7)

    # Simulate response data
    response = {
        "username": username,
        "limit": limit,
        "simulated_post": {
            "text": "Reflecting on an incredible year of growth and learning in the tech industry. Looking forward to new challenges ahead!",
            "url": f"https://linkedin.com/in/{username}/posts/123456",
            "posted_date": "2024-01-14",
            "relative_time": "1d ago",
            "author": {
                "name": "Test User",
                "headline": "Senior Software Engineer at TechCorp",
                "username": username
            },
            "engagement": {
                "total_reactions": 156,
                "comments": 23,
                "likes": 134,
                "celebrates": 12
            },
            "platform": "linkedin"
        },
        "agent_instruction": "Create a professional message referencing their career growth reflections",
        "test_metadata": {
            "weave_tracked": True,
            "simulation": True
        }
    }

    print(f"✅ Simulated LinkedIn data for {username}")
    return response

@weave.op()
def test_batch_operations() -> dict:
    """
    Test function to simulate batch operations and track performance metrics.
    """
    print("🔧 Testing batch operations with Weave tracking")

    import time
    start_time = time.time()

    # Simulate multiple operations
    results = []
    test_handles = ["elonmusk", "sundarpichai", "satyanadella"]

    for handle in test_handles:
        result = test_twitter_function(handle, 5)
        results.append({
            "handle": handle,
            "success": True,
            "data_size": len(str(result))
        })
        time.sleep(0.2)  # Simulate API rate limiting

    duration = time.time() - start_time

    batch_result = {
        "operation": "batch_twitter_scraping",
        "total_handles": len(test_handles),
        "success_count": len(results),
        "total_duration": duration,
        "average_duration": duration / len(test_handles),
        "results": results,
        "test_metadata": {
            "weave_tracked": True,
            "batch_operation": True
        }
    }

    print(f"✅ Batch operation completed in {duration:.2f}s")
    return batch_result

def main():
    """
    Run comprehensive tests to verify Weave integration.
    """
    print("🧪 Starting Weave integration tests...")
    print("="*50)

    try:
        # Test 1: Twitter function
        print("\n📱 Test 1: Twitter scraping simulation")
        twitter_result = test_twitter_function("elonmusk", 3)
        print(f"   Result keys: {list(twitter_result.keys())}")

        # Test 2: LinkedIn function
        print("\n💼 Test 2: LinkedIn scraping simulation")
        linkedin_result = test_linkedin_function("satyanadella", 5)
        print(f"   Result keys: {list(linkedin_result.keys())}")

        # Test 3: Batch operations
        print("\n📊 Test 3: Batch operations simulation")
        batch_result = test_batch_operations()
        print(f"   Processed {batch_result['total_handles']} handles in {batch_result['total_duration']:.2f}s")

        # Test 4: Error simulation
        print("\n🚨 Test 4: Error handling simulation")
        try:
            # This should work fine and be tracked
            error_test = test_twitter_function("", 0)  # Empty handle
        except Exception as e:
            print(f"   Handled error: {str(e)}")

        print("\n✅ All Weave integration tests completed successfully!")
        print("🐝 Check your Weave dashboard at https://wandb.ai/your-username/mcp-social-outreach-test")
        print("📊 You should see traces for all the test functions above")

    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
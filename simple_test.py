#!/usr/bin/env python3
"""
Simple Le Chat Test - Just the generated message
"""

import os
import json
from dotenv import load_dotenv
import openai

load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_mock_twitter_response():
    return {
        "latest_tweet": {
            "text": "I built this tool just for myself\n\n- Because I couldn't afford to hire a Sales or work with an agency\n- And everything out there was either too expensive or overkilling\n\nBut I randomly met this 3x founder while taking my breakfast at the hotel\n\nHe said: \"I'll pay for this—just let me use it.\"\n\nDecided to share it instead\n\nFeel free too use it\nI wish I knew about supabase when I started building",
            "url": "https://twitter.com/Nossa_ym/status/1834567890",
            "created_at": "2024-09-13T10:30:00Z",
            "likes": 150,
            "retweets": 25,
            "platform": "twitter"
        },
        "agent_instruction": "Based on the tweet above, generate a witty, clever conversation starter with playful observations. Be cool and fun with smart wordplay or unexpected angles on their story.",
        "context": "You're at the same event as this person and want to approach them naturally. Create an opening line that references their work without being awkward or overly flattering. Make it conversational and genuine.",
        "requirements": [
            "Be witty and playful with clever observations or wordplay",
            "Use unexpected angles or fun metaphors (like the breakfast/eggs example)",
            "Be casual and cool - show intelligence through humor",
            "Keep it short and punchy (1-2 sentences max)",
            "Make playful observations about their situation or story",
            "NEVER use 'I saw', 'I heard', 'I read', 'I know' - just make observations",
            "Think 'witty friend making clever comments at a party'"
        ]
    }

def get_mock_linkedin_response():
    return {
        "latest_post": {
            "text": "We won the 1st Prize at the Hugging Face x Zama selective hackathon! 🏆\n\nLast week, 50 AI coders across Europe were selected to take on a challenge involving the use of AI on encrypted data (privacy-preserving AI).\n\nWith my exceptional teammates, Luka, Valentin and Grégoire, we built Parseling, and managed to secure the 1st place in the Big Prizes category.\n\nA few words about Parseling:💡\nParseling comes from the challenge that General Practitioners face when they cannot share sensitive patient data with Research Organizations due to privacy concerns.\n\nDuring these two intense days, we provided a solution that allows Clinical Research Organizations (CROs) to work with Hospitals and Doctors without data leakage using Fully Homomorphic Encryption (FHE).",
            "platform": "linkedin"
        },
        "agent_instruction": "Based on the LinkedIn post above, generate a witty, playful conversation starter with clever observations about their achievement. Be fun and cool with smart wordplay.",
        "context": "You're at the same event as this person and want to start a conversation referencing their recent achievement. Make it sound natural and conversational, like you just recognized them.",
        "requirements": [
            "Be witty and playful with clever observations or wordplay",
            "Use unexpected angles or fun metaphors about their achievement",
            "Be casual and cool - show intelligence through humor",
            "Keep it short and punchy (1-2 sentences max)",
            "Make playful observations about their situation or work",
            "NEVER use 'I' followed by any verb - just make witty observations",
            "Think 'witty friend making clever comments about their success'"
        ]
    }

def generate_message(tool_response):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": str(tool_response)}],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("=== TWITTER ===")
    twitter_response = get_mock_twitter_response()
    twitter_message = generate_message(twitter_response)
    print(twitter_message)
    print(f"Characters: {len(twitter_message)}")

    print("\n=== LINKEDIN ===")
    linkedin_response = get_mock_linkedin_response()
    linkedin_message = generate_message(linkedin_response)
    print(linkedin_message)
    print(f"Characters: {len(linkedin_message)}")
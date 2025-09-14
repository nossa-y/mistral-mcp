# Social Media Cold Outreach MCP Server

A Model Context Protocol (MCP) server designed to help generate personalized engagement messages for Twitter/X and LinkedIn cold outreach. The server analyzes users' latest posts to create contextual ice-breaker messages for professional networking or casual engagement.

## 🎯 Purpose

This MCP server helps AI assistants (like Le Chat, Claude, etc.) create personalized engagement messages for social media outreach by:
- **Twitter/X**: Fetching latest tweets and generating witty, casual engagement messages
- **LinkedIn**: Retrieving recent posts and creating professional, insightful connection requests
- Analyzing post content with date awareness for relevance
- Generating platform-appropriate messages that reference specific details from recent posts

## 🚀 Features

- **Multi-Platform Support**: Separate tools for Twitter/X and LinkedIn
- **Smart Content Analysis**:
  - Twitter: Fetches latest original tweets (skips retweets)
  - LinkedIn: Retrieves recent posts with full engagement metrics
- **Date-Aware**: Includes posting dates for recency-based outreach
- **Platform-Specific Messaging**: Tailored instructions for each platform's culture
- **MCP Integration**: Works with any MCP-compatible AI assistant
- **HTTP Transport**: Easy deployment with ngrok for cloud accessibility
- **Apify Integration**: Uses reliable scrapers for both platforms

## 📋 Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Apify API token (free tier available at [apify.com](https://apify.com))
- ngrok account for remote deployment (optional, for cloud usage)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/mistral-mcp-hackathon.git
cd mistral-mcp-hackathon
```

2. **Set up environment:**
```bash
# Install dependencies using uv
uv sync
```

3. **Configure environment variables:**
```bash
# Create .env file
echo "APIFY_API_TOKEN=your_apify_token_here" > .env
```

Replace `your_apify_token_here` with your actual Apify API token from [Apify Console](https://console.apify.com/account/integrations).

## 🏃‍♂️ Running the Server

### Local Development

```bash
# Start the MCP server
uv run main.py
```

The server will start on `http://localhost:8000/mcp`

### Remote Deployment with ngrok

1. **Install ngrok:**
```bash
# macOS
brew install ngrok

# Or download from https://ngrok.com/download
```

2. **Start ngrok tunnel:**
```bash
ngrok http 8000
```

3. **Note your public URL:**
```
Forwarding: https://abc123.ngrok.io -> http://localhost:8000
```

## 🔌 Connecting to AI Assistants

### Le Chat (Mistral)

1. Go to Le Chat settings
2. Add new MCP server with URL: `https://your-ngrok-url.ngrok.io/mcp`
3. The tools will appear as "Social Media Cold Outreach Assistant"

### Claude Desktop

Add to your Claude config file:
```json
{
  "mcpServers": {
    "social-media-outreach": {
      "command": "uv",
      "args": ["run", "main.py"],
      "cwd": "/path/to/mistral-mcp-hackathon"
    }
  }
}
```

## 📖 API Reference

### Tool 1: `scrape_twitter_handles`

**Purpose:** Analyzes a Twitter user's latest tweet to help generate personalized engagement messages.

**Parameters:**
- `twitterHandle` (string, required): Twitter/X handle without @ symbol
- `maxItems` (int, optional): Number of tweets to fetch (default: 3, but only latest is used)

**Returns:** JSON object containing:
```json
{
  "latest_tweet": {
    "text": "Tweet content...",
    "url": "https://twitter.com/...",
    "created_at": "2024-01-14T...",
    "likes": 42,
    "retweets": 10,
    "platform": "twitter"
  },
  "agent_instruction": "Based on the tweet above...",
  "context": "You are helping create...",
  "requirements": [
    "Reference specific details from the tweet",
    "Be witty and attention-grabbing",
    "Keep it under 280 characters",
    "Use a professional but personable tone",
    "Make it genuinely funny or clever"
  ]
}
```

### Tool 2: `scrape_linkedin_profile`

**Purpose:** Analyzes a LinkedIn user's recent posts to help generate professional connection requests or InMail messages.

**Parameters:**
- `username` (string, required): LinkedIn username or profile URL
- `limit` (int, optional): Posts per page (default: 5, max: 100)
- `total_posts` (int, optional): Enable auto-pagination for this many posts

**Returns:** JSON object containing:
```json
{
  "latest_post": {
    "text": "Post content...",
    "url": "https://linkedin.com/...",
    "posted_date": "2024-01-14 09:30:00",
    "relative_time": "2 days ago",
    "author": {
      "name": "Satya Nadella",
      "headline": "CEO at Microsoft",
      "username": "satyanadella",
      "profile_url": "https://linkedin.com/in/satyanadella"
    },
    "engagement": {
      "total_reactions": 1500,
      "comments": 120,
      "reposts": 45,
      "likes": 1200,
      "celebrates": 150,
      "supports": 100
    },
    "platform": "linkedin"
  },
  "agent_instruction": "Based on the LinkedIn post above...",
  "context": "You are helping create a personalized connection request...",
  "requirements": [
    "Reference specific insights from their post",
    "Be professional yet personable",
    "Show genuine interest in their work",
    "Keep concise (300 chars for connection, 1000 for InMail)",
    "Add value or ask a thoughtful question",
    "Maintain a respectful, professional tone"
  ]
}
```

## 💡 Usage Examples

### Example Prompts for AI Assistants

#### Twitter/X Outreach:
1. **Hilariously Bold Engagement:**
   ```
   "Help me reach out to @elonmusk with something actually funny"
   ```

2. **Meme-Level Cold Approach:**
   ```
   "I want to cold approach @sama with something that'll make him screenshot it"
   ```

#### LinkedIn Outreach:
1. **Playfully Professional Connection:**
   ```
   "Help me connect with satyanadella on LinkedIn without being boring"
   ```

2. **Memorable Business Outreach:**
   ```
   "Generate a LinkedIn message that'll actually get a response from this CEO"
   ```

### Sample Outputs

#### Twitter Example:
When analyzing @user's tweet about "Just launched our new AI product!", the server might help generate:
> "Your AI launch caught my eye! 🚀 The approach to [specific feature] is brilliant. Been working on similar problems - would love to exchange ideas!"

#### LinkedIn Example:
When analyzing a CEO's post about "Leading digital transformation in healthcare", the server might help generate:
> "Your insights on healthcare digital transformation really resonated with me. The point about patient-centric design aligns perfectly with our work at [company]. Would love to connect and share perspectives on scaling these initiatives."

## 🧪 Testing

Run the test suite:
```bash
uv run python test_simple.py
```

Test individual APIs:
```bash
uv run python test_tools.py
```

## 📁 Project Structure

```
mistral-mcp-hackathon/
├── main.py           # MCP server with Twitter & LinkedIn tools
├── test_simple.py    # MCP integration tests
├── test_tools.py     # Direct API tests
├── pyproject.toml    # Project dependencies
├── .env             # Environment variables (create this)
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Common Issues

1. **"APIFY_API_TOKEN environment variable is required"**
   - Ensure `.env` file exists with valid token
   - Get token from [Apify Console](https://console.apify.com/account/integrations)

2. **"No tweets found for this handle"**
   - Verify the Twitter handle exists
   - Check if the account has public tweets
   - Try without the @ symbol

3. **"No posts found for this LinkedIn profile"**
   - Verify the LinkedIn username is correct
   - Check if the profile has public posts
   - Try with just the username (not full URL)

4. **Connection issues with ngrok**
   - Ensure ngrok is running: `ngrok http 8000`
   - Check firewall settings
   - Verify the URL includes `/mcp` path

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check Apify documentation at [docs.apify.com](https://docs.apify.com)
- MCP documentation at [modelcontextprotocol.io](https://modelcontextprotocol.io)
# Simple Twitter MCP Server

A focused MCP server for scraping Twitter handles using Apify's tweet-scraper. Returns raw JSON output.

## Features

- **Simple**: Only requires Twitter handles and optional maxItems
- **Raw Output**: Returns unprocessed JSON from Apify
- **Fast**: Built with FastMCP framework

## Setup

```bash
uv sync
```

## Usage

```bash
uv run main.py
```

## Tool

- `scrape_twitter_handles`: Input Twitter handles, get raw tweet JSON
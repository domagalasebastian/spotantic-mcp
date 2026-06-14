# Spotantic MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

An MCP (Model Context Protocol) server that exposes the Spotify Web API through a standardized interface. Spotantic MCP provides 50+ tools for controlling playback, managing playlists, searching music, and accessing user library data.

## ✨ Features

- **50+ MCP Tools**: Comprehensive coverage of Spotify Web API endpoints
- **Player Control**: Play, pause, skip, queue management, device switching
- **Playlist Management**: Create, modify, and curate playlists
- **Library Operations**: Save/remove/check saved items
- **Search & Discovery**: Cross-category search with pagination
- **User Insights**: Top tracks, top artists, listening history
- **Type-Safe**: Full type hints and validation
- **MCP Inspector Support**: Interactive testing and debugging
- **Multiple Auth Flows**: Client Credentials, Authorization Code, Authorization Code PKCE

## 📋 Prerequisites

- **Python 3.12 or higher**
- **Node.js and npm** (for MCP Inspector testing)
- A Spotify Developer account ([get one at developer.spotify.com](https://developer.spotify.com))
- Client ID and Client Secret from the Spotify Developer Dashboard

## 🔧 Installation

Spotantic MCP is designed to run as an MCP server and must be set up from source.

```bash
# Clone the repository
git clone https://github.com/domagalasebastian/spotantic-mcp.git
cd spotantic-mcp

# Install dependencies
uv sync --group dev

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install MCP Inspector for testing (optional but recommended)
npm install -g @modelcontextprotocol/inspector
```

## ⚙️ Configuration

### 1. Set Up Spotify Credentials

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` with your Spotify Developer credentials:

```bash
# Your application credentials
SPOTANTIC_AUTH_CLIENT_ID=your_client_id_here
SPOTANTIC_AUTH_CLIENT_SECRET=your_client_secret_here
SPOTANTIC_AUTH_REDIRECT_URI=http://127.0.0.1:8000/callback

# Scopes (space-separated)
SPOTANTIC_AUTH_SCOPE="user-read-private user-read-email user-library-read user-library-modify playlist-read-private playlist-modify-private playlist-modify-public user-top-read user-read-recently-played user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state"

# Optional: Token caching
SPOTANTIC_AUTH_ACCESS_TOKEN_FILE_PATH=.token_info_cache
SPOTANTIC_AUTH_STORE_ACCESS_TOKEN=false

# Optional: Logging
SPOTANTIC_LOGGING_ENABLE=false
SPOTANTIC_LOGGING_DEBUG=true
SPOTANTIC_LOGGING_LOGS_DIR=logs/

# Auth method (auth_code_pkce, auth_code, or client_credentials)
SPOTANTIC_MCP_AUTH_METHOD=auth_code_pkce

# Refresh token (obtained from authorization script)
SPOTANTIC_MCP_REFRESH_TOKEN=...
```

### 2. Get Refresh Token

For authorization-based flows (PKCE or Auth Code), obtain a refresh token:

```bash
# Authorize with Spotify (opens browser)
uv run scripts/authorize.py --auth-method code-pkce

# Find the token in the file specified by SPOTANTIC_AUTH_ACCESS_TOKEN_FILE_PATH
cat .token_info_cache

# Copy the refresh token to .env as SPOTANTIC_MCP_REFRESH_TOKEN
```

### 3. Load Environment Variables

Before running the server, load your environment:

```bash
set -o allexport && source .env && set +o allexport
```

## 🚀 Usage

### With MCP Clients (Claude Desktop, IDE Extensions, etc.)

Configure your MCP client to use Spotantic MCP as a server. Here's an example for `.mcp.json`:

```json
{
  "servers": {
    "spotantic": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "$HOME/repos/spotantic-mcp",
        "src/spotantic_mcp/server.py"
      ],
      "envFile": "$HOME/repos/spotantic-mcp/.env"
    }
  }
}
```

**Configuration Details:**

- **command**: `uv` - Uses Python package manager
- **args**: Runs the server script with the project directory
- **envFile**: Path to your `.env` configuration file
- **$HOME**: Automatically expands to your home directory

### Running the Server Directly

```bash
# Ensure env is loaded
set -o allexport && source .env && set +o allexport

# Run the server
uv run src/spotantic_mcp/server.py
```

## 🧪 Testing with MCP Inspector

The MCP Inspector provides an interactive interface to test tools and view request/response payloads.

### Setup

1. **Authorize with Spotify** (if needed):
   ```bash
   uv run scripts/authorize.py --auth-method code-pkce
   ```

2. **Configure `.env`** with your credentials and refresh token

3. **Load environment variables**:
   ```bash
   set -o allexport && source .env && set +o allexport
   ```

4. **Start the inspector**:
   ```bash
   npx @modelcontextprotocol/inspector uv run --directory $HOME/repos/spotantic-mcp src/spotantic_mcp/server.py
   ```

This opens an interactive browser interface where you can:
- Call MCP tools directly
- View request/response payloads
- Test authentication
- Debug API interactions
- Inspect error handling

## 🎵 Available Tools

Spotantic MCP provides 50+ tools organized by resource type:

### Player Control (15 tools - Premium Required)

- **Playback**: Start, pause, resume playback
- **Navigation**: Skip next, skip previous
- **Queue**: Add items, view current queue
- **Devices**: List devices, transfer playback
- **Settings**: Volume, repeat mode, shuffle toggle
- **Status**: Get playback state, currently playing track

### Library Management (3 tools)

- **Save/Remove**: Add or remove items from user library
- **Check Saved**: Verify if items are saved
- Supports: tracks, albums, episodes, shows, artists, playlists

### Playlist Curation (8 tools)

- **Create/Update**: Create playlists, modify details
- **Browse**: Get user's playlists and playlist items
- **Modify**: Add/remove items, reorder tracks

### Search & Discovery (1 tool)

- Search across: tracks, artists, albums, playlists, shows, episodes
- Pagination support for large result sets

### User Insights (4 tools)

- Top tracks and artists (multiple time ranges)
- Recently played tracks
- Followed artists
- User profile information

### Content Details (13+ tools)

- **Albums**: Album details, tracks, new releases
- **Artists**: Artist profiles, discography, top tracks
- **Tracks**: Track details and metadata
- **Episodes**: Podcast episode information
- **Shows**: Podcast show details and episodes

## 📚 Tool Reference

For detailed information about each tool, including parameters and return types, see the [Available Tools](src/spotantic_mcp/tools/endpoints) in the source code.

### Example: Get User's Top Tracks

When used via MCP client:

```
Tool: get_user_top_tracks
Parameters:
  - time_range: "medium_term" (options: short_term, medium_term, long_term)
  - limit: 20 (max 50)
  - offset: 0

Returns:
  List of top tracks with full metadata (artists, album, duration, etc.)
```

### Example: Create and Populate a Playlist

```
1. Tool: create_playlist
   Parameters:
     - name: "My Awesome Mix"
     - description: "Songs I found today"
     - public: false

2. Tool: add_items_to_playlist
   Parameters:
     - playlist_id: <from step 1>
     - uris: ["spotify:track:...", "spotify:track:..."]
```

## 🎭 Example: Festival Setlist Preparation with Personal DJ

Here's a practical example of using the agent to prepare for a music festival by creating a playlist based on artist setlists:

**Prompt:**

> I am going to attend the Open'er Festival in Gdynia on Day 4 (04.07.2026). I am especially interested in the concerts of these artists: JENNIE, Addison Rae, Teddy Swims, Peggy Gou, Lordofon, and PinkPantheress. Create a playlist for me so I can prepare to sing along near the stage on that day.
>
> You can use these links to analyze their recent live setlists and match the tracks accurately:
> - https://www.setlist.fm/setlist/jennie/2026/flushing-meadows-corona-park-queens-ny-234d4cd3.html
> - https://www.setlist.fm/setlist/addison-rae/2026/the-bellwether-los-angeles-ca-6372be4f.html

**What the Personal DJ Agent Does:**

1. **Analyzes setlists** from the provided links to identify the actual songs these artists perform live
2. **Searches Spotify** for each track across all artists
3. **Creates a new playlist** named something like "Open'er 2026 - Day 4 Festival Prep"
4. **Adds tracks** in setlist order to let you experience the same flow as the live performance
5. **Handles variations** like live remixes, alternate versions, or unreleased tracks by finding the closest Spotify matches

**Result:** A curated playlist ready for your commute to the festival, organized to match the energy and flow of each artist's live set. Perfect for learning the setlist so you can sing along during the actual concerts!

This example demonstrates the agent's ability to:
- Gather information from external sources
- Search and match tracks intelligently
- Create and populate playlists programmatically
- Understand context and create emotionally resonant experiences

## 🛠️ Development

### Code Quality

Run quality checks before committing:

```bash
# Format code
uv run ruff format .

# Lint and fix
uv run ruff check --fix .

# Type checking
uv run pyright

# Run all pre-commit checks
uv run pre-commit run --all-files
```

### Running Tests

```bash
# Unit tests
uv run pytest tests/unit -v

# Specific test file
uv run pytest tests/unit/tools/endpoints/player/test_playback.py -v
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Testing requirements
- MCP tool development guidelines
- Commit message conventions
- Pull request process

Key points:
- Follow Conventional Commits format
- All functions must have type hints
- Add unit tests for new features
- Test interactively with MCP Inspector
- Ensure code passes all quality checks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Disclaimer

**This project is not affiliated with, endorsed by, or associated with Spotify AB or any of its subsidiaries or affiliates.** Spotantic MCP is an independent, community-maintained library that provides convenient access to the Spotify Web API through the Model Context Protocol. All Spotify trademarks, logos, and product names are the property of Spotify AB.

Please ensure your use of this library complies with [Spotify's Developer Terms of Service](https://developer.spotify.com/terms).

## 🔗 Resources

- **[Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)**
- **[Model Context Protocol Documentation](https://modelcontextprotocol.io/)**
- **[MCP Inspector Repository](https://github.com/modelcontextprotocol/inspector)**
- **[Spotantic Library](https://github.com/domagalasebastian/spotantic)** - Base async Spotify client library
- **[Contributing Guide](CONTRIBUTING.md)**

## Related Projects

- **[Spotantic](https://github.com/domagalasebastian/spotantic)** - The underlying async Spotify client library that powers this MCP server
- **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)** - Interactive tool for testing and debugging MCP servers

---

Made with ❤️ by [Sebastian Domagała](https://github.com/domagalasebastian)

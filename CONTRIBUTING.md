# Contributing to Spotantic MCP

Thank you for your interest in contributing to Spotantic MCP! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Node.js and npm (for MCP Inspector)
- Git
- A fork of the repository

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/domagalasebastian/spotantic-mcp.git
cd spotantic-mcp

# Install development dependencies and activate virtual environment
uv sync --group dev
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install MCP Inspector globally (for testing)
npm install -g @modelcontextprotocol/inspector
```

## How to Contribute

### 1. Open an Issue

Before starting work on a new feature or bug fix, please open an issue to discuss:
- What you're trying to fix/add
- Your proposed approach
- Any potential impact on the API

### 2. Create a Feature Branch

```bash
git checkout -b feat/your-feature-name
# or for bug fixes:
git checkout -b fix/your-fix-name
```

### 3. Make Your Changes

- Keep commits small and focused
- Follow [Conventional Commits](https://www.conventionalcommits.org/) format
- Write clear commit messages

### 4. Code Quality

Ensure all code quality checks pass:

```bash
# Run pre-commit checks
uv run pre-commit run --all-files

# Run unit tests
uv run pytest tests/unit -v

# Type checking
uv run pyright
```

### 5. Testing with MCP Inspector

This project uses the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to test the MCP server implementation. Unlike traditional integration tests, the inspector provides an interactive way to validate the server's behavior.

#### Setup Inspector Environment

Before running the inspector, you need to set up authentication:

**Step 1: Authorize with Spotify**

```bash
uv run scripts/authorize.py --auth-method code-pkce
```

This will open your browser for Spotify authentication. The script will generate a refresh token and save it to the path specified in `SPOTANTIC_AUTH_ACCESS_TOKEN_FILE_PATH` (default: `.token_info_cache`).

> **Note:** The `--auth-method` must match the `SPOTANTIC_MCP_AUTH_METHOD` setting in your `.env` file. Common options are `code-pkce`, `code`, or `client-credentials`.

**Step 2: Configure Environment Variables**

Copy the refresh token from the file created in Step 1 and add it to your `.env` file:

```bash
# Copy .env.example to .env if you haven't already
cp .env.example .env

# Edit .env and add the refresh token
# SPOTANTIC_MCP_REFRESH_TOKEN=<token_from_authorize.py>
```

**Step 3: Load Environment Variables**

```bash
set -o allexport && source .env && set +o allexport
```

This command loads all variables from `.env` into your shell session.

#### Running the Inspector

Once your environment is set up, start the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv run --directory $HOME/repos/spotantic-mcp src/spotantic_mcp/server.py
```

This will:
1. Start the MCP server via `uv run`
2. Open an interactive inspector interface in your browser
3. Allow you to test tools and examine server responses

You can now:
- Call MCP tools directly
- View request/response payloads
- Debug authentication and API interactions
- Verify error handling

### 6. Testing Requirements

- **Add unit tests** for new functionality in `tests/unit/`
- **Ensure existing tests** still pass
- **Use the MCP Inspector** to validate tool behavior and API interactions

Test structure:
- Endpoint tests: `tests/unit/tools/endpoints/<resource>/test_*.py`
- Tool tests: `tests/unit/tools/test_*.py`

### 7. Documentation

- Update docstrings for public APIs (use Google style)
- Update relevant sections in `README.md` if changing behavior
- Add type hints to all functions
- Document new tools or significant changes in code comments

### 8. Submit a Pull Request

- Fill out the PR template completely
- Reference any related issue with `Closes #123`
- Ensure all CI checks pass
- Test your changes with the MCP Inspector before submitting
- Request reviews from maintainers

## Code Style Guidelines

### Formatting

- Line length: 120 characters
- Use double quotes for strings
- Indent with 4 spaces
- Run `uv run ruff format .` to auto-format

### Linting

- Follow all Ruff rules
- Run `uv run ruff check --fix .` before committing

### Type Hints

- All public functions must have type hints
- Use `from __future__ import annotations` for forward references
- Use type annotations for tool parameters and return types

### Docstrings

- Use Google-style docstrings
- Document parameters, return types, and exceptions
- Example:

```python
def get_user_queue(self) -> GetUserQueueResponseView:
    """Get the current user's playback queue.

    Retrieves information about the currently playing track and the queue.

    Returns:
        GetUserQueueResponseView: The current playback queue.

    Raises:
        SpotifyAPIError: If the API request fails.
    """
```

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Examples**:
- `feat(tools): add support for new playlist filtering options`
- `fix(auth): handle token refresh failures gracefully`
- `docs: update inspector setup instructions`

## MCP Server Development Guidelines

### Adding New Tools

When adding new MCP tools:

1. Create tool definitions in the appropriate endpoint module under `src/spotantic_mcp/tools/endpoints/`
2. Add corresponding view models in `src/spotantic_mcp/tools/endpoints/_views/`
3. Register the tool in `src/spotantic_mcp/tools/_mcp_tools.py`
4. Add unit tests in `tests/unit/tools/endpoints/<resource>/`
5. Test interactively with the MCP Inspector

### Handling Spotify API Errors

Use the error handling utilities in `src/spotantic_mcp/tools/endpoints/_handle_endpoint_errors.py` to:
- Parse Spotify API errors
- Return meaningful error messages to clients
- Log errors appropriately

## Questions?

- Open a GitHub Discussion
- Check existing issues
- Review documentation in the README

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

# Architecture & Design

## Overview

The Facebook Data Downloader is built with a modular, extensible architecture designed to make it easy to add support for other social media platforms.

## Architecture Diagram

```
main.py (CLI Interface)
    ↓
FacebookDataDownloaderCLI
    ├── facebook_auth.py (Authentication)
    ├── facebook_fetcher.py (Data Fetching)
    └── data_exporter.py (Export)
        ↓
    Facebook Graph API
```

## Module Breakdown

### 1. `main.py` - CLI Entry Point

**Responsibility:** User interface and workflow orchestration

**Key Classes:**
- `FacebookDataDownloaderCLI` - Main CLI application
  - `print_banner()` - Display welcome screen
  - `print_menu()` - Show menu options
  - `handle_authentication()` - Manage auth flow
  - `handle_download()` - Orchestrate download process
  - `handle_export_comments()` - Export comments for analysis
  - `handle_view_info()` - Display data statistics
  - `run()` - Main event loop

**Flow:**
1. Display menu
2. Get user choice
3. Delegate to appropriate handler
4. Display results
5. Loop until exit

### 2. `src/facebook_auth.py` - Authentication

**Responsibility:** OAuth authentication and token management

**Key Classes:**
- `FacebookAuth` - Handles OAuth flow
  - `authenticate()` - Initiate OAuth browser flow
  - `get_authorization_url()` - Generate auth URL with required scopes
  - `_exchange_code_for_token()` - Trade authorization code for access token
  - `save_token()` - Store token locally
  - `load_token()` - Retrieve saved token
  - `test_connection()` - Verify token validity

- `CallbackHandler` - HTTP handler for OAuth callback
  - Captures authorization code from redirect
  - Serves confirmation page to user

**OAuth Flow:**
```
1. User selects "Authenticate"
   ↓
2. Generate authorization URL with scopes
   ↓
3. Open browser to Facebook login/consent page
   ↓
4. User authorizes application
   ↓
5. Facebook redirects to http://localhost:8000/callback?code=...
   ↓
6. Local HTTP server captures code
   ↓
7. Exchange code for access token
   ↓
8. Save token to data/token.json
   ↓
9. Token ready for API calls
```

**Scopes Requested:**
- `user_posts` - Read user's posts
- `read_stream` - Read feed/timeline
- `user_friends` - Read friends list
- `public_profile` - Read public profile info

### 3. `src/facebook_fetcher.py` - Data Fetching

**Responsibility:** Retrieve posts and comments from Facebook Graph API

**Key Classes:**
- `FacebookDataFetcher` - Fetches data from Facebook
  - `_make_request()` - Generic API request handler
  - `get_user_info()` - Fetch authenticated user info
  - `get_posts()` - Fetch user's posts with pagination
  - `get_comments()` - Fetch comments for a post
  - `get_post_with_details()` - Get post + comments

**API Endpoints Used:**
- `GET /me` - Current user info
- `GET /me/posts` - User's posts (paginated)
- `GET /{post_id}/comments` - Comments on a post (paginated)

**Features:**
- Automatic pagination handling
- Rate limiting (100ms delay between requests)
- Error handling and logging
- Nested data structure for posts with comments

**Data Fetching Flow:**
```
1. User requests download (limit N posts)
   ↓
2. For each page of posts:
   a. Fetch posts (fields: id, message, created_time, etc.)
   b. For each post:
      i. Fetch comments (fields: id, message, author, etc.)
      ii. Store comments under post
   c. Check for next page
   ↓
3. Return posts list with nested comments
```

### 4. `src/data_exporter.py` - Data Export

**Responsibility:** Convert fetched data to JSON format

**Key Classes:**
- `DataExporter` - Handles JSON export
  - `export_posts_with_comments()` - Export nested structure
  - `export_comments_only()` - Export flat comment list
  - `get_file_info()` - Get file statistics

**Export Formats:**

**Format 1: Nested Posts with Comments**
```json
{
  "metadata": {
    "exported_at": ISO timestamp,
    "total_posts": number,
    "total_comments": number,
    "platform": "facebook"
  },
  "user": { ... },
  "posts": [
    {
      "id": post_id,
      "message": post content,
      "created_time": timestamp,
      "comments": [
        {
          "id": comment_id,
          "message": comment content,
          "author": author name,
          "author_id": author id,
          "like_count": number,
          "created_time": timestamp
        }
      ]
    }
  ]
}
```

**Format 2: Comments Only with Post Reference**
```json
{
  "metadata": { ... },
  "comments": [
    {
      "comment_id": id,
      "comment_text": text,
      "author": name,
      "author_id": id,
      "source_post": {
        "post_id": id,
        "post_text": preview
      }
    }
  ]
}
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│         User runs: python main.py                    │
└────────────────┬────────────────────────────────────┘
                 ↓
         ┌───────────────┐
         │ Display Menu  │
         └───────┬───────┘
                 ↓
    ┌────────────┴────────────┐
    ↓                         ↓
Authenticate            Download Posts
    ↓                         ↓
facebook_auth.py      facebook_fetcher.py
    ↓                         ↓
OAuth Flow           Fetch Posts & Comments
    ↓                         ↓
Save Token            data_exporter.py
    ↓                         ↓
Ready for API              Export JSON
                            ↓
                    Save to data/ folder
```

## File Structure

```
social_media/
├── main.py                           # Entry point (11 KB)
├── requirements.txt                  # Dependencies
├── .env.example                      # Config template
├── .gitignore                        # Git ignore rules
├── README.md                         # Full documentation
├── QUICKSTART.md                     # Quick setup guide
├── ARCHITECTURE.md                   # This file
│
├── src/
│   ├── __init__.py                  # Package marker
│   ├── facebook_auth.py              # OAuth (200 lines)
│   ├── facebook_fetcher.py           # API fetching (150 lines)
│   └── data_exporter.py              # JSON export (120 lines)
│
└── data/                             # Output directory
    ├── token.json                    # Saved auth token (not in repo)
    ├── facebook_data_*.json          # Downloaded posts (not in repo)
    └── facebook_comments_*.json      # Exported comments (not in repo)
```

## Key Design Decisions

### 1. Modular Architecture
- **Why:** Easy to extend with new platforms
- **How:** Each platform would get `{platform}_auth.py` and `{platform}_fetcher.py`
- **Benefit:** Adding Twitter/Reddit/YouTube involves minimal changes to main.py

### 2. Nested JSON Structure
- **Why:** Comments must link back to source posts
- **How:** Comments stored as array within each post object
- **Benefit:** Easy to analyze comment context without additional lookups

### 3. Local Token Storage
- **Why:** Avoid re-authentication on every run
- **How:** Save token in `data/token.json` after auth
- **Benefit:** Smooth user experience, single auth per session

### 4. Rate Limiting Built-In
- **Why:** Respect Facebook API limits
- **How:** 100ms delay between requests
- **Benefit:** Avoids rate limit errors during bulk downloads

### 5. CLI-First Interface
- **Why:** Simple, cross-platform, no dependencies on GUI libraries
- **How:** Python's built-in `input()` for prompts
- **Benefit:** Works on any OS, easy to automate/script

## Security Considerations

### Authentication
- OAuth 2.0 standard (industry best practice)
- Tokens never sent in URLs (only in Authorization headers)
- Redirect URI tied to specific localhost address

### Token Management
- Tokens stored in `data/token.json` (local, private)
- File marked in `.gitignore` (won't be committed)
- Tokens expire and require re-authentication

### Data Privacy
- Only downloads user's own data (scoped to user)
- No personal data in logs or error messages
- User controls what data to download (limit parameter)

## Extensibility Points

### Adding New Platforms

Create `src/twitter_auth.py`:
```python
class TwitterAuth:
    def authenticate(self):
        # Twitter OAuth flow
        pass
```

Create `src/twitter_fetcher.py`:
```python
class TwitterDataFetcher:
    def get_tweets(self):
        # Fetch tweets
        pass
```

Update `main.py`:
```python
def handle_platform_selection(self):
    # Add menu option for platform choice
```

### Adding New Export Formats

Extend `data_exporter.py`:
```python
def export_to_csv(self, posts):
    # Export as CSV
    pass

def export_to_sqlite(self, posts):
    # Export as SQLite database
    pass
```

### Adding Analysis Features

Create `src/comment_analyzer.py`:
```python
class OffensiveCommentDetector:
    def analyze(self, comments):
        # Detect offensive comments
        # Return flagged comments with scores
        pass
```

## Performance Considerations

### Current Implementation
- Fetches one post at a time
- Fetches comments sequentially
- ~5-10 seconds for 10 posts (varies by connection)

### Optimization Opportunities
- Parallel comment fetching (async/await)
- Batch API requests where possible
- Local caching of data
- Incremental updates (only new posts/comments)

### Pagination Handling
- Facebook API returns 100 items max per request
- Tool automatically handles next page
- Respects user limit (max 100 posts)
- Efficient for small-scale downloads

## Testing Strategy

Recommended tests to add:

```python
# test_facebook_auth.py
def test_oauth_url_generation()
def test_token_save_and_load()

# test_facebook_fetcher.py
def test_get_user_info()
def test_get_posts_pagination()
def test_get_comments()

# test_data_exporter.py
def test_export_structure()
def test_nested_comments()
```

## Future Enhancements

1. **Web Interface** - Replace CLI with Flask/React app
2. **Database Storage** - Store data in SQLite/PostgreSQL
3. **Sentiment Analysis** - Analyze comment sentiment
4. **Content Moderation** - Flag offensive comments
5. **Multi-Platform Support** - Add Twitter, Reddit, YouTube
6. **Scheduling** - Schedule regular data downloads
7. **Incremental Updates** - Only fetch new data
8. **Export Formats** - CSV, XML, PDF reports
9. **Data Visualization** - Charts and graphs
10. **API Server** - Expose as REST API

---

This architecture prioritizes simplicity, extensibility, and user experience while maintaining security and best practices.

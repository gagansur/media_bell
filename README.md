# Facebook Data Downloader

A command-line tool to download your Facebook posts and comments for analysis. Perfect for identifying offensive comments and understanding their context within source posts.

## Features

✨ **Key Features:**
- 🔐 Secure OAuth authentication with Facebook
- 📥 Download posts and comments with nested structure
- 💾 Export data in JSON format
- 🔍 Link comments back to source posts
- 📊 Batch download up to 100 posts
- 🔄 Save and reuse authentication tokens

## Project Structure

```
social_media/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── facebook_auth.py    # OAuth authentication
│   ├── facebook_fetcher.py # Data fetching from API
│   └── data_exporter.py    # JSON export functionality
└── data/                   # Output directory for downloaded data
```

## Prerequisites

- Python 3.7 or higher
- A Facebook Developer Account
- A registered Facebook Application

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new application or use an existing one
3. Navigate to **Settings → Basic** to get your:
   - App ID
   - App Secret

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   FACEBOOK_APP_ID=your_app_id_here
   FACEBOOK_APP_SECRET=your_app_secret_here
   FACEBOOK_REDIRECT_URI=http://localhost:8000/callback
   OUTPUT_DIR=./data
   ```

3. In your Facebook App Settings:
   - Go to **Settings → Basic**
   - Add `http://localhost:8000/callback` to **Valid OAuth Redirect URIs**

### 4. Configure App Permissions

Your Facebook App needs these permissions:
- `user_posts` - Read user's posts
- `read_stream` - Read feed
- `user_friends` - Read friends list
- `public_profile` - Read public profile

Add these in **App Roles → Test Users** or **Permissions** section.

## Usage

### Run the CLI

```bash
python main.py
```

### Menu Options

1. **Authenticate with Facebook**
   - Opens browser for OAuth authorization
   - Saves token for future use
   - Tests connection with Facebook API

2. **Download Posts and Comments**
   - Fetches your posts (specify number: 1-100)
   - Downloads comments for each post
   - Exports to nested JSON structure

3. **Export Comments for Analysis**
   - Creates separate file with only comments
   - Includes reference to source posts
   - Useful for content moderation analysis

4. **View Downloaded Data Info**
   - Shows statistics about downloaded files
   - Displays post and comment counts
   - Shows file sizes

5. **Exit**
   - Safely exit the application

### Check Environment Setup

```bash
python main.py --check-env
```

Verifies that environment variables are properly configured.

## Data Format

### Posts with Comments (Nested JSON)

```json
{
  "metadata": {
    "exported_at": "2025-12-26T10:30:45.123456",
    "total_posts": 2,
    "total_comments": 5,
    "platform": "facebook"
  },
  "user": {
    "id": "user_id",
    "name": "User Name",
    "email": "user@example.com"
  },
  "posts": [
    {
      "id": "post_id",
      "message": "Post content here",
      "type": "status",
      "created_time": "2025-12-25T15:30:00+0000",
      "comments": [
        {
          "id": "comment_id",
          "message": "Comment text",
          "created_time": "2025-12-25T16:00:00+0000",
          "author": "Comment Author",
          "author_id": "author_id",
          "like_count": 2
        }
      ]
    }
  ]
}
```

### Comments Only (For Analysis)

```json
{
  "metadata": {
    "exported_at": "2025-12-26T10:30:45.123456",
    "total_comments": 5,
    "platform": "facebook"
  },
  "comments": [
    {
      "comment_id": "comment_id",
      "comment_text": "Comment content",
      "created_time": "2025-12-25T16:00:00+0000",
      "author": "Comment Author",
      "author_id": "author_id",
      "like_count": 2,
      "source_post": {
        "post_id": "post_id",
        "post_text": "Original post preview..."
      }
    }
  ]
}
```

## Output

Downloaded files are saved in the `data/` directory:
- `facebook_data_YYYYMMDD_HHMMSS.json` - Posts with nested comments
- `facebook_comments_YYYYMMDD_HHMMSS.json` - Comments for analysis
- `token.json` - Saved authentication token (local use only)

## Rate Limiting

The tool includes built-in rate limiting:
- 100ms delay between API requests
- Respects Facebook API limits (100 items per page)
- Automatic pagination for large datasets

## Security Notes

⚠️ **Important Security Information:**

1. **Tokens** - Access tokens are stored locally in `data/token.json`
   - Keep this file private
   - Never commit to version control (included in `.gitignore`)
   - Tokens expire and may need re-authentication

2. **Credentials** - Always keep `.env` file private
   - Never commit to repositories
   - Don't share your App Secret

3. **Data Privacy** - Be mindful of privacy when downloading and analyzing data
   - Only analyze data you have permission to access
   - Comply with Facebook's Terms of Service
   - Respect user privacy in downloaded data

## Troubleshooting

### Authentication Issues

**Problem:** Browser doesn't open automatically
- **Solution:** Manually copy the URL from terminal and paste in browser

**Problem:** "Authorization failed - no code received"
- **Solution:** Ensure redirect URI matches in Facebook App settings

**Problem:** "Token is invalid"
- **Solution:** Delete `data/token.json` and re-authenticate

### API Errors

**Problem:** "Rate limit exceeded"
- **Solution:** Wait a few minutes and try again. The tool includes delays.

**Problem:** "Permission denied"
- **Solution:** Ensure your Facebook App has required permissions enabled

### File Issues

**Problem:** No data files found
- **Solution:** Check that downloads completed successfully. Look in `data/` directory

## Advanced Usage

### Using as a Module

```python
from src.facebook_auth import FacebookAuth
from src.facebook_fetcher import FacebookDataFetcher
from src.data_exporter import DataExporter

# Authenticate
auth = FacebookAuth()
token = auth.authenticate()
auth.save_token()

# Fetch data
fetcher = FacebookDataFetcher(token)
posts = fetcher.get_posts(limit=50)

# Export
exporter = DataExporter()
exporter.export_posts_with_comments(posts)
```

## Extending the Project

To add support for other platforms (Twitter, Reddit, YouTube):

1. Create a new module: `src/platform_auth.py`
2. Implement authentication for that platform
3. Create `src/platform_fetcher.py` for data fetching
4. Update `main.py` with platform selection

## Limitations

- Facebook API limits responses to 100 items per request
- Comments older than a certain period may not be available
- Some private accounts may have restricted data access
- Media files are referenced by URL, not downloaded directly

## Contributing

Contributions are welcome! Areas for improvement:
- Support for additional platforms
- Sentiment analysis for comments
- Export to additional formats (CSV, SQLite)
- Web interface

## License

This project is provided as-is for educational and personal use.

## Support

For issues related to:
- **Facebook API**: Check [Facebook Developers Documentation](https://developers.facebook.com/docs/)
- **This Tool**: Review the code comments or check the troubleshooting section above

## Disclaimer

This tool is designed for downloading and analyzing your own data. Ensure compliance with:
- Facebook Terms of Service
- Local data protection regulations (GDPR, CCPA, etc.)
- Privacy laws in your jurisdiction

---

**Version:** 1.0.0  
**Last Updated:** December 26, 2025

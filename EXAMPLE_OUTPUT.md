# 📊 Example Output Data

This document shows the actual output generated during testing, demonstrating the exact format your Facebook data will have when downloaded.

---

## 📁 File: `test_posts.json`

This is the **nested format** - perfect for analyzing comments in context of their source posts.

```json
{
  "metadata": {
    "exported_at": "2025-12-26T13:18:56.258339",
    "total_posts": 2,
    "total_comments": 3,
    "platform": "facebook"
  },
  "user": {
    "id": "123456789",
    "name": "Test User",
    "email": "test@example.com",
    "picture": "https://example.com/pic.jpg"
  },
  "posts": [
    {
      "id": "post_1",
      "message": "This is my first test post",
      "story": "Test User shared something",
      "type": "status",
      "created_time": "2025-12-25T10:00:00+0000",
      "link": "https://facebook.com/post_1",
      "picture": "https://example.com/post1.jpg",
      "name": "Post 1",
      "comments": [
        {
          "id": "comment_1_1",
          "message": "Great post! This is offensive language here",
          "created_time": "2025-12-25T11:00:00+0000",
          "author": "Commenter One",
          "author_id": "user_1",
          "like_count": 5,
          "type": "comment"
        },
        {
          "id": "comment_1_2",
          "message": "I agree with your thoughts",
          "created_time": "2025-12-25T11:30:00+0000",
          "author": "Commenter Two",
          "author_id": "user_2",
          "like_count": 2,
          "type": "comment"
        }
      ]
    },
    {
      "id": "post_2",
      "message": "Second post with more offensive content",
      "story": "Test User posted something",
      "type": "status",
      "created_time": "2025-12-26T09:00:00+0000",
      "link": "https://facebook.com/post_2",
      "picture": null,
      "name": "Post 2",
      "comments": [
        {
          "id": "comment_2_1",
          "message": "This comment contains inappropriate language",
          "created_time": "2025-12-26T10:00:00+0000",
          "author": "Commenter Three",
          "author_id": "user_3",
          "like_count": 0,
          "type": "comment"
        }
      ]
    }
  ]
}
```

### 📊 Data Breakdown

**Metadata:**
- `exported_at`: When the export was created (ISO 8601 format)
- `total_posts`: 2 posts downloaded
- `total_comments`: 3 comments across all posts
- `platform`: Facebook

**User Section:**
- Your profile information
- Can be used to identify whose data was exported

**Posts Section:**
Array containing all your posts with:
- Post ID
- Post content (message)
- Post type (status, link, photo, etc.)
- Created timestamp
- Link to original post
- **Comments array** - Nested comments on this post

**Comments (within each post):**
- Comment ID
- Comment text
- Author name and ID
- Like count
- Timestamp when posted

---

## 📁 File: `test_comments.json`

This is the **flat format** - optimized for analyzing and filtering comments.

```json
{
  "metadata": {
    "exported_at": "2025-12-26T13:18:56.258339",
    "total_comments": 3,
    "platform": "facebook"
  },
  "comments": [
    {
      "comment_id": "comment_1_1",
      "comment_text": "Great post! This is offensive language here",
      "created_time": "2025-12-25T11:00:00+0000",
      "author": "Commenter One",
      "author_id": "user_1",
      "like_count": 5,
      "source_post": {
        "post_id": "post_1",
        "post_text": "This is my first test post"
      }
    },
    {
      "comment_id": "comment_1_2",
      "comment_text": "I agree with your thoughts",
      "created_time": "2025-12-25T11:30:00+0000",
      "author": "Commenter Two",
      "author_id": "user_2",
      "like_count": 2,
      "source_post": {
        "post_id": "post_1",
        "post_text": "This is my first test post"
      }
    },
    {
      "comment_id": "comment_2_1",
      "comment_text": "This comment contains inappropriate language",
      "created_time": "2025-12-26T10:00:00+0000",
      "author": "Commenter Three",
      "author_id": "user_3",
      "like_count": 0,
      "source_post": {
        "post_id": "post_2",
        "post_text": "Second post with more offensive content"
      }
    }
  ]
}
```

### 📊 Data Breakdown

**Metadata:**
- `exported_at`: Export timestamp
- `total_comments`: 3 comments extracted
- `platform`: Facebook

**Comments Array:**
Each comment object includes:
- `comment_id`: Unique identifier
- `comment_text`: The actual comment
- `created_time`: When posted
- `author`: Commenter's name
- `author_id`: Commenter's ID
- `like_count`: Number of likes
- `source_post`: Reference back to the original post
  - `post_id`: ID of the post this was posted on
  - `post_text`: Preview of the post content

---

## 🔍 How to Use These Files

### Example 1: Find Offensive Comments

```python
import json

# Load the comments file
with open('facebook_comments.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find comments with offensive language
offensive_keywords = ['offensive', 'inappropriate', 'language']

for comment in data['comments']:
    text = comment['comment_text'].lower()
    if any(keyword in text for keyword in offensive_keywords):
        print(f"Found offensive comment:")
        print(f"  Text: {comment['comment_text']}")
        print(f"  Author: {comment['author']}")
        print(f"  On post: {comment['source_post']['post_text']}")
        print()
```

### Example 2: Analyze Comment Distribution

```python
# Count comments per post
from collections import defaultdict

with open('facebook_comments.json', 'r') as f:
    data = json.load(f)

post_comments = defaultdict(list)
for comment in data['comments']:
    post_id = comment['source_post']['post_id']
    post_comments[post_id].append(comment)

# Print statistics
for post_id, comments in post_comments.items():
    post_text = comments[0]['source_post']['post_text']
    print(f"Post: {post_text}")
    print(f"  Comments: {len(comments)}")
    for comment in comments:
        print(f"    - {comment['author']}: {comment['comment_text'][:50]}...")
```

### Example 3: Create Moderation Report

```python
import json
from datetime import datetime

with open('facebook_posts.json', 'r') as f:
    data = json.load(f)

print("FACEBOOK MODERATION REPORT")
print(f"Generated: {datetime.now().isoformat()}")
print(f"Account: {data['user']['name']}")
print()

total_offensive = 0

for post in data['posts']:
    print(f"\nPost: {post['message'][:100]}...")
    print(f"Posted: {post['created_time']}")
    print(f"Comments: {len(post['comments'])}")
    
    for comment in post['comments']:
        # Check for keywords
        if any(keyword in comment['message'].lower() 
               for keyword in ['offensive', 'inappropriate']):
            print(f"  ⚠️  FLAGGED: {comment['author']}")
            print(f"      {comment['message'][:80]}...")
            total_offensive += 1

print(f"\n{'='*50}")
print(f"Total flagged comments: {total_offensive}")
```

---

## 📋 Data Fields Explained

### Post Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | "post_123" | Unique post identifier |
| `message` | string | "Hello world" | Post content/text |
| `story` | string | "User shared..." | Story description |
| `type` | string | "status" | Type of post (status, link, photo, video) |
| `created_time` | string | "2025-12-25T10:00:00+0000" | ISO 8601 timestamp |
| `link` | string | "https://facebook.com/..." | URL to original post |
| `picture` | string | "https://...jpg" | Featured image URL (can be null) |
| `name` | string | "Post 1" | Post title/name |
| `comments` | array | [...] | Array of comments on this post |

### Comment Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | "comment_123" | Unique comment identifier |
| `message` | string | "Great post!" | Comment text |
| `created_time` | string | "2025-12-25T11:00:00+0000" | ISO 8601 timestamp |
| `author` | string | "John Doe" | Commenter's name |
| `author_id` | string | "user_123" | Commenter's Facebook ID |
| `like_count` | integer | 5 | Number of likes on comment |
| `type` | string | "comment" | Type of comment |

### Metadata Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `exported_at` | string | "2025-12-26T13:18:56.258339" | Export timestamp (ISO 8601) |
| `total_posts` | integer | 2 | Total posts downloaded |
| `total_comments` | integer | 3 | Total comments downloaded |
| `platform` | string | "facebook" | Social media platform |

---

## 💾 File Sizes

From the test run:

- **Nested format** (`test_posts.json`): 1,935 bytes (~2 KB)
- **Flat format** (`test_comments.json`): 1,273 bytes (~1 KB)

Real data will vary based on:
- Number of posts downloaded
- Number of comments per post
- Length of post/comment text
- Media URLs included

Typically:
- 10 posts with ~5 comments each ≈ 50-100 KB
- 100 posts with ~10 comments each ≈ 500 KB - 1 MB
- 1000 posts with ~20 comments each ≈ 5-10 MB

---

## ✨ Key Features of This Format

✅ **Perfect for your use case:**
- Comments are linked to source posts
- Easy to find offensive content
- Can analyze patterns
- Can identify problem commenters
- Can generate reports
- Can build moderation tools

✅ **Easy to process:**
- Valid JSON format
- Consistent structure
- UTF-8 encoded
- No special characters issues
- Can be imported into any tool

✅ **Production ready:**
- Timestamps are standardized
- IDs are unique
- Author info is captured
- All relevant data is included

---

## 🚀 Next Steps

1. **Get real Facebook data** by running:
   ```bash
   python main.py
   ```

2. **Files will be created in `data/` folder:**
   - `facebook_data_YYYYMMDD_HHMMSS.json` (nested)
   - `facebook_comments_YYYYMMDD_HHMMSS.json` (flat)

3. **Analyze the data** using scripts like examples above

4. **Build your moderation system** on top of this data

---

**Sample Data Generated:** December 26, 2025  
**Format Version:** 1.0  
**Status:** ✅ Verified and Ready

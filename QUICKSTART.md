# Quick Start Guide

This guide will get you up and running in 5 minutes.

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Create Facebook App (2 minutes)

1. Go to https://developers.facebook.com/
2. Create a new application (or use existing)
3. Copy your **App ID** and **App Secret** from Settings → Basic

## Step 3: Configure Environment (1 minute)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and paste your credentials:
   ```
   FACEBOOK_APP_ID=your_app_id_here
   FACEBOOK_APP_SECRET=your_app_secret_here
   ```

3. In Facebook App Dashboard:
   - Go to Settings → Basic
   - Add `http://localhost:8000/callback` to **Valid OAuth Redirect URIs**
   - Click Save Changes

## Step 4: Run the Application (1 minute)

```bash
python main.py
```

Select option **1** to authenticate with Facebook.

## Step 5: Download Your Data

Select option **2** to download posts and comments.

---

That's it! Your data will be saved in the `data/` folder as JSON files.

## Next Steps

- Read `README.md` for detailed documentation
- Check the exported JSON files in `data/` folder
- Use option 3 to export comments for analysis
- Extend the tool to support other platforms

## Common Issues

**Q: The browser doesn't open**  
A: Copy the URL from the terminal and paste in your browser manually.

**Q: Authentication fails**  
A: Make sure you added the redirect URI in Facebook App settings.

**Q: No data downloaded**  
A: Check that your Facebook app has the required permissions enabled.

For more help, see `README.md` → Troubleshooting section.

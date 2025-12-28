#!/usr/bin/env python3
"""
Facebook Data Downloader - Command Line Interface
Download posts, comments, and media from Facebook for analysis
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from facebook_auth import FacebookAuth
from facebook_fetcher import FacebookDataFetcher
from data_exporter import DataExporter


class FacebookDataDownloaderCLI:
    """Main CLI application for Facebook data downloading"""
    
    def __init__(self):
        self.auth = None
        self.fetcher = None
        self.exporter = DataExporter()
        self.token_file = 'data/token.json'
    
    def print_banner(self):
        """Print application banner"""
        print("\n" + "="*70)
        print("  Facebook Data Downloader".center(70))
        print("  Download and analyze your Facebook posts and comments".center(70))
        print("="*70)
    
    def print_menu(self):
        """Print main menu"""
        print("\n" + "-"*70)
        print("Main Menu:")
        print("-"*70)
        print("1. Authenticate with Facebook (new or refresh token)")
        print("2. Download posts and comments")
        print("3. Export comments for analysis")
        print("4. View downloaded data info")
        print("5. Exit")
        print("-"*70)
    
    def handle_authentication(self):
        """Handle Facebook authentication"""
        try:
            self.auth = FacebookAuth()
            
            # Check if token already exists
            if os.path.exists(self.token_file):
                use_existing = input("\nToken file found. Use existing token? (y/n): ").strip().lower()
                
                if use_existing == 'y':
                    token = self.auth.load_token(self.token_file)
                    if token:
                        print("✓ Token loaded successfully")
                        self.fetcher = FacebookDataFetcher(token)
                        
                        # Test connection
                        if self.auth.test_connection():
                            user_info = self.fetcher.get_user_info()
                            print(f"✓ Connected as: {user_info.get('name', 'Unknown')}")
                            return True
                        else:
                            print("✗ Token is invalid, authenticating with new token...")
            
            # Perform new authentication
            print("\nStarting new authentication flow...")
            token = self.auth.authenticate()
            
            if token:
                self.auth.save_token(self.token_file)
                self.fetcher = FacebookDataFetcher(token)
                user_info = self.fetcher.get_user_info()
                print(f"✓ Successfully authenticated as: {user_info.get('name', 'Unknown')}")
                return True
            
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            return False
    
    def handle_download(self):
        """Handle downloading posts and comments"""
        if not self.fetcher:
            print("✗ Not authenticated. Please authenticate first.")
            return
        
        try:
            # Get limit from user
            limit_input = input("\nHow many posts to download? (default: 10, max: 100): ").strip()
            limit = int(limit_input) if limit_input.isdigit() else 10
            limit = min(max(limit, 1), 100)
            
            # Fetch user info and posts
            print(f"\nFetching user information...")
            user_info = self.fetcher.get_user_info()
            print(f"✓ User: {user_info.get('name', 'Unknown')}")
            
            print(f"\nStarting download (this may take a while)...")
            posts = self.fetcher.get_posts(limit=limit)
            
            if posts:
                # Export to JSON
                filepath = self.exporter.export_posts_with_comments(posts, user_info)
                file_info = self.exporter.get_file_info(filepath)
                
                print(f"\n✓ Data successfully exported!")
                print(f"  File: {file_info['filename']}")
                print(f"  Size: {file_info['size_mb']} MB")
                print(f"  Location: {filepath}")
            else:
                print("✗ No posts found")
            
        except Exception as e:
            print(f"✗ Download failed: {e}")
    
    def handle_export_comments(self):
        """Handle exporting comments for analysis"""
        json_files = self._find_json_files()
        
        if not json_files:
            print("✗ No downloaded data files found. Please download posts first.")
            return
        
        print("\nAvailable data files:")
        for i, file in enumerate(json_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = int(input(f"\nSelect file (1-{len(json_files)}): ").strip())
            if 1 <= choice <= len(json_files):
                selected_file = json_files[choice - 1]
                
                # Load and re-export
                import json
                with open(selected_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                filepath = self.exporter.export_comments_only(data.get('posts', []))
                file_info = self.exporter.get_file_info(filepath)
                
                print(f"\n✓ Comments exported successfully!")
                print(f"  File: {file_info['filename']}")
                print(f"  Location: {filepath}")
            else:
                print("✗ Invalid selection")
        except Exception as e:
            print(f"✗ Export failed: {e}")
    
    def handle_view_info(self):
        """Show information about downloaded data"""
        json_files = self._find_json_files()
        
        if not json_files:
            print("✗ No downloaded data files found.")
            return
        
        print("\nDownloaded Data Files:")
        print("-"*70)
        
        import json
        total_posts = 0
        total_comments = 0
        
        for file in json_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = data.get('metadata', {})
                posts = metadata.get('total_posts', 0)
                comments = metadata.get('total_comments', 0)
                
                file_info = self.exporter.get_file_info(file)
                
                print(f"\nFile: {file_info['filename']}")
                print(f"  Posts: {posts}")
                print(f"  Comments: {comments}")
                print(f"  Size: {file_info['size_mb']} MB")
                
                total_posts += posts
                total_comments += comments
                
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        print("\n" + "-"*70)
        print(f"Total: {total_posts} posts, {total_comments} comments")
    
    def _find_json_files(self):
        """Find all JSON export files"""
        data_dir = Path('data')
        if data_dir.exists():
            return sorted([
                str(f) for f in data_dir.glob('facebook_data_*.json')
            ])
        return []
    
    def run(self):
        """Main CLI loop"""
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.handle_authentication()
            elif choice == '2':
                self.handle_download()
            elif choice == '3':
                self.handle_export_comments()
            elif choice == '4':
                self.handle_view_info()
            elif choice == '5':
                print("\nThank you for using Facebook Data Downloader!")
                print("Goodbye!\n")
                sys.exit(0)
            else:
                print("✗ Invalid choice. Please try again.")


def main():
    """Entry point for the application"""
    parser = argparse.ArgumentParser(
        description='Facebook Data Downloader - Download and analyze your Facebook data'
    )
    parser.add_argument(
        '--check-env',
        action='store_true',
        help='Check if environment variables are set up'
    )
    
    args = parser.parse_args()
    
    if args.check_env:
        print("Checking environment configuration...")
        from dotenv import load_dotenv
        load_dotenv()
        
        app_id = os.getenv('FACEBOOK_APP_ID')
        app_secret = os.getenv('FACEBOOK_APP_SECRET')
        
        if app_id and app_secret:
            print("✓ Environment variables are set")
            print(f"  App ID: {app_id[:10]}...")
        else:
            print("✗ Environment variables are not configured")
            print("  Please set FACEBOOK_APP_ID and FACEBOOK_APP_SECRET in .env file")
        return
    
    # Run the CLI
    cli = FacebookDataDownloaderCLI()
    cli.run()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Test script to verify the application works correctly
Simulates the download workflow without needing actual Facebook credentials
"""

import json
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_exporter import DataExporter

def test_data_exporter():
    """Test the data exporter with mock data"""
    print("\n" + "="*70)
    print("Testing Data Exporter Module".center(70))
    print("="*70)
    
    # Create mock data
    mock_user = {
        'id': '123456789',
        'name': 'Test User',
        'email': 'test@example.com',
        'picture': 'https://example.com/pic.jpg'
    }
    
    mock_posts = [
        {
            'id': 'post_1',
            'message': 'This is my first test post',
            'story': 'Test User shared something',
            'type': 'status',
            'created_time': '2025-12-25T10:00:00+0000',
            'link': 'https://facebook.com/post_1',
            'picture': 'https://example.com/post1.jpg',
            'name': 'Post 1',
            'comments': [
                {
                    'id': 'comment_1_1',
                    'message': 'Great post! This is offensive language here',
                    'created_time': '2025-12-25T11:00:00+0000',
                    'from': {
                        'name': 'Commenter One',
                        'id': 'user_1'
                    },
                    'like_count': 5,
                    'type': 'comment'
                },
                {
                    'id': 'comment_1_2',
                    'message': 'I agree with your thoughts',
                    'created_time': '2025-12-25T11:30:00+0000',
                    'from': {
                        'name': 'Commenter Two',
                        'id': 'user_2'
                    },
                    'like_count': 2,
                    'type': 'comment'
                }
            ]
        },
        {
            'id': 'post_2',
            'message': 'Second post with more offensive content',
            'story': 'Test User posted something',
            'type': 'status',
            'created_time': '2025-12-26T09:00:00+0000',
            'link': 'https://facebook.com/post_2',
            'picture': None,
            'name': 'Post 2',
            'comments': [
                {
                    'id': 'comment_2_1',
                    'message': 'This comment contains inappropriate language',
                    'created_time': '2025-12-26T10:00:00+0000',
                    'from': {
                        'name': 'Commenter Three',
                        'id': 'user_3'
                    },
                    'like_count': 0,
                    'type': 'comment'
                }
            ]
        }
    ]
    
    # Test 1: Export nested posts with comments
    print("\n✓ Test 1: Exporting posts with nested comments...")
    try:
        exporter = DataExporter()
        filepath = exporter.export_posts_with_comments(
            mock_posts, 
            mock_user, 
            filename='test_posts.json'
        )
        
        # Verify file exists and contains correct data
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data['metadata']['total_posts'] == 2, "Wrong post count"
        assert data['metadata']['total_comments'] == 3, "Wrong comment count"
        assert len(data['posts']) == 2, "Posts not properly saved"
        assert len(data['posts'][0]['comments']) == 2, "Comments not nested properly"
        
        file_info = exporter.get_file_info(filepath)
        print(f"  ✓ File created: {file_info['filename']}")
        print(f"  ✓ File size: {file_info['size_mb']} MB")
        print(f"  ✓ Posts: {data['metadata']['total_posts']}")
        print(f"  ✓ Comments: {data['metadata']['total_comments']}")
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False
    
    # Test 2: Export comments only
    print("\n✓ Test 2: Exporting comments for analysis...")
    try:
        filepath = exporter.export_comments_only(mock_posts, filename='test_comments.json')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data['metadata']['total_comments'] == 3, "Wrong comment count"
        assert len(data['comments']) == 3, "Comments not properly exported"
        assert 'source_post' in data['comments'][0], "Source post not linked"
        
        print(f"  ✓ File created: {data['metadata'].get('total_comments')} comments exported")
        print(f"  ✓ Each comment linked to source post")
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False
    
    # Test 3: Verify file structure
    print("\n✓ Test 3: Verifying nested JSON structure...")
    try:
        with open('data/test_posts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check metadata
        assert 'metadata' in data, "Missing metadata"
        assert 'user' in data, "Missing user"
        assert 'posts' in data, "Missing posts"
        
        # Check post structure
        post = data['posts'][0]
        assert 'id' in post, "Missing post id"
        assert 'message' in post, "Missing post message"
        assert 'comments' in post, "Missing comments in post"
        
        # Check comment structure
        comment = post['comments'][0]
        assert 'id' in comment, "Missing comment id"
        assert 'message' in comment, "Missing comment message"
        assert 'author' in comment, "Missing comment author"
        assert 'created_time' in comment, "Missing comment timestamp"
        
        print("  ✓ Metadata structure: ✓")
        print("  ✓ User information: ✓")
        print("  ✓ Posts structure: ✓")
        print("  ✓ Nested comments: ✓")
        print("  ✓ Comment details: ✓")
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False
    
    return True


def test_imports():
    """Test that all modules can be imported correctly"""
    print("\n" + "="*70)
    print("Testing Module Imports".center(70))
    print("="*70)
    
    try:
        print("\n✓ Importing facebook_auth...")
        from facebook_auth import FacebookAuth
        print("  ✓ FacebookAuth class found")
        
        print("\n✓ Importing facebook_fetcher...")
        from facebook_fetcher import FacebookDataFetcher
        print("  ✓ FacebookDataFetcher class found")
        
        print("\n✓ Importing data_exporter...")
        from data_exporter import DataExporter
        print("  ✓ DataExporter class found")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_cli_startup():
    """Test that the CLI can start up without errors"""
    print("\n" + "="*70)
    print("Testing CLI Module".center(70))
    print("="*70)
    
    try:
        print("\n✓ Checking main.py can be loaded...")
        
        # Check main.py exists
        main_file = Path('main.py')
        assert main_file.exists(), "main.py not found"
        print("  ✓ main.py found")
        
        # Check syntax
        with open('main.py', 'r') as f:
            content = f.read()
            compile(content, 'main.py', 'exec')
        print("  ✓ main.py syntax valid")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_environment():
    """Test environment setup"""
    print("\n" + "="*70)
    print("Testing Environment Setup".center(70))
    print("="*70)
    
    try:
        print("\n✓ Checking Python version...")
        import sys
        version = sys.version_info
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        
        print("\n✓ Checking required packages...")
        import requests
        print(f"  ✓ requests {requests.__version__}")
        
        from dotenv import load_dotenv
        print(f"  ✓ python-dotenv installed")
        
        print("\n✓ Checking project structure...")
        required_dirs = ['src', 'data']
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            assert dir_path.exists(), f"{dir_name} directory not found"
            print(f"  ✓ {dir_name}/ directory found")
        
        required_files = ['main.py', 'requirements.txt', 'README.md']
        for file_name in required_files:
            file_path = Path(file_name)
            assert file_path.exists(), f"{file_name} not found"
            print(f"  ✓ {file_name} found")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("Facebook Data Downloader - Application Tests".center(70))
    print("="*70)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Module Imports", test_imports),
        ("CLI Module", test_cli_startup),
        ("Data Exporter", test_data_exporter),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary".center(70))
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} | {test_name}")
    
    print("-" * 70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Application is ready to use.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your Facebook App ID and Secret to .env")
        print("3. Run: python main.py")
        return True
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

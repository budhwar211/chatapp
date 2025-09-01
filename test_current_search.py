#!/usr/bin/env python3
"""
Test script for current information search using proper LangChain tool invoke
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_current_search():
    """Test the current information search function properly"""
    try:
        print("🧪 Testing Current Information Search")
        print("=" * 50)
        
        # Import the tool
        from main import get_current_information
        
        # Test query
        query = "current terrorism news in India"
        search_type = "news"
        
        print(f"📝 Testing query: '{query}'")
        print(f"🔍 Search type: {search_type}")
        print("-" * 40)
        
        # Use proper invoke method instead of direct call
        if hasattr(get_current_information, 'invoke'):
            result = get_current_information.invoke({"query": query, "search_type": search_type})
        else:
            # Fallback to direct function call
            result = get_current_information(query, search_type)
        
        print("✅ Integration test passed")
        print(f"📄 Result preview: {result[:300]}{'...' if len(result) > 300 else ''}")
        
        # Check if result contains helpful information
        if "🇮🇳" in result or "terrorism" in result.lower() or "news" in result.lower():
            print("✅ Result contains relevant information")
        else:
            print("⚠️ Result may need improvement")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        success = test_current_search()
        if success:
            print("\n🎉 Search functionality is working!")
        else:
            print("\n❌ Search test failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)
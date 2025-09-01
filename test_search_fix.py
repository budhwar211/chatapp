#!/usr/bin/env python3
"""
Test script to verify the enhanced search_web function
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the parent directory to sys.path to import from main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_search_web():
    """Test the enhanced search_web function with various queries"""
    try:
        # Import the search_web function from main.py
        from main import search_web
        
        # Test queries that previously failed
        test_queries = [
            "latest AI news",
            "current terrorism news in India", 
            "What time is it in Tokyo?",
            "weather in New York",
            "python programming tutorial",
            "artificial intelligence",  # This might have Wikipedia content
            "how to bake a cake",
            "breaking news today"
        ]
        
        print("🧪 Testing Enhanced Web Search Function")
        print("=" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Testing query: '{query}'")
            print("-" * 40)
            
            try:
                result = search_web(query)
                print(f"✅ Result: {result[:200]}{'...' if len(result) > 200 else ''}")
                
                # Check if we got a meaningful result (not just "No results found")
                if "No quick answer found" in result or "Search failed" in result:
                    print("⚠️  Got fallback response - this is expected for news queries")
                else:
                    print("✅ Got meaningful search result!")
                    
            except Exception as e:
                print(f"❌ Error testing query '{query}': {e}")
            
            print()
        
        print("🎉 Search function testing completed!")
        
    except ImportError as e:
        print(f"❌ Failed to import search_web function: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during testing: {e}")

if __name__ == "__main__":
    test_search_web()
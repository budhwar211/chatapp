#!/usr/bin/env python3
"""
Test script for MCP Web Search Server
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_mcp_server():
    """Test the MCP web search server"""
    try:
        print("🧪 Testing MCP Web Search Server")
        print("=" * 50)
        
        # Import the server class
        from mcp_web_search_server import WebSearchMCPServer
        
        # Create server instance
        server = WebSearchMCPServer()
        print("✅ Server instance created successfully")
        
        # Test rate limiting
        print("\n🔒 Testing rate limiting...")
        rate_check1 = server._check_rate_limit()
        rate_check2 = server._check_rate_limit()
        print(f"Rate limit check 1: {rate_check1}")
        print(f"Rate limit check 2: {rate_check2}")
        
        # Test search functions
        test_queries = [
            ("terrorism news India", "news"),
            ("latest AI technology", "comprehensive"),
            ("breaking news today", "realtime")
        ]
        
        print("\n🔍 Testing search functions...")
        for query, search_type in test_queries:
            print(f"\n📝 Testing: '{query}' (type: {search_type})")
            
            if search_type == "news":
                result = await server._search_news({"query": query, "country": "in"})
            elif search_type == "comprehensive":
                result = await server._search_web_comprehensive({"query": query, "result_count": 3})
            else:
                result = await server._search_realtime({"query": query, "time_range": "past_day"})
            
            print(f"✅ Result length: {len(result) if result else 0} characters")
            if result:
                print(f"📄 Preview: {result[:150]}{'...' if len(result) > 150 else ''}")
            else:
                print("⚠️ No result returned")
        
        print("\n🎉 MCP Web Search Server test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import MCP server: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_mcp_server())
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)
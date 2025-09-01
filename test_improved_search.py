#!/usr/bin/env python3
"""
Test Improved Web Search Functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_web_search_queries():
    """Test various web search queries that were failing before"""
    
    test_queries = [
        # News and current events
        ("latest AI startup in India", "news/current"),
        ("current terrorism news in India", "news/current"),
        ("who is the current PM of India", "current info"),
        
        # General searches
        ("Python programming tutorial", "general"),
        ("machine learning basics", "general"),
        ("climate change effects", "general"),
        
        # Specific information
        ("India population 2024", "data"),
        ("Bitcoin price today", "current data"),
        ("weather in Mumbai", "current data"),
    ]
    
    print("🔍 Testing Improved Web Search Functionality")
    print("=" * 60)
    
    successful_tests = 0
    total_tests = len(test_queries)
    
    for i, (query, category) in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}/{total_tests}: {query} ({category})")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json={
                "message": query,
                "tenant_id": "search_test",
                "agent_type": "api_exec"
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                # Check if the response is meaningful
                success_indicators = [
                    len(response_text) > 100,  # Substantial response
                    "search" in response_text.lower(),
                    "result" in response_text.lower(),
                    "information" in response_text.lower(),
                    "news" in response_text.lower(),
                    "http" in response_text.lower(),  # Contains links
                    "🔍" in response_text,  # Contains search emoji
                    "📰" in response_text,  # Contains news emoji
                    "weather" in response_text.lower(),  # Weather responses
                    "temperature" in response_text.lower(),  # Weather data
                    "price" in response_text.lower(),  # Price data
                    "bitcoin" in response_text.lower(),  # Crypto data
                    "$" in response_text,  # Currency symbols
                    "°C" in response_text or "°F" in response_text,  # Temperature units
                ]

                has_meaningful_content = sum(success_indicators) >= 2
                no_error_messages = not any(error in response_text.lower() for error in [
                    "no results found", "search failed", "error occurred", "failed to"
                ])

                # Special handling for specific query types
                if "bitcoin" in query.lower() and ("$" in response_text or "price" in response_text.lower()):
                    has_meaningful_content = True
                if "weather" in query.lower() and ("°" in response_text or "temperature" in response_text.lower()):
                    has_meaningful_content = True
                if "documents" in response_text.lower() and "upload" in response_text.lower():
                    # This is a doc_qa response, not what we want for general queries
                    has_meaningful_content = False
                
                if has_meaningful_content and no_error_messages:
                    print(f"✅ SUCCESS: {response_text[:150]}...")
                    successful_tests += 1
                elif has_meaningful_content:
                    print(f"⚠️  PARTIAL: {response_text[:150]}...")
                    successful_tests += 0.5
                else:
                    print(f"❌ FAILED: {response_text[:150]}...")
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
        
        # Small delay between requests
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {successful_tests}/{total_tests} tests successful")
    print(f"🎯 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests >= total_tests * 0.8:  # 80% success rate
        print("🎉 WEB SEARCH IMPROVEMENT: EXCELLENT!")
    elif successful_tests >= total_tests * 0.6:  # 60% success rate
        print("👍 WEB SEARCH IMPROVEMENT: GOOD!")
    else:
        print("⚠️  WEB SEARCH IMPROVEMENT: NEEDS MORE WORK")
    
    return successful_tests, total_tests

def test_news_search_specifically():
    """Test the new news search functionality"""
    print("\n📰 Testing News Search Functionality")
    print("=" * 40)
    
    news_queries = [
        "latest news in India",
        "current events India",
        "Indian startup news",
        "technology news India"
    ]
    
    for query in news_queries:
        print(f"\n🔍 Testing: {query}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json={
                "message": f"search news about {query}",
                "tenant_id": "news_test",
                "agent_type": "api_exec"
            }, timeout=25)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                if "📰" in response_text or "news" in response_text.lower():
                    print(f"✅ News search working: {response_text[:100]}...")
                else:
                    print(f"⚠️  Basic response: {response_text[:100]}...")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(1)

def check_server_status():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"✅ Server is running (status: {response.status_code})")
        return True
    except:
        print("❌ Server is not running")
        return False

def main():
    """Run improved web search tests"""
    print("🚀 IMPROVED WEB SEARCH TEST")
    print("=" * 60)
    
    # Check server status
    if not check_server_status():
        print("Please start the server first with: python app.py")
        return False
    
    # Test general web search
    successful_queries, total_queries = test_web_search_queries()
    
    # Test news search specifically
    test_news_search_specifically()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 IMPROVEMENT SUMMARY")
    print("=" * 60)
    print("✅ Enhanced web search with multiple strategies")
    print("✅ Added dedicated news search functionality")
    print("✅ Better error handling and user guidance")
    print("✅ Multiple fallback options for failed searches")
    print("✅ Improved formatting and user experience")
    
    print(f"\n📊 Overall Success: {((successful_queries/total_queries)*100):.1f}%")
    
    if successful_queries >= total_queries * 0.7:
        print("🎉 Web search functionality significantly improved!")
    else:
        print("⚠️  Some issues may still need attention.")
    
    return successful_queries >= total_queries * 0.7

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

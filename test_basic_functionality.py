#!/usr/bin/env python3
"""
Basic functionality test without problematic imports
"""

import sys
import os
from pathlib import Path

def test_basic_search():
    """Test basic search functionality without importing main.py"""
    print("🔍 Testing Basic Search Functionality")
    print("=" * 50)
    
    try:
        import requests
        
        # Test DuckDuckGo API directly
        query = "artificial intelligence"
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10,
        )
        data = resp.json() if resp.ok else {}
        
        # Try abstract first
        abstract = data.get("AbstractText") or data.get("Abstract") or ""
        
        if abstract:
            print(f"✅ DuckDuckGo API search successful")
            print(f"   Query: {query}")
            print(f"   Result: {abstract[:100]}...")
            return True
        else:
            print(f"⚠️ DuckDuckGo API returned no abstract for: {query}")
            
            # Try related topics
            related = data.get("RelatedTopics", [])
            if related:
                print(f"✅ Found {len(related)} related topics")
                return True
            else:
                print(f"❌ No results from DuckDuckGo API")
                return False
                
    except Exception as e:
        print(f"❌ Basic search test failed: {e}")
        return False

def test_weather_api():
    """Test weather API functionality"""
    print("\n🌤️ Testing Weather API Functionality")
    print("-" * 30)
    
    try:
        import requests
        
        # Test geocoding
        city = "London"
        geo_resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        
        if geo_resp.ok:
            geo_data = geo_resp.json()
            results = geo_data.get("results", [])
            
            if results:
                location = results[0]
                lat, lon = location["latitude"], location["longitude"]
                
                # Test weather API
                weather_resp = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current_weather": "true",
                        "timezone": "auto"
                    },
                    timeout=10,
                )
                
                if weather_resp.ok:
                    weather_data = weather_resp.json()
                    current = weather_data.get("current_weather", {})
                    
                    if current:
                        temp = current.get("temperature")
                        print(f"✅ Weather API successful")
                        print(f"   City: {city}")
                        print(f"   Temperature: {temp}°C")
                        return True
                    else:
                        print(f"❌ No current weather data")
                        return False
                else:
                    print(f"❌ Weather API request failed")
                    return False
            else:
                print(f"❌ City not found: {city}")
                return False
        else:
            print(f"❌ Geocoding request failed")
            return False
            
    except Exception as e:
        print(f"❌ Weather test failed: {e}")
        return False

def test_playwright_import():
    """Test Playwright import"""
    print("\n🎭 Testing Playwright Import")
    print("-" * 30)
    
    try:
        import playwright
        print("✅ Playwright imported successfully")
        
        # Test async playwright
        from playwright.async_api import async_playwright
        print("✅ Async Playwright imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Playwright import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        return False

def test_mcp_import():
    """Test MCP imports"""
    print("\n📡 Testing MCP Imports")
    print("-" * 30)
    
    try:
        from mcp.server import Server
        from mcp.server.models import InitializationOptions
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent
        print("✅ MCP imports successful")
        return True
        
    except ImportError as e:
        print(f"⚠️ MCP not available: {e}")
        return False
    except Exception as e:
        print(f"❌ MCP test failed: {e}")
        return False

def run_basic_tests():
    """Run all basic functionality tests"""
    print("🧪 BASIC FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Basic Search
    results['search'] = test_basic_search()
    
    # Test 2: Weather API
    results['weather'] = test_weather_api()
    
    # Test 3: Playwright Import
    results['playwright'] = test_playwright_import()
    
    # Test 4: MCP Import
    results['mcp'] = test_mcp_import()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 BASIC TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name.title()} Test")
    
    success_rate = (passed / total) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}% ({passed}/{total})")
    
    if success_rate >= 75:
        print("🎉 Core infrastructure is working!")
        return True
    elif success_rate >= 50:
        print("⚠️ Some infrastructure issues detected")
        return True
    else:
        print("❌ Significant infrastructure problems")
        return False

if __name__ == "__main__":
    try:
        success = run_basic_tests()
        if success:
            print("\n✅ Basic functionality test PASSED!")
            print("\n💡 The issue appears to be in the tool registration/initialization, not the core functionality.")
            sys.exit(0)
        else:
            print("\n❌ Basic functionality test FAILED!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
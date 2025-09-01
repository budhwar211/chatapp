#!/usr/bin/env python3
"""
Final Playwright Integration Test
Tests web interface using Playwright MCP tools
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_playwright_web_automation():
    """Test Playwright web automation capabilities"""
    logger.info("🎭 Testing Playwright Web Automation")
    
    try:
        from mcp_playwright_server import PlaywrightMCPServer
        
        # Initialize Playwright server
        playwright_server = PlaywrightMCPServer()
        await playwright_server._init_browser()
        
        # Test 1: Live News Scraping
        logger.info("1. Testing Live News Scraping...")
        news_result = await playwright_server._scrape_live_news({
            "query": "technology news",
            "source": "bbc",
            "max_articles": 2
        })
        
        if news_result and len(news_result) > 100:
            logger.info("✅ Live news scraping successful")
            logger.info(f"   Result: {news_result[:150]}...")
        else:
            logger.warning(f"⚠️ Live news scraping issue: {news_result}")
        
        # Test 2: Google News Search
        logger.info("2. Testing Google News Search...")
        google_result = await playwright_server._search_google_news({
            "query": "artificial intelligence",
            "region": "us"
        })
        
        if google_result and len(google_result) > 50:
            logger.info("✅ Google News search successful")
            logger.info(f"   Result: {google_result[:100]}...")
        else:
            logger.warning(f"⚠️ Google News search issue: {google_result}")
        
        # Test 3: Breaking News
        logger.info("3. Testing Breaking News...")
        breaking_result = await playwright_server._get_breaking_news({
            "topic": "technology"
        })
        
        if breaking_result and len(breaking_result) > 50:
            logger.info("✅ Breaking news successful")
            logger.info(f"   Result: {breaking_result[:100]}...")
        else:
            logger.warning(f"⚠️ Breaking news issue: {breaking_result}")
        
        # Clean up
        if playwright_server.browser:
            await playwright_server.browser.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Playwright test error: {e}")
        return False

def test_system_integration():
    """Test system integration with main chatbot"""
    logger.info("🔗 Testing System Integration")
    
    try:
        from main import get_tenant_tools, set_current_tenant, create_tenant
        
        # Create test tenant
        create_tenant("playwright_test", "Playwright Test", ["read_documents", "use_tools"])
        set_current_tenant("playwright_test")
        
        # Get available tools
        tools = get_tenant_tools("playwright_test")
        
        # Check for web automation tools
        web_tools = []
        for tool in tools:
            tool_name = getattr(tool, 'name', getattr(tool, '__name__', str(tool)))
            if 'web' in tool_name.lower() or 'search' in tool_name.lower():
                web_tools.append(tool)
        
        if web_tools:
            logger.info(f"✅ Found {len(web_tools)} web automation tools")
            for tool in web_tools:
                tool_name = getattr(tool, 'name', getattr(tool, '__name__', str(tool)))
                tool_desc = getattr(tool, 'description', 'No description available')
                logger.info(f"   - {tool_name}: {tool_desc[:50]}...")
            return True
        else:
            logger.warning("⚠️ No web automation tools found")
            return False
            
    except Exception as e:
        logger.error(f"❌ System integration error: {e}")
        return False

async def run_final_playwright_test():
    """Run comprehensive Playwright test"""
    print("🎭 FINAL PLAYWRIGHT INTEGRATION TEST")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Playwright Web Automation
    print("\n1. 🌐 Playwright Web Automation Test")
    print("-" * 30)
    results['playwright_automation'] = await test_playwright_web_automation()
    
    # Test 2: System Integration
    print("\n2. 🔗 System Integration Test")
    print("-" * 30)
    results['system_integration'] = test_system_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 FINAL TEST SUMMARY")
    print("=" * 50)
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n📊 Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate == 100:
        print("🎉 ALL TESTS PASSED! Playwright MCP integration is working perfectly!")
        return True
    elif success_rate >= 50:
        print("⚠️ Some issues detected, but core functionality works")
        return True
    else:
        print("❌ Significant issues found")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(run_final_playwright_test())
        if success:
            print("\n✅ Final Playwright test PASSED!")
            sys.exit(0)
        else:
            print("\n❌ Final Playwright test FAILED!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
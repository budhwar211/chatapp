#!/usr/bin/env python3
"""
API Executor Functionality Test
Tests web search, date/time, and other API tools
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    node_api_exec, create_tenant, create_session, MessagesState,
    CURRENT_TENANT_ID, CURRENT_SESSION, set_current_tenant,
    get_tenant_tools, build_llm_with_tools_for_tenant
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api_executor_node():
    """Test the API executor node functionality"""
    logger.info("Testing API Executor Node")
    
    global CURRENT_TENANT_ID, CURRENT_SESSION
    original_tenant = CURRENT_TENANT_ID
    original_session = CURRENT_SESSION
    
    try:
        # Set up test context
        tenant_id = "test_api_exec"
        
        # Create tenant and session
        create_tenant(tenant_id, "API Test Tenant", ["read_documents", "use_tools", "generate_forms"])
        set_current_tenant(tenant_id)
        
        test_queries = [
            "Search the web for current news about AI",
            "What's the current date and time?",
            "Get weather information for New York",
            "Search for information about Python programming",
            "What time is it now?"
        ]
        
        results = {}
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"Testing API executor query {i}: '{query}'")
            
            try:
                # Create message state
                state = MessagesState(messages=[("user", query)])
                
                # Run API executor node
                result = node_api_exec(state)
                
                if result and 'messages' in result:
                    response_msg = result['messages'][0]
                    if hasattr(response_msg, 'content'):
                        response = response_msg.content
                    elif isinstance(response_msg, tuple) and len(response_msg) >= 2:
                        response = response_msg[1]
                    else:
                        response = str(response_msg)
                    
                    # Check if API execution was successful
                    success = not (
                        "error" in response.lower() or
                        "failed" in response.lower() or
                        "not available" in response.lower() or
                        "permission denied" in response.lower()
                    )
                    
                    results[f"query_{i}"] = {
                        'query': query,
                        'response': response,
                        'success': success,
                        'has_data': len(response) > 100,
                        'response_length': len(response)
                    }
                    
                    if success:
                        logger.info(f"✅ API execution successful for query {i}")
                        logger.info(f"   Response: {response[:150]}...")
                    else:
                        logger.warning(f"⚠️ API execution may have issues for query {i}")
                        logger.info(f"   Response: {response[:200]}...")
                else:
                    logger.error(f"❌ API execution failed for query {i} - no response")
                    results[f"query_{i}"] = {
                        'query': query,
                        'success': False,
                        'error': 'No response from API execution node'
                    }
                    
            except Exception as e:
                logger.error(f"❌ API execution error for query {i}: {e}")
                results[f"query_{i}"] = {
                    'query': query,
                    'success': False,
                    'error': str(e)
                }
        
        return results
        
    finally:
        # Restore context
        CURRENT_TENANT_ID = original_tenant
        CURRENT_SESSION = original_session

def test_tenant_tools():
    """Test tenant tools availability"""
    logger.info("Testing Tenant Tools Availability")
    
    try:
        # Set up test context
        tenant_id = "test_tools"
        create_tenant(tenant_id, "Tools Test Tenant", ["read_documents", "use_tools", "generate_forms"])
        set_current_tenant(tenant_id)
        
        # Get available tools
        tools = get_tenant_tools(tenant_id)
        
        # Handle both function tools and StructuredTool objects
        tool_names = []
        for tool in tools:
            tool_name = getattr(tool, 'name', getattr(tool, '__name__', str(tool)))
            tool_names.append(tool_name)
            
        has_web_search = any('search' in tool_name.lower() for tool_name in tool_names) if tool_names else False
        has_date_time = any('date' in tool_name.lower() or 'time' in tool_name.lower() for tool_name in tool_names) if tool_names else False
        has_weather = any('weather' in tool_name.lower() for tool_name in tool_names) if tool_names else False
        
        results = {
            'tools_available': len(tools) > 0,
            'tools_count': len(tools),
            'tool_names': tool_names,
            'has_web_search': has_web_search,
            'has_date_time': has_date_time,
            'has_weather': has_weather
        }
        
        logger.info(f"✅ Tools test results: {results}")
        return results
        
    except Exception as e:
        logger.error(f"❌ Tools test error: {e}")
        return {'error': str(e)}

def test_llm_with_tools():
    """Test LLM with tools binding"""
    logger.info("Testing LLM with Tools")
    
    try:
        # Set up test context
        tenant_id = "test_llm_tools"
        create_tenant(tenant_id, "LLM Tools Test Tenant", ["read_documents", "use_tools", "generate_forms"])
        set_current_tenant(tenant_id)
        
        # Build LLM with tools
        llm_with_tools = build_llm_with_tools_for_tenant(tenant_id)
        
        results = {
            'llm_created': llm_with_tools is not None,
            'has_bind_tools': hasattr(llm_with_tools, 'bind_tools') or hasattr(llm_with_tools, 'bind'),
            'llm_type': type(llm_with_tools).__name__ if llm_with_tools else None
        }
        
        # Test a simple tool invocation
        if llm_with_tools:
            try:
                # Simple test message
                response = llm_with_tools.invoke([("user", "What time is it?")])
                results['simple_invocation'] = True
                results['has_tool_calls'] = hasattr(response, 'tool_calls') and response.tool_calls is not None
            except Exception as e:
                logger.warning(f"Simple invocation failed: {e}")
                results['simple_invocation'] = False
                results['invocation_error'] = str(e)
        
        logger.info(f"✅ LLM with tools test results: {results}")
        return results
        
    except Exception as e:
        logger.error(f"❌ LLM with tools test error: {e}")
        return {'error': str(e)}

def test_mcp_servers():
    """Test MCP server connectivity"""
    logger.info("Testing MCP Server Connectivity")
    
    try:
        from main import MCP_AVAILABLE, _active_mcp_servers, _mcp_server_registry
        
        results = {
            'mcp_available': MCP_AVAILABLE,
            'active_servers': len(_active_mcp_servers) if _active_mcp_servers else 0,
            'registered_servers': len(_mcp_server_registry) if _mcp_server_registry else 0,
            'server_names': list(_mcp_server_registry.keys()) if _mcp_server_registry else []
        }
        
        # Test specific servers
        if _active_mcp_servers:
            for server_name, server_info in _active_mcp_servers.items():
                results[f'{server_name}_active'] = server_info is not None
        
        logger.info(f"✅ MCP servers test results: {results}")
        return results
        
    except Exception as e:
        logger.error(f"❌ MCP servers test error: {e}")
        return {'error': str(e)}

def test_web_search_functionality():
    """Test web search functionality specifically"""
    logger.info("Testing Web Search Functionality")
    
    try:
        # Set up test context
        tenant_id = "test_web_search"
        create_tenant(tenant_id, "Web Search Test Tenant", ["read_documents", "use_tools", "generate_forms"])
        set_current_tenant(tenant_id)
        
        # Test direct web search queries
        search_queries = [
            "Python programming tutorial",
            "Current weather in New York",
            "Latest news AI technology",
            "How to install Python packages"
        ]
        
        results = {}
        
        for i, query in enumerate(search_queries, 1):
            logger.info(f"Testing web search: '{query}'")
            
            try:
                # Create a specific web search message
                search_message = f"Search the web for: {query}"
                state = MessagesState(messages=[("user", search_message)])
                
                result = node_api_exec(state)
                
                if result and 'messages' in result:
                    response_msg = result['messages'][0]
                    if hasattr(response_msg, 'content'):
                        response = response_msg.content
                    elif isinstance(response_msg, tuple) and len(response_msg) >= 2:
                        response = response_msg[1]
                    else:
                        response = str(response_msg)
                    
                    # Check for web search indicators
                    search_success = any(indicator in response.lower() for indicator in [
                        'search results', 'found', 'according to', 'based on search',
                        'web search', 'internet', 'online', 'website', 'sources'
                    ])
                    
                    results[f"search_{i}"] = {
                        'query': query,
                        'response': response,
                        'success': search_success,
                        'has_results': len(response) > 50,
                        'response_length': len(response)
                    }
                    
                    if search_success:
                        logger.info(f"✅ Web search successful for: '{query}'")
                    else:
                        logger.warning(f"⚠️ Web search may have failed for: '{query}'")
                        logger.info(f"   Response: {response[:200]}...")
                        
                else:
                    results[f"search_{i}"] = {
                        'query': query,
                        'success': False,
                        'error': 'No response from web search'
                    }
                    
            except Exception as e:
                logger.error(f"❌ Web search error for '{query}': {e}")
                results[f"search_{i}"] = {
                    'query': query,
                    'success': False,
                    'error': str(e)
                }
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Web search functionality test error: {e}")
        return {'error': str(e)}

def run_comprehensive_api_test():
    """Run comprehensive API executor test suite"""
    logger.info("🧪 Starting Comprehensive API Executor Test Suite")
    logger.info("=" * 60)
    
    all_results = {}
    
    # Test 1: API Executor Node
    logger.info("\n🔧 Testing API Executor Node")
    logger.info("-" * 40)
    all_results['node_tests'] = test_api_executor_node()
    
    # Test 2: Tenant Tools
    logger.info("\n🛠️ Testing Tenant Tools")
    logger.info("-" * 40)
    all_results['tools_tests'] = test_tenant_tools()
    
    # Test 3: LLM with Tools
    logger.info("\n🤖 Testing LLM with Tools")
    logger.info("-" * 40)
    all_results['llm_tests'] = test_llm_with_tools()
    
    # Test 4: MCP Servers
    logger.info("\n📡 Testing MCP Servers")
    logger.info("-" * 40)
    all_results['mcp_tests'] = test_mcp_servers()
    
    # Test 5: Web Search Functionality
    logger.info("\n🔍 Testing Web Search Functionality")
    logger.info("-" * 40)
    all_results['search_tests'] = test_web_search_functionality()
    
    # Calculate summary
    logger.info("\n" + "=" * 60)
    logger.info("🎯 API EXECUTOR TEST SUMMARY")
    logger.info("=" * 60)
    
    total_tests = 0
    successful_tests = 0
    
    # Count node tests
    if 'node_tests' in all_results:
        node_success = sum(1 for test in all_results['node_tests'].values() if test.get('success', False))
        node_total = len(all_results['node_tests'])
        logger.info(f"🔧 API Executor Node: {node_success}/{node_total} successful")
        total_tests += node_total
        successful_tests += node_success
    
    # Count tools tests
    if 'tools_tests' in all_results and 'error' not in all_results['tools_tests']:
        tools_success = sum(1 for v in all_results['tools_tests'].values() if v is True)
        tools_total = len(all_results['tools_tests'])
        logger.info(f"🛠️ Tenant Tools: {tools_success}/{tools_total} tests passed")
        total_tests += tools_total
        successful_tests += tools_success
    
    # Count LLM tests
    if 'llm_tests' in all_results and 'error' not in all_results['llm_tests']:
        llm_success = sum(1 for v in all_results['llm_tests'].values() if v is True)
        llm_total = len(all_results['llm_tests'])
        logger.info(f"🤖 LLM with Tools: {llm_success}/{llm_total} tests passed")
        total_tests += llm_total
        successful_tests += llm_success
    
    # Count MCP tests
    if 'mcp_tests' in all_results and 'error' not in all_results['mcp_tests']:
        mcp_success = sum(1 for v in all_results['mcp_tests'].values() if v is True)
        mcp_total = len(all_results['mcp_tests'])
        logger.info(f"📡 MCP Servers: {mcp_success}/{mcp_total} tests passed")
        total_tests += mcp_total
        successful_tests += mcp_success
    
    # Count search tests
    if 'search_tests' in all_results and 'error' not in all_results['search_tests']:
        search_success = sum(1 for test in all_results['search_tests'].values() if test.get('success', False))
        search_total = len(all_results['search_tests'])
        logger.info(f"🔍 Web Search: {search_success}/{search_total} tests passed")
        total_tests += search_total
        successful_tests += search_success
    
    # Overall assessment
    if total_tests > 0:
        success_rate = (successful_tests / total_tests) * 100
        logger.info(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        
        if success_rate >= 80:
            logger.info("🎉 API executor system is working well!")
        elif success_rate >= 60:
            logger.info("⚠️ API executor system needs some improvements")
        else:
            logger.info("❌ API executor system has significant issues")
            
        return success_rate >= 80
    else:
        logger.error("❌ No tests were able to run properly")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_api_test()
        if success:
            print("\n✅ API executor test suite passed!")
            sys.exit(0)
        else:
            print("\n❌ API executor test suite failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
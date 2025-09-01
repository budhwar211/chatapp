#!/usr/bin/env python3
"""
Analytics System Test
Tests system statistics display and formatting functionality
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    node_analytics, create_tenant, create_session, MessagesState,
    CURRENT_TENANT_ID, CURRENT_SESSION, set_current_tenant,
    get_system_stats, get_tool_stats, _tenant_registry,
    _active_sessions, _tool_call_counts, _tool_error_counts
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_system_stats():
    """Test system statistics functionality"""
    logger.info("Testing System Statistics Function")
    
    try:
        # Get system stats
        stats = get_system_stats()
        
        logger.info(f"✅ System stats retrieved successfully")
        logger.info(f"   Stats keys: {list(stats.keys())}")
        
        # Validate stats structure
        expected_keys = ['tenants', 'sessions', 'tools']
        missing_keys = [key for key in expected_keys if key not in stats]
        
        if missing_keys:
            logger.error(f"❌ Missing expected keys: {missing_keys}")
            return False
        
        # Check tenant stats
        tenant_stats = stats.get('tenants', {})
        logger.info(f"   Tenant stats: {tenant_stats}")
        
        # Check session stats
        session_stats = stats.get('sessions', {})
        logger.info(f"   Session stats: {session_stats}")
        
        # Check tool stats
        tool_stats = stats.get('tools', {})
        logger.info(f"   Tool stats count: {len(tool_stats)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ System stats test error: {e}")
        return False

def test_tool_stats():
    """Test tool statistics functionality"""
    logger.info("Testing Tool Statistics Function")
    
    try:
        # Simulate some tool usage
        _tool_call_counts['search_web'] = 10
        _tool_call_counts['get_weather'] = 5
        _tool_error_counts['search_web'] = 1
        _tool_error_counts['get_weather'] = 0
        
        # Get tool stats
        tool_stats = get_tool_stats()
        
        logger.info(f"✅ Tool stats retrieved successfully")
        logger.info(f"   Tools tracked: {list(tool_stats.keys())}")
        
        # Validate structure
        if 'search_web' in tool_stats:
            search_stats = tool_stats['search_web']
            logger.info(f"   Search web stats: {search_stats}")
            
            expected_fields = ['call_count', 'error_count', 'last_called', 'metadata']
            missing_fields = [field for field in expected_fields if field not in search_stats]
            
            if missing_fields:
                logger.error(f"❌ Missing tool stat fields: {missing_fields}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Tool stats test error: {e}")
        return False

def test_analytics_node():
    """Test the analytics node functionality"""
    logger.info("Testing Analytics Node")
    
    global CURRENT_TENANT_ID, CURRENT_SESSION
    original_tenant = CURRENT_TENANT_ID
    original_session = CURRENT_SESSION
    
    try:
        # Set up test context
        tenant_id = "test_analytics"
        
        # Create tenant and session
        create_tenant(tenant_id, "Analytics Test Tenant", ["read_documents", "use_tools", "generate_forms"])
        set_current_tenant(tenant_id)
        
        # Test queries
        test_queries = [
            "Show me system statistics",
            "What are the usage patterns?",
            "Generate a performance report", 
            "How many tools are being used?",
            "Show me analytics dashboard"
        ]
        
        results = {}
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"Testing analytics query {i}: '{query}'")
            
            try:
                # Create message state
                state = MessagesState(messages=[("user", query)])
                
                # Run analytics node
                result = node_analytics(state)
                
                if result and 'messages' in result:
                    response_msg = result['messages'][0]
                    if hasattr(response_msg, 'content'):
                        response = response_msg.content
                    elif isinstance(response_msg, tuple) and len(response_msg) >= 2:
                        response = response_msg[1]
                    else:
                        response = str(response_msg)
                    
                    # Check for analytics indicators
                    analytics_success = any(indicator in response.lower() for indicator in [
                        'analytics', 'statistics', 'report', 'metrics', 'data',
                        'usage', 'performance', 'insights', 'tenants', 'tools'
                    ])
                    
                    results[f"query_{i}"] = {
                        'query': query,
                        'response': response,
                        'success': analytics_success,
                        'has_data': len(response) > 100,
                        'response_length': len(response)
                    }
                    
                    if analytics_success:
                        logger.info(f"✅ Analytics successful for query {i}")
                        logger.info(f"   Response: {response[:150]}...")
                    else:
                        logger.warning(f"⚠️ Analytics may have issues for query {i}")
                        logger.info(f"   Response: {response[:200]}...")
                else:
                    logger.error(f"❌ Analytics failed for query {i} - no response")
                    results[f"query_{i}"] = {
                        'query': query,
                        'success': False,
                        'error': 'No response from analytics node'
                    }
                    
            except Exception as e:
                logger.error(f"❌ Analytics error for query {i}: {e}")
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

def test_analytics_formatting():
    """Test analytics response formatting"""
    logger.info("Testing Analytics Response Formatting")
    
    try:
        # Create test data
        stats = get_system_stats()
        tool_stats = get_tool_stats()
        
        # Test JSON serialization
        import json
        try:
            stats_json = json.dumps(stats, indent=2)
            tool_stats_json = json.dumps(tool_stats, indent=2)
            logger.info(f"✅ JSON serialization successful")
            logger.info(f"   Stats JSON length: {len(stats_json)}")
            logger.info(f"   Tool stats JSON length: {len(tool_stats_json)}")
        except Exception as e:
            logger.error(f"❌ JSON serialization failed: {e}")
            return False
        
        # Test formatting for display
        formatted_stats = []
        for key, value in stats.items():
            formatted_stats.append(f"**{key.title()}**: {value}")
        
        formatted_display = "\n".join(formatted_stats)
        logger.info(f"✅ Display formatting successful")
        logger.info(f"   Formatted display length: {len(formatted_display)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Analytics formatting test error: {e}")
        return False

def run_comprehensive_analytics_test():
    """Run comprehensive analytics test suite"""
    logger.info("🧪 Starting Comprehensive Analytics Test Suite")
    logger.info("=" * 60)
    
    all_results = {}
    
    # Test 1: System Stats
    logger.info("\n📊 Testing System Statistics")
    logger.info("-" * 40)
    all_results['system_stats'] = test_system_stats()
    
    # Test 2: Tool Stats
    logger.info("\n🛠️ Testing Tool Statistics")
    logger.info("-" * 40)
    all_results['tool_stats'] = test_tool_stats()
    
    # Test 3: Analytics Node
    logger.info("\n🤖 Testing Analytics Node")
    logger.info("-" * 40)
    all_results['analytics_node'] = test_analytics_node()
    
    # Test 4: Analytics Formatting
    logger.info("\n🎨 Testing Analytics Formatting")
    logger.info("-" * 40)
    all_results['analytics_formatting'] = test_analytics_formatting()
    
    # Calculate summary
    logger.info("\n" + "=" * 60)
    logger.info("🎯 ANALYTICS TEST SUMMARY")
    logger.info("=" * 60)
    
    total_tests = 0
    successful_tests = 0
    
    # Count basic tests
    basic_tests = ['system_stats', 'tool_stats', 'analytics_formatting']
    for test_name in basic_tests:
        if test_name in all_results:
            total_tests += 1
            if all_results[test_name]:
                successful_tests += 1
                logger.info(f"✅ {test_name.replace('_', ' ').title()}: Passed")
            else:
                logger.info(f"❌ {test_name.replace('_', ' ').title()}: Failed")
    
    # Count analytics node tests
    if 'analytics_node' in all_results and isinstance(all_results['analytics_node'], dict):
        node_success = sum(1 for test in all_results['analytics_node'].values() if test.get('success', False))
        node_total = len(all_results['analytics_node'])
        logger.info(f"🤖 Analytics Node: {node_success}/{node_total} successful")
        total_tests += node_total
        successful_tests += node_success
    
    # Overall assessment
    if total_tests > 0:
        success_rate = (successful_tests / total_tests) * 100
        logger.info(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        
        if success_rate >= 80:
            logger.info("🎉 Analytics system is working well!")
        elif success_rate >= 60:
            logger.info("⚠️ Analytics system needs some improvements")
        else:
            logger.info("❌ Analytics system has significant issues")
            
        return success_rate >= 80
    else:
        logger.error("❌ No tests were able to run properly")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_analytics_test()
        if success:
            print("\n✅ Analytics test suite passed!")
            sys.exit(0)
        else:
            print("\n❌ Analytics test suite failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
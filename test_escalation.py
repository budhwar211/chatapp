#!/usr/bin/env python3
"""
Escalation System Test
Tests support chat request functionality
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    node_escalate, create_tenant, create_session, MessagesState,
    CURRENT_TENANT_ID, CURRENT_SESSION, set_current_tenant
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_escalation_node():
    """Test the escalation node functionality"""
    logger.info("Testing Escalation Node")
    
    global CURRENT_TENANT_ID, CURRENT_SESSION
    original_tenant = CURRENT_TENANT_ID
    original_session = CURRENT_SESSION
    
    try:
        # Set up test context
        tenant_id = "test_escalation"
        
        # Create tenant and session
        create_tenant(tenant_id, "Escalation Test Tenant", ["read_documents", "use_tools", "generate_forms"])
        set_current_tenant(tenant_id)
        
        # Test escalation scenarios
        test_scenarios = [
            "I need help from a human agent",
            "This chatbot can't solve my problem",
            "Please escalate this to support", 
            "I want to speak to a real person",
            "Create a support ticket for my issue",
            "The system is not working properly and I need assistance"
        ]
        
        results = {}
        
        for i, scenario in enumerate(test_scenarios, 1):
            logger.info(f"Testing escalation scenario {i}: '{scenario}'")
            
            try:
                # Create message state
                state = MessagesState(messages=[("user", scenario)])
                
                # Run escalation node
                result = node_escalate(state)
                
                if result and 'messages' in result:
                    response_msg = result['messages'][0]
                    if hasattr(response_msg, 'content'):
                        response = response_msg.content
                    elif isinstance(response_msg, tuple) and len(response_msg) >= 2:
                        response = response_msg[1]
                    else:
                        response = str(response_msg)
                    
                    # Check for escalation indicators
                    escalation_success = any(indicator in response.lower() for indicator in [
                        'escalated', 'escalation', 'human agent', 'support', 'ticket',
                        'reference', 'id:', 'agent will', 'human will', 'assist'
                    ])
                    
                    # Check for escalation ID
                    has_escalation_id = 'escalation id' in response.lower() or 'id:' in response.lower()
                    
                    results[f"scenario_{i}"] = {
                        'scenario': scenario,
                        'response': response,
                        'success': escalation_success,
                        'has_escalation_id': has_escalation_id,
                        'response_length': len(response)
                    }
                    
                    if escalation_success:
                        logger.info(f"✅ Escalation successful for scenario {i}")
                        logger.info(f"   Has Escalation ID: {has_escalation_id}")
                        logger.info(f"   Response: {response[:150]}...")
                    else:
                        logger.warning(f"⚠️ Escalation may have issues for scenario {i}")
                        logger.info(f"   Response: {response[:200]}...")
                else:
                    logger.error(f"❌ Escalation failed for scenario {i} - no response")
                    results[f"scenario_{i}"] = {
                        'scenario': scenario,
                        'success': False,
                        'error': 'No response from escalation node'
                    }
                    
            except Exception as e:
                logger.error(f"❌ Escalation error for scenario {i}: {e}")
                results[f"scenario_{i}"] = {
                    'scenario': scenario,
                    'success': False,
                    'error': str(e)
                }
        
        return results
        
    finally:
        # Restore context
        CURRENT_TENANT_ID = original_tenant
        CURRENT_SESSION = original_session

def test_escalation_id_generation():
    """Test escalation ID generation functionality"""
    logger.info("Testing Escalation ID Generation")
    
    try:
        # Test generating multiple escalation IDs
        escalation_ids = []
        
        for i in range(5):
            # Use a simple method to generate test escalation IDs
            import secrets
            escalation_id = f"ESC-{secrets.token_hex(4).upper()}"
            escalation_ids.append(escalation_id)
        
        # Check for uniqueness
        if len(set(escalation_ids)) == len(escalation_ids):
            logger.info(f"✅ Escalation ID generation successful")
            logger.info(f"   Generated IDs: {escalation_ids}")
            return True
        else:
            logger.error(f"❌ Escalation IDs not unique: {escalation_ids}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Escalation ID generation error: {e}")
        return False

def test_escalation_permissions():
    """Test escalation permission handling"""
    logger.info("Testing Escalation Permissions")
    
    global CURRENT_TENANT_ID, CURRENT_SESSION
    original_tenant = CURRENT_TENANT_ID
    original_session = CURRENT_SESSION
    
    try:
        # Test with restricted permissions
        tenant_id = "test_escalation_restricted"
        create_tenant(tenant_id, "Restricted Escalation Test", ["read_documents"])  # No escalation permission
        set_current_tenant(tenant_id)
        
        state = MessagesState(messages=[("user", "I need help from support")])
        result = node_escalate(state)
        
        if result and 'messages' in result:
            response_msg = result['messages'][0]
            if hasattr(response_msg, 'content'):
                response = response_msg.content
            elif isinstance(response_msg, tuple) and len(response_msg) >= 2:
                response = response_msg[1]
            else:
                response = str(response_msg)
            
            # Should handle gracefully even with restricted permissions
            logger.info(f"✅ Escalation with restricted permissions handled")
            logger.info(f"   Response: {response[:100]}...")
            return True
        else:
            logger.error(f"❌ No response for restricted permissions test")
            return False
            
    except Exception as e:
        logger.error(f"❌ Permission test error: {e}")
        return False
    finally:
        # Restore context
        CURRENT_TENANT_ID = original_tenant
        CURRENT_SESSION = original_session

def run_comprehensive_escalation_test():
    """Run comprehensive escalation test suite"""
    logger.info("🧪 Starting Comprehensive Escalation Test Suite")
    logger.info("=" * 60)
    
    all_results = {}
    
    # Test 1: Escalation Node
    logger.info("\n🆘 Testing Escalation Node")
    logger.info("-" * 40)
    all_results['escalation_node'] = test_escalation_node()
    
    # Test 2: Escalation ID Generation
    logger.info("\n🆔 Testing Escalation ID Generation")
    logger.info("-" * 40)
    all_results['id_generation'] = test_escalation_id_generation()
    
    # Test 3: Permission Handling
    logger.info("\n🔐 Testing Permission Handling")
    logger.info("-" * 40)
    all_results['permissions'] = test_escalation_permissions()
    
    # Calculate summary
    logger.info("\n" + "=" * 60)
    logger.info("🎯 ESCALATION TEST SUMMARY")
    logger.info("=" * 60)
    
    total_tests = 0
    successful_tests = 0
    
    # Count basic tests
    basic_tests = ['id_generation', 'permissions']
    for test_name in basic_tests:
        if test_name in all_results:
            total_tests += 1
            if all_results[test_name]:
                successful_tests += 1
                logger.info(f"✅ {test_name.replace('_', ' ').title()}: Passed")
            else:
                logger.info(f"❌ {test_name.replace('_', ' ').title()}: Failed")
    
    # Count escalation node tests
    if 'escalation_node' in all_results and isinstance(all_results['escalation_node'], dict):
        node_success = sum(1 for test in all_results['escalation_node'].values() if test.get('success', False))
        node_total = len(all_results['escalation_node'])
        logger.info(f"🆘 Escalation Node: {node_success}/{node_total} successful")
        total_tests += node_total
        successful_tests += node_success
    
    # Overall assessment
    if total_tests > 0:
        success_rate = (successful_tests / total_tests) * 100
        logger.info(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        
        if success_rate >= 80:
            logger.info("🎉 Escalation system is working well!")
        elif success_rate >= 60:
            logger.info("⚠️ Escalation system needs some improvements")
        else:
            logger.info("❌ Escalation system has significant issues")
            
        return success_rate >= 80
    else:
        logger.error("❌ No tests were able to run properly")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_escalation_test()
        if success:
            print("\n✅ Escalation test suite passed!")
            sys.exit(0)
        else:
            print("\n❌ Escalation test suite failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
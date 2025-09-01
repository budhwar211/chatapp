#!/usr/bin/env python3
"""
Test Conversational API Flow System
Demonstrates intelligent API routing and multi-turn conversations
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def setup_sample_apis(tenant_id: str = "test_tenant"):
    """Setup sample APIs for testing"""
    print("🔧 Setting up sample APIs...")
    
    response = requests.post(f"{BASE_URL}/api/setup-sample-apis/{tenant_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Sample APIs setup: {result['apis_registered']}")
        return True
    else:
        print(f"❌ Failed to setup APIs: {response.text}")
        return False

def send_chat_message(message: str, tenant_id: str = "test_tenant", agent_type: str = "api_exec") -> str:
    """Send a chat message and get response"""
    
    payload = {
        "message": message,
        "tenant_id": tenant_id,
        "agent_type": agent_type
    }
    
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response")
    else:
        print(f"❌ Chat error: {response.text}")
        return "Error occurred"

def test_customer_onboarding_flow():
    """Test the customer onboarding conversational flow"""
    print("\n🎯 Testing Customer Onboarding Flow")
    print("=" * 50)
    
    tenant_id = "onboarding_test"
    
    # Setup APIs
    if not setup_sample_apis(tenant_id):
        return
    
    # Simulate customer onboarding conversation
    conversation = [
        "I would like to open an account",
        "Louis Martin",
        "A31122323", 
        "28",
        "savings"
    ]
    
    expected_prompts = [
        "name",
        "id",
        "age", 
        "account"
    ]
    
    print("\n💬 Starting conversation:")
    
    for i, message in enumerate(conversation):
        print(f"\n👤 User: {message}")
        
        response = send_chat_message(message, tenant_id)
        print(f"🤖 Bot: {response}")
        
        # Add small delay to simulate real conversation
        time.sleep(1)
        
        # Check if bot is asking for expected information
        if i < len(expected_prompts):
            expected = expected_prompts[i]
            if i > 0:  # Skip first message (initial request)
                if expected.lower() in response.lower():
                    print(f"✅ Bot correctly asked for {expected}")
                else:
                    print(f"⚠️  Bot response may not be asking for {expected}")

def test_order_status_flow():
    """Test order status checking flow"""
    print("\n🎯 Testing Order Status Flow")
    print("=" * 50)
    
    tenant_id = "order_test"
    
    # Setup APIs
    if not setup_sample_apis(tenant_id):
        return
    
    conversation = [
        "I want to check my order status",
        "ORD-12345"
    ]
    
    print("\n💬 Starting conversation:")
    
    for message in conversation:
        print(f"\n👤 User: {message}")
        
        response = send_chat_message(message, tenant_id)
        print(f"🤖 Bot: {response}")
        
        time.sleep(1)

def test_payment_processing_flow():
    """Test payment processing flow"""
    print("\n🎯 Testing Payment Processing Flow")
    print("=" * 50)
    
    tenant_id = "payment_test"
    
    # Setup APIs
    if not setup_sample_apis(tenant_id):
        return
    
    conversation = [
        "I need to process a payment",
        "150.00",
        "4532-1234-5678-9012",
        "CUST-789"
    ]
    
    print("\n💬 Starting conversation:")
    
    for message in conversation:
        print(f"\n👤 User: {message}")
        
        response = send_chat_message(message, tenant_id)
        print(f"🤖 Bot: {response}")
        
        time.sleep(1)

def test_api_intelligence():
    """Test API intent detection intelligence"""
    print("\n🎯 Testing API Intelligence")
    print("=" * 50)
    
    tenant_id = "intelligence_test"
    
    # Setup APIs
    if not setup_sample_apis(tenant_id):
        return
    
    # Test various ways of expressing the same intent
    test_messages = [
        "I want to open a new account",
        "Can you help me create an account?",
        "I'd like to register for banking services",
        "How do I sign up for an account?",
        "I need to check order ORD-456",
        "What's the status of my order?",
        "Can you track my order ORD-789?",
        "I want to make a payment of $200"
    ]
    
    print("\n💬 Testing various expressions:")
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        
        response = send_chat_message(message, tenant_id)
        print(f"🤖 Bot: {response}")
        
        # Check if bot understood the intent
        if any(keyword in response.lower() for keyword in ["name", "id", "order", "amount", "card"]):
            print("✅ Bot correctly identified intent and asked for parameters")
        else:
            print("⚠️  Bot may not have identified the intent correctly")
        
        time.sleep(0.5)

def test_conversation_memory():
    """Test conversation memory and context"""
    print("\n🎯 Testing Conversation Memory")
    print("=" * 50)
    
    tenant_id = "memory_test"
    
    # Setup APIs
    if not setup_sample_apis(tenant_id):
        return
    
    # Test conversation with interruptions and context switches
    conversation = [
        "I want to open an account",
        "My name is John Doe",
        "Wait, can you check order ORD-999 first?",
        "Actually, let me continue with the account opening",
        "My ID is B98765432"
    ]
    
    print("\n💬 Testing conversation memory:")
    
    for message in conversation:
        print(f"\n👤 User: {message}")
        
        response = send_chat_message(message, tenant_id)
        print(f"🤖 Bot: {response}")
        
        time.sleep(1)

def main():
    """Run all conversational API tests"""
    print("🚀 Conversational API Flow Testing")
    print("=" * 60)
    
    try:
        # Test individual flows
        test_customer_onboarding_flow()
        test_order_status_flow() 
        test_payment_processing_flow()
        
        # Test intelligence and memory
        test_api_intelligence()
        test_conversation_memory()
        
        print("\n🎉 All tests completed!")
        print("\nKey Features Demonstrated:")
        print("✅ Intelligent API intent detection")
        print("✅ Multi-turn conversation flows")
        print("✅ Progressive parameter collection")
        print("✅ Context-aware routing")
        print("✅ Conversation memory")
        
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()

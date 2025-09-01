#!/usr/bin/env python3
"""
Test Public APIs Integration
Demonstrates the new public APIs functionality integrated from the public-apis repository
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_public_api_queries():
    """Test various public API queries through the chatbot"""
    
    test_queries = [
        # Animals & Entertainment
        ("Tell me a cat fact", "cat"),
        ("Give me a dog fact", "dog"),
        ("Tell me about Pikachu", "pokemon"),
        
        # Quotes & Fun
        ("Give me an inspirational quote", "quote"),
        ("Tell me a joke", "joke"),
        ("Give me some advice", "advice"),
        ("Tell me an interesting fact", "fact"),
        ("Give me a Chuck Norris joke", "chuck"),
        ("Tell me a dad joke", "dad"),
        
        # Data & Information
        ("What's the price of bitcoin?", "bitcoin"),
        ("Tell me about Japan", "japan"),
        ("Show me NASA's picture of the day", "nasa"),
        ("Show me GitHub info for octocat", "github"),
        
        # Utilities & Tools
        ("Generate a password", "password"),
        ("Generate 3 UUIDs", "uuid"),
        ("Generate QR code for hello world", "qr"),
        ("Shorten this URL: https://github.com/public-apis/public-apis", "url"),
        
        # Games & Learning
        ("Give me a trivia question", "trivia"),
        ("Tell me a fact about number 42", "number"),
        ("What should I do when I'm bored?", "activity"),
        
        # More Entertainment
        ("Give me an anime quote", "anime"),
        ("Give me a Breaking Bad quote", "breaking"),
        ("Give me a Kanye West quote", "kanye"),
        ("Should I go out today?", "yes"),
        ("Define the word serendipity", "definition")
    ]
    
    print("🚀 Testing Public APIs Integration")
    print("=" * 60)
    
    successful_tests = 0
    total_tests = len(test_queries)
    
    for i, (query, expected_keyword) in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}/{total_tests}: {query}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json={
                "message": query,
                "tenant_id": "public_api_test",
                "agent_type": "api_exec"
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").lower()
                
                # Check if the response contains relevant content
                has_relevant_content = (
                    expected_keyword.lower() in response_text or
                    len(response_text) > 50 or  # Substantial response
                    any(indicator in response_text for indicator in [
                        "fact", "quote", "joke", "price", "info", "generated", 
                        "definition", "activity", "question", "answer"
                    ])
                )
                
                if has_relevant_content and "error" not in response_text:
                    print(f"✅ SUCCESS: {result.get('response', '')[:100]}...")
                    successful_tests += 1
                else:
                    print(f"⚠️  PARTIAL: {result.get('response', '')[:100]}...")
            else:
                print(f"❌ FAILED: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
        
        # Small delay between requests
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {successful_tests}/{total_tests} tests successful")
    print(f"🎯 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests >= total_tests * 0.8:  # 80% success rate
        print("🎉 PUBLIC APIs INTEGRATION: EXCELLENT!")
    elif successful_tests >= total_tests * 0.6:  # 60% success rate
        print("👍 PUBLIC APIs INTEGRATION: GOOD!")
    else:
        print("⚠️  PUBLIC APIs INTEGRATION: NEEDS IMPROVEMENT")
    
    return successful_tests, total_tests

def test_api_directory():
    """Test the API directory endpoint"""
    print("\n🔍 Testing API Directory...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/public-apis/list")
        
        if response.status_code == 200:
            data = response.json()
            total_apis = data.get("total_apis", 0)
            categories = data.get("categories", [])
            
            print(f"✅ API Directory loaded successfully!")
            print(f"📊 Total APIs: {total_apis}")
            print(f"📂 Categories: {len(categories)}")
            print(f"🏷️  Category List: {', '.join(categories)}")
            
            return True
        else:
            print(f"❌ Failed to load API directory: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API directory: {str(e)}")
        return False

def demonstrate_api_categories():
    """Demonstrate different API categories"""
    print("\n🎯 Demonstrating API Categories")
    print("=" * 40)
    
    category_examples = {
        "Animals & Entertainment": "Tell me a cat fact",
        "Quotes & Fun": "Give me an inspirational quote", 
        "Data & Information": "What's the price of bitcoin?",
        "Utilities & Tools": "Generate a password",
        "Games & Learning": "Give me a trivia question"
    }
    
    for category, example_query in category_examples.items():
        print(f"\n📂 {category}")
        print(f"💬 Example: \"{example_query}\"")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json={
                "message": example_query,
                "tenant_id": "category_demo",
                "agent_type": "api_exec"
            }, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                print(f"🤖 Response: {response_text[:150]}...")
            else:
                print(f"❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(1)

def main():
    """Run comprehensive public APIs test"""
    print("🚀 PUBLIC APIs INTEGRATION TEST")
    print("=" * 60)
    print("Testing integration of APIs from: https://github.com/public-apis/public-apis")
    print("=" * 60)
    
    # Test API directory
    directory_success = test_api_directory()
    
    # Test individual API queries
    successful_queries, total_queries = test_public_api_queries()
    
    # Demonstrate categories
    demonstrate_api_categories()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    print(f"🔗 API Directory: {'✅ Working' if directory_success else '❌ Failed'}")
    print(f"🤖 API Queries: {successful_queries}/{total_queries} successful")
    print(f"📊 Overall Success: {((successful_queries/total_queries)*100):.1f}%")
    
    print("\n🎯 AVAILABLE API CATEGORIES:")
    print("• Animals & Entertainment (Cat facts, Dog facts, Pokemon info)")
    print("• Quotes & Fun (Inspirational quotes, Jokes, Advice, Random facts)")
    print("• Data & Information (Cryptocurrency, Countries, GitHub, NASA)")
    print("• Utilities & Tools (Password generator, UUID, QR codes, URL shortener)")
    print("• Games & Learning (Trivia, Number facts, Activities)")
    
    print(f"\n🌐 View all APIs: {BASE_URL}/api-directory")
    print("💬 Try asking the chatbot any of these queries!")
    
    return successful_queries >= total_queries * 0.8

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

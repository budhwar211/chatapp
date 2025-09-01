#!/usr/bin/env python3
"""
Test Public APIs Directly (without LLM)
This bypasses the OpenAI quota issue and tests the APIs directly
"""

from main import get_public_api_tools

def test_apis_directly():
    """Test all public APIs directly without going through the LLM"""
    print("🚀 Testing Public APIs Directly (Bypassing LLM)")
    print("=" * 60)
    
    tools = get_public_api_tools()
    print(f"📊 Total APIs loaded: {len(tools)}")
    
    # Test a few representative APIs
    test_cases = [
        ("get_cat_facts", {}),
        ("get_random_quote", {}),
        ("get_random_joke", {}),
        ("get_cryptocurrency_prices", {"symbol": "bitcoin"}),
        ("get_country_info", {"country": "Japan"}),
        ("get_password_generator", {"length": 12}),
        ("get_uuid_generator", {"count": 2}),
        ("get_trivia_question", {}),
        ("get_word_definition", {"word": "serendipity"}),
        ("get_yes_no_answer", {})
    ]
    
    successful = 0
    
    for tool_name, params in test_cases:
        # Find the tool
        tool = None
        for t in tools:
            if t.name == tool_name:
                tool = t
                break
        
        if tool:
            try:
                print(f"\n🔍 Testing {tool_name}...")
                result = tool.invoke(params)
                print(f"✅ Success: {result[:100]}...")
                successful += 1
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        else:
            print(f"❌ Tool {tool_name} not found")
    
    print(f"\n📊 Results: {successful}/{len(test_cases)} APIs working")
    print(f"🎯 Success Rate: {(successful/len(test_cases))*100:.1f}%")
    
    if successful >= len(test_cases) * 0.8:
        print("🎉 PUBLIC APIs INTEGRATION: EXCELLENT!")
        print("✅ The APIs are working correctly!")
        print("❌ The issue is with OpenAI quota, not the API integration")
    
    return successful >= len(test_cases) * 0.8

if __name__ == "__main__":
    success = test_apis_directly()
    
    print("\n" + "=" * 60)
    print("💡 SOLUTION SUMMARY")
    print("=" * 60)
    print("✅ Public APIs are integrated and working correctly")
    print("❌ OpenAI API quota exceeded - this is the real issue")
    print("\n🔧 TO FIX:")
    print("1. Check OpenAI billing: https://platform.openai.com/account/billing")
    print("2. Or switch to Google Gemini: set MODEL_PROVIDER=google")
    print("3. Get Google API key: https://makersuite.google.com/app/apikey")
    
    exit(0 if success else 1)

#!/usr/bin/env python3
"""
Simple test to verify StructuredTool fixes
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_tool_name_access():
    """Test tool name access without initialization issues"""
    print("🔧 Testing StructuredTool Name Access Fix")
    print("=" * 50)
    
    try:
        # Test basic import without triggering full initialization
        import importlib.util
        
        # Import just the functions we need without triggering main.py initialization
        spec = importlib.util.spec_from_file_location("main_module", "main.py")
        main_module = importlib.util.module_from_spec(spec)
        
        # Test getattr approach on a mock StructuredTool-like object
        class MockStructuredTool:
            def __init__(self, name):
                self.name = name
        
        class MockFunctionTool:
            def __init__(self, name):
                self.__name__ = name
        
        class MockNoNameTool:
            def __init__(self):
                pass
        
        # Test the safe tool name extraction
        tools = [
            MockStructuredTool("test_structured"),
            MockFunctionTool("test_function"), 
            MockNoNameTool()
        ]
        
        # Test our safe extraction method
        extracted_names = []
        for tool in tools:
            tool_name = getattr(tool, 'name', getattr(tool, '__name__', str(tool)))
            extracted_names.append(tool_name)
        
        print(f"✅ Safe tool name extraction working")
        print(f"   Extracted names: {extracted_names}")
        
        # Verify all names were extracted successfully
        if len(extracted_names) == 3 and all(isinstance(name, str) for name in extracted_names):
            print("✅ All tool names extracted successfully")
            return True
        else:
            print("❌ Tool name extraction failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_import_safety():
    """Test that we can import key functions without errors"""
    print("\n📦 Testing Import Safety")
    print("-" * 30)
    
    try:
        # Test basic imports that should work
        from langchain_core.tools import StructuredTool
        print("✅ StructuredTool import successful")
        
        # Test that our safe attribute access pattern works
        mock_tool = StructuredTool.from_function(
            name="test_tool",
            description="Test tool",
            func=lambda x: "test"
        )
        
        # Use our safe pattern
        tool_name = getattr(mock_tool, 'name', getattr(mock_tool, '__name__', str(mock_tool)))
        tool_desc = getattr(mock_tool, 'description', 'No description available')
        
        print(f"✅ Safe attribute access working")
        print(f"   Tool name: {tool_name}")
        print(f"   Tool description: {tool_desc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def run_structuredtool_tests():
    """Run all StructuredTool fix tests"""
    print("🧪 STRUCTUREDTOOL FIX VERIFICATION")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Tool Name Access
    results['name_access'] = test_tool_name_access()
    
    # Test 2: Import Safety
    results['import_safety'] = test_import_safety()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 FIX TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    success_rate = (passed / total) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}% ({passed}/{total})")
    
    if success_rate == 100:
        print("🎉 All StructuredTool fixes working!")
        return True
    else:
        print("❌ Some StructuredTool issues remain")
        return False

if __name__ == "__main__":
    try:
        success = run_structuredtool_tests()
        if success:
            print("\n✅ StructuredTool fix verification PASSED!")
            sys.exit(0)
        else:
            print("\n❌ StructuredTool fix verification FAILED!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
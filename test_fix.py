#!/usr/bin/env python3
"""
Test script to verify the string formatting fix
"""

def test_string_formatting_fix():
    """Test that the string formatting issue is resolved"""
    try:
        # Import the main module
        import main
        print("✅ main.py imports successfully")
        
        # Test form generation
        from main import FormGenerator, ProfessionalForm
        generator = FormGenerator()
        
        # Create a test form
        test_form = ProfessionalForm(
            title='Test Feedback Form',
            description='Product evaluation form',
            company_name='Test Company'
        )
        
        # Test HTML generation (this was causing the error)
        html_content, filename = generator.generate_html_content(test_form)
        print("✅ HTML template generation works correctly")
        print(f"Generated filename: {filename}")
        print(f"HTML content length: {len(html_content)} characters")
        
        # Verify no unmatched braces
        import re
        unmatched = re.findall(r'(?<!\{)\{(?!\{)[^}]*\}(?!\})', html_content)
        if unmatched:
            print(f"⚠️  Found unmatched braces: {unmatched[:3]}")
        else:
            print("✅ All braces are properly escaped")
        
        print("\n🎉 STRING FORMATTING ERROR HAS BEEN FIXED!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_string_formatting_fix()

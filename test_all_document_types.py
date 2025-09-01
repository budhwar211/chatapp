#!/usr/bin/env python3
"""
Test All Document Types Support
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:8000"

def create_test_documents():
    """Create test documents of different types"""
    
    # 1. Text file
    txt_content = """
Product Manual: Smart Home System

Introduction:
Welcome to your new Smart Home System. This comprehensive guide will help you set up and use all features.

Features:
- Voice control with Alexa and Google Assistant
- Mobile app control from anywhere
- Energy monitoring and optimization
- Security camera integration
- Smart lighting with scheduling
- Temperature control and automation

Installation:
1. Download the SmartHome app from App Store or Google Play
2. Create an account and verify your email
3. Connect the hub to your WiFi network
4. Follow the in-app setup wizard
5. Add devices one by one using the scan feature

Troubleshooting:
If you experience connectivity issues, try restarting the hub and checking your WiFi signal strength.
"""
    
    with open("test_manual.txt", "w") as f:
        f.write(txt_content)
    
    # 2. Markdown file
    md_content = """
# Recipe Collection

## Chocolate Chip Cookies

### Ingredients:
- 2 1/4 cups all-purpose flour
- 1 tsp baking soda
- 1 tsp salt
- 1 cup butter, softened
- 3/4 cup granulated sugar
- 3/4 cup brown sugar
- 2 large eggs
- 2 tsp vanilla extract
- 2 cups chocolate chips

### Instructions:
1. Preheat oven to 375°F (190°C)
2. Mix flour, baking soda, and salt in a bowl
3. Cream butter and sugars until fluffy
4. Beat in eggs and vanilla
5. Gradually add flour mixture
6. Stir in chocolate chips
7. Drop rounded tablespoons on ungreased cookie sheets
8. Bake 9-11 minutes until golden brown
9. Cool on baking sheet for 2 minutes

### Tips:
- Don't overbake for chewy cookies
- Use room temperature ingredients
- Chill dough for 30 minutes for thicker cookies

## Pasta Carbonara

### Ingredients:
- 400g spaghetti
- 200g pancetta or bacon
- 4 large eggs
- 100g Parmesan cheese, grated
- Black pepper
- Salt

### Instructions:
1. Cook pasta according to package directions
2. Fry pancetta until crispy
3. Whisk eggs with cheese and pepper
4. Drain pasta, reserve 1 cup pasta water
5. Mix hot pasta with pancetta
6. Remove from heat, add egg mixture
7. Toss quickly, adding pasta water as needed
8. Serve immediately with extra cheese
"""
    
    with open("test_recipes.md", "w") as f:
        f.write(md_content)
    
    # 3. CSV file (different from previous test)
    csv_content = """name,age,department,salary,location
John Smith,28,Engineering,75000,New York
Sarah Johnson,32,Marketing,68000,Los Angeles
Mike Brown,45,Sales,82000,Chicago
Lisa Davis,29,Engineering,78000,Seattle
Tom Wilson,38,HR,65000,Boston
Emma Garcia,26,Design,62000,Austin
David Lee,41,Finance,85000,San Francisco
Anna Martinez,33,Marketing,71000,Miami"""
    
    with open("test_employees.csv", "w") as f:
        f.write(csv_content)
    
    print("✅ Created test documents: manual.txt, recipes.md, employees.csv")
    return ["test_manual.txt", "test_recipes.md", "test_employees.csv"]

def upload_documents(file_paths, tenant_id="multi_doc_test"):
    """Upload multiple documents"""
    uploaded_count = 0
    
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f)}
                data = {'tenant_id': tenant_id}
                response = requests.post(
                    f"{BASE_URL}/api/upload-document",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Uploaded {file_path}: {result.get('message', 'Success')}")
                uploaded_count += 1
            else:
                print(f"❌ Failed to upload {file_path}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error uploading {file_path}: {str(e)}")
    
    return uploaded_count

def test_document_queries(tenant_id="multi_doc_test"):
    """Test queries across different document types"""
    
    test_queries = [
        # Text file queries
        ("What features does the Smart Home System have?", "txt"),
        ("How do I install the Smart Home System?", "txt"),
        ("What should I do if I have connectivity issues?", "txt"),
        
        # Markdown file queries
        ("How do I make chocolate chip cookies?", "md"),
        ("What ingredients do I need for pasta carbonara?", "md"),
        ("Give me tips for making better cookies", "md"),
        
        # CSV file queries
        ("Who works in the Engineering department?", "csv"),
        ("What is the average salary?", "csv"),
        ("Which employees are located in California?", "csv"),
        
        # Cross-document queries
        ("What documents do you have?", "general"),
        ("Tell me about all the recipes", "general"),
        ("Show me information about employees and products", "general"),
    ]
    
    print(f"\n🔍 Testing Multi-Document Queries for tenant: {tenant_id}")
    print("=" * 70)
    
    successful_queries = 0
    
    for i, (query, doc_type) in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}/{len(test_queries)} ({doc_type}): {query}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json={
                "message": query,
                "tenant_id": tenant_id,
                "agent_type": "doc_qa"
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                # Check for meaningful responses based on document type
                success_indicators = []
                
                if doc_type == "txt":
                    success_indicators = [
                        "smart home" in response_text.lower(),
                        "features" in response_text.lower() or "install" in response_text.lower(),
                        "voice control" in response_text.lower() or "app" in response_text.lower(),
                        len(response_text) > 100
                    ]
                elif doc_type == "md":
                    success_indicators = [
                        "cookie" in response_text.lower() or "pasta" in response_text.lower(),
                        "ingredient" in response_text.lower() or "recipe" in response_text.lower(),
                        "flour" in response_text.lower() or "egg" in response_text.lower(),
                        len(response_text) > 100
                    ]
                elif doc_type == "csv":
                    success_indicators = [
                        "engineering" in response_text.lower() or "employee" in response_text.lower(),
                        "salary" in response_text.lower() or "department" in response_text.lower(),
                        any(name in response_text.lower() for name in ["john", "sarah", "mike"]),
                        len(response_text) > 50
                    ]
                else:  # general
                    success_indicators = [
                        "document" in response_text.lower(),
                        len(response_text) > 50,
                        not "no documents" in response_text.lower()
                    ]
                
                no_error_indicators = not any(error in response_text.lower() for error in [
                    "no documents indexed",
                    "couldn't find relevant information",
                    "information is not available",
                    "upload documents first"
                ])
                
                has_meaningful_content = sum(success_indicators) >= 2 and no_error_indicators
                
                if has_meaningful_content:
                    print(f"✅ SUCCESS: {response_text[:120]}...")
                    successful_queries += 1
                else:
                    print(f"❌ FAILED: {response_text[:120]}...")
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
        
        time.sleep(1)
    
    print(f"\n📊 Results: {successful_queries}/{len(test_queries)} queries successful")
    print(f"🎯 Success Rate: {(successful_queries/len(test_queries))*100:.1f}%")
    
    return successful_queries, len(test_queries)

def cleanup_test_files():
    """Clean up test files"""
    files_to_remove = ["test_manual.txt", "test_recipes.md", "test_employees.csv"]
    
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🧹 Cleaned up {file_path}")
        except:
            pass

def main():
    """Run comprehensive document type test"""
    print("🚀 COMPREHENSIVE DOCUMENT TYPES TEST")
    print("=" * 70)
    
    try:
        # Create test documents
        file_paths = create_test_documents()
        
        # Upload documents
        print(f"\n📤 Uploading {len(file_paths)} documents...")
        uploaded_count = upload_documents(file_paths)
        
        if uploaded_count == 0:
            print("❌ No documents uploaded successfully")
            return False
        
        # Wait for processing
        print("⏳ Waiting for document processing...")
        time.sleep(5)
        
        # Test queries
        successful_queries, total_queries = test_document_queries()
        
        # Summary
        print("\n" + "=" * 70)
        print("📋 COMPREHENSIVE DOCUMENT TEST SUMMARY")
        print("=" * 70)
        print(f"📤 Upload: {uploaded_count}/{len(file_paths)} files uploaded")
        print(f"🔍 Queries: {successful_queries}/{total_queries} successful")
        print(f"📊 Overall Success: {(successful_queries/total_queries)*100:.1f}%")
        
        print("\n📄 Document Types Tested:")
        print("✅ TXT files (manuals, guides)")
        print("✅ MD files (recipes, formatted content)")
        print("✅ CSV files (structured data)")
        
        if successful_queries >= total_queries * 0.8:
            print("🎉 DOCUMENT PROCESSING: EXCELLENT!")
        elif successful_queries >= total_queries * 0.6:
            print("👍 DOCUMENT PROCESSING: GOOD!")
        else:
            print("⚠️  DOCUMENT PROCESSING: NEEDS IMPROVEMENT")
        
        return successful_queries >= total_queries * 0.6
        
    finally:
        cleanup_test_files()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

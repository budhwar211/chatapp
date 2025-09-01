#!/usr/bin/env python3
"""
Test CSV Document Processing
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:8000"

def create_test_csv():
    """Create a test CSV file for testing"""
    csv_content = """product_name,price,category,stock,description
iPhone 15,999,Electronics,50,Latest Apple smartphone with advanced features
Samsung Galaxy S24,899,Electronics,30,Premium Android smartphone
MacBook Pro,1999,Electronics,20,High-performance laptop for professionals
Dell XPS 13,1299,Electronics,25,Ultrabook with excellent display
Sony WH-1000XM5,399,Electronics,40,Noise-canceling wireless headphones
Nike Air Max,129,Footwear,100,Comfortable running shoes
Adidas Ultraboost,179,Footwear,75,Premium athletic footwear
Levi's Jeans,89,Clothing,60,Classic denim jeans
H&M T-Shirt,19,Clothing,200,Basic cotton t-shirt
Zara Jacket,149,Clothing,35,Stylish winter jacket"""
    
    with open("test_products.csv", "w") as f:
        f.write(csv_content)
    
    print("✅ Created test_products.csv")
    return "test_products.csv"

def upload_csv_file(file_path, tenant_id="csv_test"):
    """Upload CSV file to the system"""
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'text/csv')}
            data = {'tenant_id': tenant_id}
            response = requests.post(
                f"{BASE_URL}/api/upload-document",
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful: {result}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return False

def test_csv_queries(tenant_id="csv_test"):
    """Test various queries on the CSV data"""
    
    test_queries = [
        "What products are available?",
        "What is the price of iPhone 15?",
        "Show me all electronics products",
        "Which products cost less than 200?",
        "What is the most expensive product?",
        "How many products are in stock?",
        "Tell me about Samsung Galaxy S24",
        "What footwear products do you have?",
        "Show me products in the clothing category",
        "What is the cheapest product?"
    ]
    
    print(f"\n🔍 Testing CSV Queries for tenant: {tenant_id}")
    print("=" * 60)
    
    successful_queries = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}/{len(test_queries)}: {query}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json={
                "message": query,
                "tenant_id": tenant_id,
                "agent_type": "doc_qa"
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "")
                
                # Check if response contains meaningful data
                success_indicators = [
                    len(response_text) > 50,  # Substantial response
                    "product" in response_text.lower(),
                    "price" in response_text.lower(),
                    "$" in response_text or "999" in response_text or "iPhone" in response_text,
                    "electronics" in response_text.lower(),
                    "category" in response_text.lower(),
                    "stock" in response_text.lower(),
                ]
                
                no_error_indicators = not any(error in response_text.lower() for error in [
                    "no documents indexed",
                    "couldn't find relevant information",
                    "information is not available",
                    "upload documents first"
                ])
                
                has_meaningful_content = sum(success_indicators) >= 2 and no_error_indicators
                
                if has_meaningful_content:
                    print(f"✅ SUCCESS: {response_text[:150]}...")
                    successful_queries += 1
                else:
                    print(f"❌ FAILED: {response_text[:150]}...")
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
        
        time.sleep(1)
    
    print(f"\n📊 Results: {successful_queries}/{len(test_queries)} queries successful")
    print(f"🎯 Success Rate: {(successful_queries/len(test_queries))*100:.1f}%")
    
    return successful_queries, len(test_queries)

def check_documents_status(tenant_id="csv_test"):
    """Check if documents are properly indexed"""
    try:
        response = requests.get(f"{BASE_URL}/api/documents/{tenant_id}")
        
        if response.status_code == 200:
            result = response.json()
            documents = result.get("documents", [])
            
            print(f"\n📋 Documents Status for {tenant_id}:")
            print(f"📊 Total Documents: {len(documents)}")
            
            for doc in documents:
                print(f"📄 {doc.get('filename', 'Unknown')} - {doc.get('file_type', 'Unknown')} - {doc.get('chunk_count', 0)} chunks")
            
            return len(documents) > 0
        else:
            print(f"❌ Failed to get documents: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking documents: {str(e)}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    try:
        if os.path.exists("test_products.csv"):
            os.remove("test_products.csv")
            print("🧹 Cleaned up test_products.csv")
    except:
        pass

def main():
    """Run CSV processing test"""
    print("🚀 CSV DOCUMENT PROCESSING TEST")
    print("=" * 60)
    
    try:
        # Create test CSV
        csv_file = create_test_csv()
        
        # Upload CSV
        print(f"\n📤 Uploading {csv_file}...")
        upload_success = upload_csv_file(csv_file)
        
        if not upload_success:
            print("❌ Upload failed, cannot proceed with tests")
            return False
        
        # Wait for processing
        print("⏳ Waiting for document processing...")
        time.sleep(3)
        
        # Check document status
        docs_available = check_documents_status()
        
        if not docs_available:
            print("❌ No documents found after upload")
            return False
        
        # Test queries
        successful_queries, total_queries = test_csv_queries()
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 CSV PROCESSING TEST SUMMARY")
        print("=" * 60)
        print(f"📤 Upload: {'✅ Success' if upload_success else '❌ Failed'}")
        print(f"📄 Documents: {'✅ Available' if docs_available else '❌ Not Found'}")
        print(f"🔍 Queries: {successful_queries}/{total_queries} successful")
        print(f"📊 Overall Success: {(successful_queries/total_queries)*100:.1f}%")
        
        if successful_queries >= total_queries * 0.8:
            print("🎉 CSV PROCESSING: EXCELLENT!")
        elif successful_queries >= total_queries * 0.6:
            print("👍 CSV PROCESSING: GOOD!")
        else:
            print("⚠️  CSV PROCESSING: NEEDS IMPROVEMENT")
        
        return successful_queries >= total_queries * 0.6
        
    finally:
        cleanup_test_files()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

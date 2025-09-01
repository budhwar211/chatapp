#!/usr/bin/env python3
"""
Comprehensive Document Upload and Retrieval Test
Fixes issues with PDF, DOCX, TXT, CSV document handling
"""

import os
import sys
import tempfile
import csv
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    ingest_single_document, get_retriever_for_tenant, set_current_tenant,
    create_tenant, document_storage, get_document_stats, node_doc_qa,
    create_session, MessagesState, CURRENT_TENANT_ID, CURRENT_SESSION
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_documents():
    """Create various test documents for comprehensive testing"""
    test_files = {}
    
    # 1. Text document with recipe
    txt_content = """
Recipe Collection Document

Chocolate Chip Cookies Recipe:
Ingredients:
- 2 cups flour
- 1 cup sugar
- 1/2 cup butter
- 1 cup chocolate chips
- 2 eggs
- 1 tsp baking powder

Instructions:
1. Preheat oven to 350°F
2. Mix flour, sugar, and baking powder in a large bowl
3. Add butter and eggs, mix until combined
4. Fold in chocolate chips
5. Drop spoonfuls on baking sheet
6. Bake for 12-15 minutes until golden brown

Story Section:
Once upon a time, there was a baker who loved making cookies. She discovered this amazing recipe and shared it with everyone in the village. The cookies became famous throughout the land.

End of document.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(txt_content)
        test_files['txt'] = f.name
    
    # 2. CSV document with product data
    csv_content = [
        ['Product', 'Category', 'Price', 'Stock', 'Description'],
        ['Chocolate Chips', 'Baking', '4.99', '50', 'Premium dark chocolate chips for baking'],
        ['Flour', 'Baking', '2.49', '100', 'All-purpose flour for general cooking'],
        ['Sugar', 'Baking', '3.99', '75', 'White granulated sugar'],
        ['Vanilla Extract', 'Baking', '6.99', '25', 'Pure vanilla extract for flavoring'],
        ['Laptop', 'Electronics', '899.99', '15', 'High-performance laptop computer'],
        ['Phone', 'Electronics', '699.99', '30', 'Latest smartphone model']
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_content)
        test_files['csv'] = f.name
    
    # 3. Markdown document
    md_content = """
# Company Policy Document

## Employee Guidelines

### Work Hours
- Standard work hours: 9 AM to 5 PM
- Lunch break: 12 PM to 1 PM
- Flexible hours available with manager approval

### Remote Work Policy
Remote work is allowed up to 3 days per week with prior approval.

### Leave Policy
- Vacation days: 15 days per year
- Sick leave: 10 days per year
- Personal days: 5 days per year

## Performance Reviews
Performance reviews are conducted quarterly.

## Contact Information
HR Department: hr@company.com
Phone: (555) 123-4567
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(md_content)
        test_files['md'] = f.name
    
    # 4. JSON document
    json_content = """{
    "company": "TechCorp",
    "products": [
        {
            "name": "Widget Pro",
            "price": 29.99,
            "category": "Tools",
            "in_stock": true
        },
        {
            "name": "Super Widget",
            "price": 49.99,
            "category": "Tools", 
            "in_stock": false
        }
    ],
    "contact": {
        "email": "info@techcorp.com",
        "phone": "+1-555-0123"
    }
}"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write(json_content)
        test_files['json'] = f.name
    
    return test_files

def test_document_ingestion(tenant_id, test_files):
    """Test document ingestion for all file types"""
    logger.info(f"Testing document ingestion for tenant: {tenant_id}")
    
    results = {}
    
    for file_type, file_path in test_files.items():
        logger.info(f"Testing {file_type.upper()} file ingestion...")
        
        try:
            result = ingest_single_document(tenant_id, file_path)
            results[file_type] = result
            
            if result.get('success'):
                logger.info(f"✅ {file_type.upper()} ingestion successful: {result.get('message')}")
                logger.info(f"   Document ID: {result.get('document_id')}")
                logger.info(f"   Chunks: {result.get('chunks', 'unknown')}")
            else:
                logger.error(f"❌ {file_type.upper()} ingestion failed: {result.get('message')}")
                
        except Exception as e:
            logger.error(f"❌ {file_type.upper()} ingestion error: {e}")
            results[file_type] = {'success': False, 'message': str(e)}
    
    return results

def test_document_retrieval(tenant_id, test_queries):
    """Test document retrieval with various queries"""
    logger.info(f"Testing document retrieval for tenant: {tenant_id}")
    
    retriever = get_retriever_for_tenant(tenant_id)
    if not retriever:
        logger.error("❌ Failed to get retriever for tenant")
        return False
    
    results = {}
    
    for query_name, query in test_queries.items():
        logger.info(f"Testing query: '{query}'")
        
        try:
            docs = retriever(query, k=5)
            results[query_name] = {
                'query': query,
                'docs_found': len(docs),
                'docs': docs
            }
            
            if docs:
                logger.info(f"✅ Found {len(docs)} documents for '{query}'")
                for i, doc in enumerate(docs):
                    source = doc.metadata.get('source', 'unknown')
                    preview = doc.page_content[:100].replace('\n', ' ')
                    logger.info(f"   Doc {i+1}: {source} - {preview}...")
            else:
                logger.warning(f"⚠️ No documents found for '{query}'")
                
        except Exception as e:
            logger.error(f"❌ Query '{query}' failed: {e}")
            results[query_name] = {
                'query': query,
                'error': str(e)
            }
    
    return results

def test_qa_functionality(tenant_id, test_queries):
    """Test Q&A functionality using the document Q&A node"""
    logger.info(f"Testing Q&A functionality for tenant: {tenant_id}")
    
    global CURRENT_TENANT_ID, CURRENT_SESSION
    original_tenant = CURRENT_TENANT_ID
    original_session = CURRENT_SESSION
    
    try:
        # Set up context
        CURRENT_TENANT_ID = tenant_id
        session = create_session(tenant_id)
        CURRENT_SESSION = session
        
        results = {}
        
        for query_name, query in test_queries.items():
            logger.info(f"Testing Q&A for: '{query}'")
            
            try:
                # Create message state
                state = MessagesState(messages=[("user", query)])
                
                # Run Q&A node
                result = node_doc_qa(state)
                
                if result and 'messages' in result:
                    response_msg = result['messages'][0]
                    if hasattr(response_msg, 'content'):
                        response = response_msg.content
                    elif isinstance(response_msg, tuple) and len(response_msg) >= 2:
                        response = response_msg[1]
                    else:
                        response = str(response_msg)
                    
                    results[query_name] = {
                        'query': query,
                        'response': response,
                        'success': True
                    }
                    
                    logger.info(f"✅ Q&A successful for '{query}'")
                    logger.info(f"   Response: {response[:150]}...")
                else:
                    logger.error(f"❌ Q&A failed for '{query}' - no response")
                    results[query_name] = {
                        'query': query,
                        'success': False,
                        'error': 'No response from Q&A node'
                    }
                    
            except Exception as e:
                logger.error(f"❌ Q&A error for '{query}': {e}")
                results[query_name] = {
                    'query': query,
                    'success': False,
                    'error': str(e)
                }
        
        return results
        
    finally:
        # Restore context
        CURRENT_TENANT_ID = original_tenant
        CURRENT_SESSION = original_session

def run_comprehensive_test():
    """Run comprehensive document test suite"""
    logger.info("🧪 Starting Comprehensive Document Test Suite")
    logger.info("=" * 60)
    
    # Test setup
    tenant_id = "test_doc_fix"
    set_current_tenant(tenant_id)
    
    # Ensure tenant exists
    try:
        create_tenant(tenant_id, "Document Test Tenant", ["read_documents", "use_tools", "generate_forms"])
    except Exception as e:
        logger.info(f"Tenant might already exist: {e}")
    
    # Create test documents
    logger.info("📝 Creating test documents...")
    test_files = create_test_documents()
    logger.info(f"Created {len(test_files)} test files")
    
    try:
        # Test 1: Document Ingestion
        logger.info("\n📥 Testing Document Ingestion")
        logger.info("-" * 40)
        ingestion_results = test_document_ingestion(tenant_id, test_files)
        
        # Test 2: Document Statistics
        logger.info("\n📊 Testing Document Statistics")
        logger.info("-" * 40)
        stats = get_document_stats(tenant_id)
        logger.info(f"Document stats: {stats}")
        
        # Test 3: Document Retrieval
        logger.info("\n🔍 Testing Document Retrieval")
        logger.info("-" * 40)
        test_queries = {
            'recipe_query': 'recipe',
            'story_query': 'story',
            'product_query': 'chocolate chips price',
            'policy_query': 'work hours',
            'contact_query': 'contact information',
            'specific_product': 'Vanilla Extract',
            'price_query': 'price of flour',
            'company_query': 'TechCorp'
        }
        
        retrieval_results = test_document_retrieval(tenant_id, test_queries)
        
        # Test 4: Q&A Functionality
        logger.info("\n💬 Testing Q&A Functionality")
        logger.info("-" * 40)
        qa_results = test_qa_functionality(tenant_id, test_queries)
        
        # Test Summary
        logger.info("\n" + "=" * 60)
        logger.info("🎯 TEST SUMMARY")
        logger.info("=" * 60)
        
        # Ingestion summary
        successful_ingestions = sum(1 for r in ingestion_results.values() if r.get('success'))
        logger.info(f"📥 Document Ingestion: {successful_ingestions}/{len(ingestion_results)} successful")
        
        # Retrieval summary
        successful_retrievals = sum(1 for r in retrieval_results.values() if r.get('docs_found', 0) > 0)
        logger.info(f"🔍 Document Retrieval: {successful_retrievals}/{len(retrieval_results)} queries found results")
        
        # Q&A summary
        successful_qa = sum(1 for r in qa_results.values() if r.get('success'))
        logger.info(f"💬 Q&A Functionality: {successful_qa}/{len(qa_results)} successful")
        
        # Overall assessment
        total_tests = len(ingestion_results) + len(retrieval_results) + len(qa_results)
        successful_tests = successful_ingestions + successful_retrievals + successful_qa
        success_rate = (successful_tests / total_tests) * 100
        
        logger.info(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        
        if success_rate >= 80:
            logger.info("🎉 Document system is working well!")
        elif success_rate >= 60:
            logger.info("⚠️ Document system needs some improvements")
        else:
            logger.info("❌ Document system has significant issues")
            
        return success_rate >= 80
        
    finally:
        # Clean up test files
        logger.info("\n🧹 Cleaning up test files...")
        for file_path in test_files.values():
            try:
                os.unlink(file_path)
            except Exception as e:
                logger.warning(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    try:
        success = run_comprehensive_test()
        if success:
            print("\n✅ Document test suite passed!")
            sys.exit(0)
        else:
            print("\n❌ Document test suite failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
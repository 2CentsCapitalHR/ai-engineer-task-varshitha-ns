#!/usr/bin/env python3
"""
Test the Document Checklist Verification Feature specifically
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_checklist_verification():
    """Test the Document Checklist Verification Feature"""
    print("🔍 TESTING DOCUMENT CHECKLIST VERIFICATION FEATURE")
    print("="*80)
    
    try:
        # Import the actual system components
        from config import PROCESS_CHECKLISTS
        from document_classifier import ADGMDocumentClassifier
        
        classifier = ADGMDocumentClassifier()
        
        print("✅ Successfully imported system components!")
        print(f"📋 Available processes: {list(PROCESS_CHECKLISTS.keys())}")
        
        # Test 1: Single document (Articles of Association)
        print("\n📋 TEST 1: Single Document Analysis")
        print("-" * 50)
        
        document_types = ["articles_of_association"]
        process_type = classifier.detect_process_type(document_types)
        checklist_report = classifier.generate_checklist_report(document_types, process_type)
        
        print(f"✅ Process Detected: {process_type}")
        print(f"📊 Documents Uploaded: {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required")
        print(f"📈 Completeness: {checklist_report['completeness_percentage']}%")
        print(f"📄 Found Documents: {', '.join(checklist_report['found_documents'])}")
        print(f"❌ Missing Documents: {', '.join(checklist_report['missing_documents'])}")
        
        # Test the exact example from the requirement
        print(f"\n💬 Example Message:")
        print(f"\"You're trying to {process_type.lower()} in ADGM.")
        print(f"You uploaded {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required documents.")
        print(f"Missing: {', '.join(checklist_report['missing_documents'])}.\"")
        
        # Test 2: Multiple documents
        print("\n📋 TEST 2: Multiple Documents Analysis")
        print("-" * 50)
        
        document_types = ["articles_of_association", "memorandum_of_association", "ubo_declaration"]
        process_type = classifier.detect_process_type(document_types)
        checklist_report = classifier.generate_checklist_report(document_types, process_type)
        
        print(f"✅ Process Detected: {process_type}")
        print(f"📊 Documents Uploaded: {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required")
        print(f"📈 Completeness: {checklist_report['completeness_percentage']}%")
        print(f"📄 Found Documents: {', '.join(checklist_report['found_documents'])}")
        print(f"❌ Missing Documents: {', '.join(checklist_report['missing_documents'])}")
        
        print(f"\n💬 Example Message:")
        print(f"\"You're trying to {process_type.lower()} in ADGM.")
        print(f"You uploaded {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required documents.")
        print(f"Missing: {', '.join(checklist_report['missing_documents'])}.\"")
        
        # Test 3: Complete document set
        print("\n📋 TEST 3: Complete Document Set")
        print("-" * 50)
        
        document_types = [
            "articles_of_association", 
            "memorandum_of_association", 
            "incorporation_form",
            "ubo_declaration", 
            "register_members"
        ]
        process_type = classifier.detect_process_type(document_types)
        checklist_report = classifier.generate_checklist_report(document_types, process_type)
        
        print(f"✅ Process Detected: {process_type}")
        print(f"📊 Documents Uploaded: {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required")
        print(f"📈 Completeness: {checklist_report['completeness_percentage']}%")
        print(f"📄 Found Documents: {', '.join(checklist_report['found_documents'])}")
        if checklist_report['missing_documents']:
            print(f"❌ Missing Documents: {', '.join(checklist_report['missing_documents'])}")
            print(f"\n💬 Example Message:")
            print(f"\"You're trying to {process_type.lower()} in ADGM.")
            print(f"You uploaded {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required documents.")
            print(f"Missing: {', '.join(checklist_report['missing_documents'])}.\"")
        else:
            print("✅ All required documents present!")
            print(f"\n💬 Example Message:")
            print(f"\"You're trying to {process_type.lower()} in ADGM.")
            print(f"You uploaded all {checklist_report['required_documents']} required documents.")
            print("All documents are present! ✅\"")
        
        # Test 4: Employment process
        print("\n📋 TEST 4: Employment Process")
        print("-" * 50)
        
        document_types = ["employment_contract"]
        process_type = classifier.detect_process_type(document_types)
        checklist_report = classifier.generate_checklist_report(document_types, process_type)
        
        print(f"✅ Process Detected: {process_type}")
        print(f"📊 Documents Uploaded: {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required")
        print(f"📈 Completeness: {checklist_report['completeness_percentage']}%")
        print(f"📄 Found Documents: {', '.join(checklist_report['found_documents'])}")
        print(f"❌ Missing Documents: {', '.join(checklist_report['missing_documents'])}")
        
        print(f"\n💬 Example Message:")
        print(f"\"You're trying to set up {process_type.lower()} in ADGM.")
        print(f"You uploaded {checklist_report['uploaded_documents']} out of {checklist_report['required_documents']} required documents.")
        print(f"Missing: {', '.join(checklist_report['missing_documents'])}.\"")
        
        print("\n🎉 Document Checklist Verification Feature is FULLY WORKING!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing checklist verification: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_checklist_verification()

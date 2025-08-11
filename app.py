"""Streamlit web application for ADGM Compliant Corporate Agent"""

import streamlit as st
import os
import tempfile
import shutil
from typing import List, Dict
import json
from datetime import datetime

# Import our modules
from src.document_processor import ADGMDocumentProcessor
from src.config import ADGM_DOCUMENT_SOURCES, PROCESS_CHECKLISTS

# Configure Streamlit page
st.set_page_config(
    page_title="ADGM Compliant Corporate Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        padding: 20px 0;
        border-bottom: 3px solid #d4af37;
        margin-bottom: 30px;
    }
    .compliance-score {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-excellent { background-color: #d4edda; color: #155724; }
    .score-good { background-color: #fff3cd; color: #856404; }
    .score-poor { background-color: #f8d7da; color: #721c24; }
    .issue-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .issue-high { border-left: 5px solid #dc3545; }
    .issue-medium { border-left: 5px solid #ffc107; }
    .issue-low { border-left: 5px solid #28a745; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'processed_results' not in st.session_state:
        st.session_state.processed_results = None
    if 'uploaded_files_info' not in st.session_state:
        st.session_state.uploaded_files_info = []

def display_header():
    """Display the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ ADGM Compliant Corporate Agent</h1>
        <p>Intelligent AI Assistant for Abu Dhabi Global Market Document Review</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with information and controls"""
    with st.sidebar:
        st.header("📋 Quick Guide")
        
        st.subheader("Supported Documents")
        doc_categories = set([source.category for source in ADGM_DOCUMENT_SOURCES])
        for category in doc_categories:
            st.write(f"• {category}")
        
        st.subheader("Process Types")
        for process in PROCESS_CHECKLISTS.keys():
            st.write(f"• {process}")
        
        st.markdown("---")
        
        st.subheader("🔍 What We Check")
        st.write("""
        • **Document Completeness** - All required documents uploaded
        • **Jurisdiction Clauses** - Proper ADGM Courts reference
        • **Governing Law** - ADGM law compliance
        • **Registration Authority** - Correct ADGM RA references
        • **Signature Requirements** - Proper signature blocks
        • **Document-specific Requirements** - Content validation
        """)
        
        st.markdown("---")
        
        st.subheader("📈 Compliance Scoring")
        st.write("""
        • **90-100**: Compliant ✅
        • **70-89**: Minor Issues ⚠️
        • **50-69**: Major Issues ❌
        • **<50**: Non-Compliant 🚫
        """)
        
        st.markdown("---")
        st.caption("Built with ADGM Official Sources")

def file_upload_section():
    """Handle file upload section"""
    st.header("📁 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Upload your ADGM documents (.docx files)",
        type=['docx'],
        accept_multiple_files=True,
        help="Upload all documents for your business process (incorporation, licensing, etc.)"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
        
        # Display uploaded files
        st.subheader("📄 Uploaded Files")
        for i, file in enumerate(uploaded_files):
            st.write(f"{i+1}. {file.name} ({file.size:,} bytes)")
        
        return uploaded_files
    
    return None

def process_documents(uploaded_files):
    """Process uploaded documents"""
    if not uploaded_files:
        return None
    
    with st.spinner("🔍 Analyzing documents for ADGM compliance..."):
        try:
            # Create temporary directory for processing
            temp_dir = tempfile.mkdtemp()
            output_dir = tempfile.mkdtemp()
            
            # Save uploaded files
            files_info = []
            for file in uploaded_files:
                temp_path = os.path.join(temp_dir, file.name)
                with open(temp_path, 'wb') as f:
                    f.write(file.getbuffer())
                
                files_info.append({
                    "name": file.name,
                    "path": temp_path
                })
            
            # Process documents
            processor = ADGMDocumentProcessor()
            results = processor.process_documents(files_info, output_dir)
            
            # Store results in session state
            st.session_state.processed_results = results
            st.session_state.output_dir = output_dir
            
            # Cleanup temp directory
            shutil.rmtree(temp_dir)
            
            return results
            
        except Exception as e:
            st.error(f"❌ Error processing documents: {str(e)}")
            return None

def display_process_analysis(results):
    """Display process analysis and checklist verification"""
    process_analysis = results.get("process_analysis", {})
    
    st.header("🎯 Process Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Detected Process",
            process_analysis.get("process", "Unknown"),
            help="Business process detected based on uploaded documents"
        )
    
    with col2:
        completeness = process_analysis.get("completeness_percentage", 0)
        st.metric(
            "Document Completeness",
            f"{completeness}%",
            help="Percentage of required documents uploaded"
        )
    
    with col3:
        status = process_analysis.get("status", "Unknown")
        color = "🟢" if status == "Complete" else "🔴"
        st.metric(
            "Status",
            f"{color} {status}",
            help="Overall document set status"
        )
    
    # Missing documents
    missing_docs = process_analysis.get("missing_documents", [])
    if missing_docs:
        st.subheader("❌ Missing Documents")
        for doc in missing_docs:
            st.error(f"📋 {doc}")
    
    # Found documents
    found_docs = process_analysis.get("found_documents", [])
    if found_docs:
        st.subheader("✅ Found Documents")
        for doc in found_docs:
            st.success(f"📄 {doc}")

def display_compliance_overview(results):
    """Display overall compliance overview"""
    overall = results.get("overall_compliance", {})
    summary = results.get("summary", {})
    
    st.header("📊 Compliance Overview")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = overall.get("average_score", 0)
        st.metric("Overall Score", f"{score}/100")
    
    with col2:
        st.metric("Total Issues", summary.get("total_issues", 0))
    
    with col3:
        st.metric("Critical Issues", summary.get("critical_issues", 0))
    
    with col4:
        st.metric("Warnings", summary.get("warnings", 0))
    
    # Compliance score display
    score = overall.get("average_score", 0)
    status = overall.get("status", "Unknown")
    
    if score >= 90:
        score_class = "score-excellent"
    elif score >= 70:
        score_class = "score-good"
    else:
        score_class = "score-poor"
    
    st.markdown(f"""
    <div class="compliance-score {score_class}">
        Compliance Status: {status} ({score}/100)
    </div>
    """, unsafe_allow_html=True)

def display_document_details(results):
    """Display detailed document analysis"""
    documents = results.get("documents", [])
    
    st.header("📋 Document Details")
    
    for i, doc in enumerate(documents):
        with st.expander(f"📄 {doc['original_filename']} - {doc['document_type'].replace('_', ' ').title()}", expanded=True):
            
            # Document metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Compliance Score", f"{doc['compliance_score']}/100")
            
            with col2:
                st.metric("Issues Found", doc['issues_count'])
            
            with col3:
                analysis = doc['analysis']
                status = analysis.get('compliance_status', 'Unknown')
                st.metric("Status", status)
            
            # Issues
            issues = analysis.get('issues_found', [])
            if issues:
                st.subheader("🚨 Issues Found")
                
                for issue in issues:
                    severity = issue.get('severity', 'Unknown')
                    severity_class = f"issue-{severity.lower()}"
                    
                    st.markdown(f"""
                    <div class="issue-card {severity_class}">
                        <strong>{severity} Severity:</strong> {issue.get('issue', 'Unknown issue')}<br>
                        <strong>Suggestion:</strong> {issue.get('suggestion', 'No suggestion')}<br>
                        <strong>ADGM Reference:</strong> {issue.get('adgm_reference', 'General')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No compliance issues found in this document!")

def display_download_section(results):
    """Display download section for reviewed documents and summary"""
    st.header("📥 Download Results")
    
    documents = results.get("documents", [])
    
    # Download reviewed documents
    if documents:
        st.subheader("📄 Reviewed Documents")
        
        for doc in documents:
            reviewed_path = doc.get('reviewed_document_path', '')
            if reviewed_path and os.path.exists(reviewed_path):
                with open(reviewed_path, 'rb') as file:
                    st.download_button(
                        label=f"📥 Download {doc['original_filename']} (Reviewed)",
                        data=file.read(),
                        file_name=f"reviewed_{doc['original_filename']}",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_{doc['original_filename']}"
                    )
    
    # Download JSON summary
    if 'output_dir' in st.session_state:
        json_path = os.path.join(st.session_state.output_dir, "compliance_summary.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as file:
                st.download_button(
                    label="📥 Download Compliance Summary (JSON)",
                    data=file.read(),
                    file_name=f"adgm_compliance_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

def display_json_output(results):
    """Display JSON output as specified in requirements"""
    st.header("🔧 JSON Output")
    
    # Create simplified JSON as per requirements
    process_analysis = results.get("process_analysis", {})
    summary = results.get("summary", {})
    
    json_output = {
        "process": process_analysis.get("process", "Unknown"),
        "documents_uploaded": summary.get("total_documents", 0),
        "required_documents": process_analysis.get("required_documents", 0),
        "missing_documents": process_analysis.get("missing_documents", []),
        "issues_found": []
    }
    
    # Add issues from all documents
    for doc in results.get("documents", []):
        for issue in doc["analysis"].get("issues_found", []):
            json_output["issues_found"].append({
                "document": doc["original_filename"],
                "section": f"Paragraph {issue.get('paragraph_index', 0)}",
                "issue": issue.get("issue", ""),
                "severity": issue.get("severity", ""),
                "suggestion": issue.get("suggestion", "")
            })
    
    st.json(json_output)

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # File upload section
    uploaded_files = file_upload_section()
    
    # Process button
    if uploaded_files:
        if st.button("🔍 Analyze Documents", type="primary", use_container_width=True):
            results = process_documents(uploaded_files)
            if results:
                st.success("✅ Analysis completed successfully!")
                st.rerun()
    
    # Display results if available
    if st.session_state.processed_results:
        results = st.session_state.processed_results
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "🎯 Process Analysis", 
            "📋 Document Details", 
            "📥 Downloads",
            "🔧 JSON Output"
        ])
        
        with tab1:
            display_compliance_overview(results)
        
        with tab2:
            display_process_analysis(results)
        
        with tab3:
            display_document_details(results)
        
        with tab4:
            display_download_section(results)
        
        with tab5:
            display_json_output(results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🏛️ ADGM Compliant Corporate Agent | Built with Official ADGM Sources</p>
        <p>⚠️ This tool provides guidance only. Always consult with qualified legal professionals.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

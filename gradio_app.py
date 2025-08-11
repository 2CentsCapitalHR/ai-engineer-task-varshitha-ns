"""Gradio alternative interface for ADGM Compliant Corporate Agent"""

import gradio as gr
import os
import tempfile
import shutil
import json
from datetime import datetime
from typing import List, Tuple, Dict, Any

# Import our modules
from src.document_processor import ADGMDocumentProcessor
from src.config import ADGM_DOCUMENT_SOURCES, PROCESS_CHECKLISTS

# Initialize the processor
processor = ADGMDocumentProcessor()

def process_documents_gradio(files) -> Tuple[str, str, str]:
    """Process documents and return results for Gradio interface"""
    if not files:
        return "❌ No files uploaded", "", ""
    
    try:
        # Create temporary directories
        temp_dir = tempfile.mkdtemp()
        output_dir = tempfile.mkdtemp()
        
        # Save uploaded files
        files_info = []
        for file in files:
            # Copy file to temp directory
            filename = os.path.basename(file.name)
            temp_path = os.path.join(temp_dir, filename)
            shutil.copy2(file.name, temp_path)
            
            files_info.append({
                "name": filename,
                "path": temp_path
            })
        
        # Process documents
        results = processor.process_documents(files_info, output_dir)
        
        # Generate summary report
        summary_report = generate_summary_report(results)
        
        # Generate JSON output
        json_output = generate_json_output(results)
        
        # Generate file list for downloads
        download_info = generate_download_info(results, output_dir)
        
        # Cleanup temp directory
        shutil.rmtree(temp_dir)
        
        return summary_report, json_output, download_info
        
    except Exception as e:
        return f"❌ Error processing documents: {str(e)}", "", ""

def generate_summary_report(results: Dict[str, Any]) -> str:
    """Generate a comprehensive summary report"""
    summary = results.get("summary", {})
    process_analysis = results.get("process_analysis", {})
    overall_compliance = results.get("overall_compliance", {})
    documents = results.get("documents", [])
    
    report = f"""
# 🏛️ ADGM COMPLIANCE REVIEW REPORT

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 EXECUTIVE SUMMARY

**Process Type:** {process_analysis.get('process', 'Unknown')}
**Overall Compliance Score:** {overall_compliance.get('average_score', 0)}/100
**Status:** {overall_compliance.get('status', 'Unknown')}

**Documents Processed:** {summary.get('total_documents', 0)}
**Total Issues Found:** {summary.get('total_issues', 0)}
**Critical Issues:** {summary.get('critical_issues', 0)}
**Warnings:** {summary.get('warnings', 0)}

## 🎯 DOCUMENT COMPLETENESS

**Required Documents:** {process_analysis.get('required_documents', 0)}
**Completeness:** {process_analysis.get('completeness_percentage', 0)}%

"""
    
    # Missing documents
    missing_docs = process_analysis.get('missing_documents', [])
    if missing_docs:
        report += "### ❌ Missing Documents:\n"
        for doc in missing_docs:
            report += f"- {doc}\n"
        report += "\n"
    
    # Found documents
    found_docs = process_analysis.get('found_documents', [])
    if found_docs:
        report += "### ✅ Found Documents:\n"
        for doc in found_docs:
            report += f"- {doc}\n"
        report += "\n"
    
    # Document details
    report += "## 📋 DOCUMENT ANALYSIS\n\n"
    
    for doc in documents:
        report += f"### 📄 {doc['original_filename']}\n"
        report += f"**Type:** {doc['document_type'].replace('_', ' ').title()}\n"
        report += f"**Compliance Score:** {doc['compliance_score']}/100\n"
        report += f"**Issues Found:** {doc['issues_count']}\n\n"
        
        issues = doc['analysis'].get('issues_found', [])
        if issues:
            report += "**Issues:**\n"
            for i, issue in enumerate(issues, 1):
                report += f"{i}. **{issue.get('severity', 'Unknown')} Severity:** {issue.get('issue', 'Unknown')}\n"
                report += f"   - *Suggestion:* {issue.get('suggestion', 'No suggestion')}\n"
                report += f"   - *ADGM Reference:* {issue.get('adgm_reference', 'General')}\n\n"
        else:
            report += "✅ No compliance issues found.\n\n"
    
    # Recommendations
    report += "## 🎯 RECOMMENDATIONS\n\n"
    
    if summary.get('critical_issues', 0) > 0:
        report += "🚨 **IMMEDIATE ACTION REQUIRED:**\n"
        report += "- Address all critical (High severity) issues before submission\n"
        report += "- Ensure proper ADGM jurisdiction and governing law clauses\n\n"
    
    if missing_docs:
        report += "📋 **COMPLETE DOCUMENT SET:**\n"
        report += "- Upload all missing required documents\n"
        report += "- Verify document completeness for your process type\n\n"
    
    if summary.get('warnings', 0) > 0:
        report += "⚠️ **REVIEW AND IMPROVE:**\n"
        report += "- Address warning-level issues to improve compliance\n"
        report += "- Ensure all signature blocks are properly formatted\n\n"
    
    report += "✅ **FINAL STEPS:**\n"
    report += "- Re-submit documents after making corrections\n"
    report += "- Consult with qualified legal professionals if needed\n"
    report += "- Keep reviewed documents for your records\n"
    
    return report

def generate_json_output(results: Dict[str, Any]) -> str:
    """Generate JSON output as per requirements"""
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
    
    return json.dumps(json_output, indent=2, ensure_ascii=False)

def generate_download_info(results: Dict[str, Any], output_dir: str) -> str:
    """Generate download information"""
    info = "## 📥 AVAILABLE DOWNLOADS\n\n"
    
    documents = results.get("documents", [])
    
    if documents:
        info += "### 📄 Reviewed Documents:\n"
        for doc in documents:
            reviewed_path = doc.get('reviewed_document_path', '')
            if reviewed_path and os.path.exists(reviewed_path):
                info += f"- **{doc['original_filename']}** (reviewed with comments)\n"
                info += f"  - Compliance Score: {doc['compliance_score']}/100\n"
                info += f"  - Issues Found: {doc['issues_count']}\n\n"
    
    # JSON summary
    json_path = os.path.join(output_dir, "compliance_summary.json")
    if os.path.exists(json_path):
        info += "### 🔧 Summary Files:\n"
        info += "- **compliance_summary.json** - Machine-readable summary\n\n"
    
    info += "**Note:** Download the reviewed documents to see detailed inline comments and suggestions."
    
    return info

def create_gradio_interface():
    """Create and configure Gradio interface"""
    
    # Custom CSS
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1f4e79, #d4af37);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    """
    
    with gr.Blocks(css=css, title="ADGM Compliant Corporate Agent") as app:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>⚖️ ADGM Compliant Corporate Agent</h1>
            <p>Intelligent AI Assistant for Abu Dhabi Global Market Document Review</p>
        </div>
        """)
        
        # Main interface
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📁 Upload Documents")
                gr.Markdown("Upload your ADGM documents (.docx files) for compliance review.")
                
                file_input = gr.File(
                    label="Select DOCX files",
                    file_count="multiple",
                    file_types=[".docx"],
                    height=150
                )
                
                process_btn = gr.Button(
                    "🔍 Analyze Documents", 
                    variant="primary",
                    size="lg"
                )
                
                # Information sidebar
                gr.Markdown("### 📋 Supported Documents")
                doc_categories = set([source.category for source in ADGM_DOCUMENT_SOURCES])
                for category in doc_categories:
                    gr.Markdown(f"• {category}")
                
                gr.Markdown("### 🎯 Process Types")
                for process in PROCESS_CHECKLISTS.keys():
                    gr.Markdown(f"• {process}")
            
            with gr.Column(scale=2):
                gr.Markdown("## 📊 Analysis Results")
                
                with gr.Tabs():
                    with gr.TabItem("📋 Summary Report"):
                        summary_output = gr.Markdown(
                            value="Upload documents and click 'Analyze Documents' to see results here.",
                            height=600
                        )
                    
                    with gr.TabItem("🔧 JSON Output"):
                        json_output = gr.Code(
                            language="json",
                            value="{}",
                            height=600
                        )
                    
                    with gr.TabItem("📥 Downloads"):
                        download_info = gr.Markdown(
                            value="Analysis results and download links will appear here.",
                            height=600
                        )
        
        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666;">
            <p>🏛️ Built with Official ADGM Sources | ⚠️ For guidance only - consult qualified legal professionals</p>
        </div>
        """)
        
        # Event handlers
        process_btn.click(
            fn=process_documents_gradio,
            inputs=[file_input],
            outputs=[summary_output, json_output, download_info]
        )
    
    return app

if __name__ == "__main__":
    # Create and launch the Gradio app
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )

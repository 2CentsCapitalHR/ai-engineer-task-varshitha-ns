"""Red flag detection system for ADGM document compliance"""

import re
from typing import List, Dict, Any, Tuple
from docx import Document
import logging
from .config import RED_FLAGS
from .rag_system import ADGMRAGSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ADGMRedFlagDetector:
    """Detects compliance issues and red flags in ADGM documents"""
    
    def __init__(self):
        self.red_flags = RED_FLAGS
        self.rag_system = ADGMRAGSystem()
    
    def analyze_document(self, file_path: str, document_type: str) -> Dict[str, Any]:
        """Analyze document for red flags and compliance issues"""
        try:
            doc = Document(file_path)
            document_analysis = {
                "document_type": document_type,
                "issues_found": [],
                "compliance_score": 100,
                "total_flags": 0,
                "critical_issues": 0,
                "warnings": 0
            }
            
            # Extract all text with paragraph tracking
            paragraphs_data = []
            for i, paragraph in enumerate(doc.paragraphs):
                if paragraph.text.strip():
                    paragraphs_data.append({
                        "index": i,
                        "text": paragraph.text,
                        "text_lower": paragraph.text.lower()
                    })
            
            # Check for red flags
            for flag_type, flag_config in self.red_flags.items():
                issues = self._detect_flag_in_paragraphs(
                    paragraphs_data, flag_type, flag_config
                )
                document_analysis["issues_found"].extend(issues)
            
            # Perform additional compliance checks
            additional_issues = self._perform_additional_checks(paragraphs_data, document_type)
            document_analysis["issues_found"].extend(additional_issues)
            
            # Calculate compliance score and categorize issues
            document_analysis = self._calculate_compliance_metrics(document_analysis)
            
            return document_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document {file_path}: {str(e)}")
            return {
                "document_type": document_type,
                "error": str(e),
                "issues_found": [],
                "compliance_score": 0
            }
    
    def _detect_flag_in_paragraphs(self, paragraphs_data: List[Dict], flag_type: str, flag_config: Dict) -> List[Dict]:
        """Detect specific red flag in document paragraphs"""
        issues = []
        patterns = flag_config["patterns"]
        
        for paragraph_data in paragraphs_data:
            text_lower = paragraph_data["text_lower"]
            
            for pattern in patterns:
                if pattern in text_lower:
                    # Get RAG guidance for this issue
                    guidance = self.rag_system.get_compliance_guidance(
                        "general", flag_type
                    )
                    
                    issue = {
                        "flag_type": flag_type,
                        "paragraph_index": paragraph_data["index"],
                        "paragraph_text": paragraph_data["text"][:200] + "..." if len(paragraph_data["text"]) > 200 else paragraph_data["text"],
                        "issue": flag_config["description"],
                        "pattern_found": pattern,
                        "severity": flag_config["severity"],
                        "suggestion": f"Replace with: {flag_config['correct']}",
                        "rag_guidance": guidance,
                        "adgm_reference": self._get_relevant_adgm_reference(flag_type)
                    }
                    issues.append(issue)
        
        return issues
    
    def _perform_additional_checks(self, paragraphs_data: List[Dict], document_type: str) -> List[Dict]:
        """Perform additional document-specific compliance checks"""
        issues = []
        all_text = " ".join([p["text_lower"] for p in paragraphs_data])
        
        # Check for missing signature blocks
        signature_patterns = ["signature", "signed by", "director signature", "authorized signatory"]
        has_signature = any(pattern in all_text for pattern in signature_patterns)
        
        if not has_signature:
            issues.append({
                "flag_type": "missing_signature",
                "paragraph_index": len(paragraphs_data) - 1,  # Point to end of document
                "paragraph_text": "End of document",
                "issue": "Document appears to be missing signature blocks",
                "severity": "Medium",
                "suggestion": "Add proper signature blocks for authorized signatories",
                "rag_guidance": self.rag_system.get_compliance_guidance(document_type, "signatures"),
                "adgm_reference": "ADGM Companies Regulations - Execution of Documents"
            })
        
        # Document-specific checks
        if document_type == "articles_of_association":
            issues.extend(self._check_articles_specific_requirements(paragraphs_data))
        elif document_type == "memorandum_of_association":
            issues.extend(self._check_memorandum_specific_requirements(paragraphs_data))
        elif document_type == "employment_contract":
            issues.extend(self._check_employment_contract_requirements(paragraphs_data))
        
        return issues
    
    def _check_articles_specific_requirements(self, paragraphs_data: List[Dict]) -> List[Dict]:
        """Check Articles of Association specific requirements"""
        issues = []
        all_text = " ".join([p["text_lower"] for p in paragraphs_data])
        
        required_sections = [
            ("share capital", "Share capital structure must be defined"),
            ("directors", "Directors' powers and responsibilities must be specified"),
            ("meetings", "Meeting procedures must be outlined"),
            ("dividends", "Dividend distribution rules must be included")
        ]
        
        for section, description in required_sections:
            if section not in all_text:
                issues.append({
                    "flag_type": "missing_section",
                    "paragraph_index": 0,
                    "paragraph_text": "Document structure",
                    "issue": f"Missing required section: {section}",
                    "severity": "High",
                    "suggestion": description,
                    "rag_guidance": self.rag_system.get_compliance_guidance("articles_of_association", section),
                    "adgm_reference": "ADGM Companies Regulations - Articles of Association Requirements"
                })
        
        return issues
    
    def _check_memorandum_specific_requirements(self, paragraphs_data: List[Dict]) -> List[Dict]:
        """Check Memorandum of Association specific requirements"""
        issues = []
        all_text = " ".join([p["text_lower"] for p in paragraphs_data])
        
        required_elements = [
            ("company name", "Company name must be clearly stated"),
            ("registered office", "Registered office address must be specified"),
            ("objects", "Company objects and powers must be defined"),
            ("liability", "Member liability must be specified")
        ]
        
        for element, description in required_elements:
            if element not in all_text:
                issues.append({
                    "flag_type": "missing_element",
                    "paragraph_index": 0,
                    "paragraph_text": "Document content",
                    "issue": f"Missing required element: {element}",
                    "severity": "High",
                    "suggestion": description,
                    "rag_guidance": self.rag_system.get_compliance_guidance("memorandum_of_association", element),
                    "adgm_reference": "ADGM Companies Regulations - Memorandum of Association Requirements"
                })
        
        return issues
    
    def _check_employment_contract_requirements(self, paragraphs_data: List[Dict]) -> List[Dict]:
        """Check Employment Contract specific requirements"""
        issues = []
        all_text = " ".join([p["text_lower"] for p in paragraphs_data])
        
        required_clauses = [
            ("job description", "Job description and duties must be specified"),
            ("salary", "Salary and compensation must be defined"),
            ("working hours", "Working hours and schedule must be outlined"),
            ("notice period", "Notice periods for termination must be specified"),
            ("data protection", "Data protection and confidentiality clauses required")
        ]
        
        for clause, description in required_clauses:
            if clause not in all_text:
                issues.append({
                    "flag_type": "missing_clause",
                    "paragraph_index": 0,
                    "paragraph_text": "Contract terms",
                    "issue": f"Missing required clause: {clause}",
                    "severity": "Medium",
                    "suggestion": description,
                    "rag_guidance": self.rag_system.get_compliance_guidance("employment_contract", clause),
                    "adgm_reference": "ADGM Employment Regulations 2019"
                })
        
        return issues
    
    def _get_relevant_adgm_reference(self, flag_type: str) -> str:
        """Get relevant ADGM regulation reference for the flag type"""
        reference_map = {
            "jurisdiction": "ADGM Courts and Civil Procedures Rules",
            "governing_law": "ADGM Companies Regulations",
            "registration_authority": "ADGM Registration Authority Regulations",
            "signature_requirements": "ADGM Companies Regulations - Execution of Documents"
        }
        return reference_map.get(flag_type, "ADGM General Regulations")
    
    def _calculate_compliance_metrics(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate compliance score and categorize issues"""
        issues = analysis["issues_found"]
        
        critical_count = len([i for i in issues if i["severity"] == "High"])
        warning_count = len([i for i in issues if i["severity"] == "Medium"])
        
        # Calculate compliance score (start with 100, deduct points for issues)
        score = 100
        score -= critical_count * 20  # 20 points per critical issue
        score -= warning_count * 10   # 10 points per warning
        score = max(0, score)  # Don't go below 0
        
        analysis.update({
            "compliance_score": score,
            "total_flags": len(issues),
            "critical_issues": critical_count,
            "warnings": warning_count,
            "compliance_status": self._get_compliance_status(score)
        })
        
        return analysis
    
    def _get_compliance_status(self, score: int) -> str:
        """Get compliance status based on score"""
        if score >= 90:
            return "Compliant"
        elif score >= 70:
            return "Minor Issues"
        elif score >= 50:
            return "Major Issues"
        else:
            return "Non-Compliant"

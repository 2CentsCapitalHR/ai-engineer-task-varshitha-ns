"""Configuration settings for ADGM Compliant Corporate Agent"""

import os
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ADGMDocumentSource:
    category: str
    document_type: str
    official_link: str

# ADGM Official Document Sources for RAG Knowledge Base - Complete from PDF
ADGM_DOCUMENT_SOURCES = [
    # Company Formation & Governance
    ADGMDocumentSource(
        category="Company Formation & Governance",
        document_type="General Incorporation, AoA, MoA, Registers, UBO, Board Resolutions",
        official_link="https://www.adgm.com/registration-authority/registration-and-incorporation"
    ),
    
    # Company Formation
    ADGMDocumentSource(
        category="Company Formation",
        document_type="Resolution for Incorporation (LTD - Multiple Shareholders)",
        official_link="https://assets.adgm.com/download/assets/adgm-ra-resolution-multiple-incorporate-shareholders-LTD-incorporation-v2.docx/186a12846c3911efa4e6c6223862cd87"
    ),
    
    # Company Formation & Compliance
    ADGMDocumentSource(
        category="Company Formation & Compliance",
        document_type="Incorporation, SPV, LLC, Other Forms & Templates",
        official_link="https://www.adgm.com/setting-up"
    ),
    
    # Policy & Guidance
    ADGMDocumentSource(
        category="Policy & Guidance",
        document_type="Guidance, Templates, Policy Statements",
        official_link="https://www.adgm.com/legal-framework/guidance-and-policy-statements"
    ),
    
    # ADGM Company Set-up Checklists
    ADGMDocumentSource(
        category="ADGM Company Set-up",
        document_type="Checklist – Company Set-up (Various Entities)",
        official_link="https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/branch-non-financial-services-20231228.pdf"
    ),
    ADGMDocumentSource(
        category="ADGM Company Set-up",
        document_type="Checklist – Private Company Limited",
        official_link="https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/private-company-limited-by-guarantee-non-financial-services-20231228.pdf"
    ),
    
    # Employment & HR
    ADGMDocumentSource(
        category="Employment & HR",
        document_type="Standard Employment Contract Template (2024 update)",
        official_link="https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+Template+-+ER+2024+(Feb+2025).docx/ee14b252edbe11efa63b12b3a30e5e3a"
    ),
    ADGMDocumentSource(
        category="Employment & HR",
        document_type="Standard Employment Contract Template (2019 short version)",
        official_link="https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+-+ER+2019+-+Short+Version+(May+2024).docx/33b57a92ecfe11ef97a536cc36767ef8"
    ),
    
    # Data Protection
    ADGMDocumentSource(
        category="Data Protection",
        document_type="Appropriate Policy Document Template",
        official_link="https://www.adgm.com/documents/office-of-data-protection/templates/adgm-dpr-2021-appropriate-policy-document.pdf"
    ),
    
    # Compliance & Filings
    ADGMDocumentSource(
        category="Compliance & Filings",
        document_type="Annual Accounts & Filings",
        official_link="https://www.adgm.com/operating-in-adgm/obligations-of-adgm-registered-entities/annual-filings/annual-accounts"
    ),
    
    # Letters/Permits
    ADGMDocumentSource(
        category="Letters/Permits",
        document_type="Application for Official Letters & Permits",
        official_link="https://www.adgm.com/operating-in-adgm/post-registration-services/letters-and-permits"
    ),
    
    # Regulatory Guidance
    ADGMDocumentSource(
        category="Regulatory Guidance",
        document_type="Incorporation Package, Filings, Templates",
        official_link="https://en.adgm.thomsonreuters.com/rulebook/7-company-incorporation-package"
    ),
    
    # Regulatory Template
    ADGMDocumentSource(
        category="Regulatory Template",
        document_type="Shareholder Resolution – Amendment of Articles",
        official_link="https://assets.adgm.com/download/assets/Templates_SHReso_AmendmentArticles-v1-20220107.docx/97120d7c5af911efae4b1e183375c0b2?forcedownload=1"
    ),
    
    # Additional sources from Data Sources PDF - Page 2
    # Compliance & Filings - Second entry from PDF
    ADGMDocumentSource(
        category="Compliance & Filings",
        document_type="Annual Accounts & Filings",
        official_link="https://www.adgm.com/operating-in-adgm/obligations-of-adgm-registered-entities/annual-filings/annual-accounts"
    ),
    
    # Letters/Permits - Second entry from PDF  
    ADGMDocumentSource(
        category="Letters/Permits",
        document_type="Application for Official Letters & Permits",
        official_link="https://www.adgm.com/operating-in-adgm/post-registration-services/letters-and-permits"
    ),
    
    # Regulatory Guidance - Second entry from PDF
    ADGMDocumentSource(
        category="Regulatory Guidance", 
        document_type="Incorporation Package, Filings, Templates",
        official_link="https://en.adgm.thomsonreuters.com/rulebook/7-company-incorporation-package"
    ),
    
    # Note: Some document types mentioned in the PDF (SHA, NDA, Consultancy Agreements)
    # exist as guidance or sample outlines and should be searched for on the main ADGM
    # guidance/templates page as mentioned in the PDF notes section
]

# Document type mappings for classification
DOCUMENT_TYPE_MAPPINGS = {
    # Order matters! More specific patterns should come first
    "memorandum_of_association": [
        "memorandum of association", "memorandum_of_association", "moa", "memorandum"
    ],
    "articles_of_association": [
        "articles of association", "articles_of_association", "aoa", "articles"
    ],
    "board_resolution": [
        "board resolution", "board_resolution", "resolution", "board", "directors resolution"
    ],
    "shareholder_resolution": [
        "shareholder resolution", "shareholders resolution", "member resolution"
    ],
    "incorporation_form": [
        "incorporation", "application form", "registration form", "incorporation_form"
    ],
    "ubo_declaration": [
        "ubo", "ubo_form", "ultimate beneficial owner", "beneficial owner", "declaration"
    ],
    "register_members": [
        "register of members", "members register", "register of directors", "directors register"
    ],
    "employment_contract": [
        "employment contract", "employment agreement", "contract of employment"
    ],
    "data_protection_policy": [
        "data protection", "privacy policy", "data policy"
    ],
    "annual_accounts": [
        "annual accounts", "financial statements", "accounts"
    ],
    "company_checklist": [
        "checklist", "setup checklist", "incorporation checklist"
    ]
}

# Required documents for different processes
PROCESS_CHECKLISTS = {
    "Company Incorporation": {
        "required_documents": [
            "Memorandum of Association",
            "Articles of Association", 
            "Incorporation Application Form",
            "UBO Declaration Form",
            "Register of Members and Directors"
        ],
        "optional_documents": [
            "Board Resolution for Incorporation",
            "Shareholder Resolution"
        ]
    },
    "Private Company Limited": {
        "required_documents": [
            "Memorandum of Association",
            "Articles of Association",
            "Application Form",
            "Register of Members",
            "Register of Directors",
            "UBO Declaration"
        ]
    },
    "Employment Setup": {
        "required_documents": [
            "Employment Contract",
            "Data Protection Policy"
        ]
    },
    "Annual Compliance": {
        "required_documents": [
            "Annual Accounts",
            "Annual Return"
        ]
    }
}

# Red flags and compliance issues
RED_FLAGS = {
    "jurisdiction": {
        "patterns": ["uae federal court", "dubai court", "sharjah court", "federal court"],
        "correct": "ADGM Courts",
        "severity": "High",
        "description": "Jurisdiction must be ADGM Courts, not UAE federal or other emirate courts"
    },
    "governing_law": {
        "patterns": ["uae law", "dubai law", "federal law"],
        "correct": "ADGM law",
        "severity": "High", 
        "description": "Governing law must reference ADGM law and regulations"
    },
    "registration_authority": {
        "patterns": ["department of economic development", "ded", "chamber of commerce"],
        "correct": "ADGM Registration Authority",
        "severity": "High",
        "description": "Registration authority must be ADGM Registration Authority"
    },
    "signature_requirements": {
        "patterns": ["without signature", "unsigned", "no signature block"],
        "correct": "Proper signature blocks required",
        "severity": "Medium",
        "description": "All documents must have proper signature blocks for authorized signatories"
    }
}

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCzVOyI-f3SKAfhD2nB_tyEw9FmmVzcsjs")
VECTOR_DB_PATH = "./data/vector_db"
TEMP_UPLOAD_PATH = "./temp"
OUTPUT_PATH = "./output"

# Performance settings
ENABLE_LLM_ANALYSIS = os.getenv("ENABLE_LLM_ANALYSIS", "false").lower() == "true"
FAST_MODE = os.getenv("FAST_MODE", "true").lower() == "true"

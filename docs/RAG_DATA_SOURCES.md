# RAG System Data Sources Implementation

## Overview

The ADGM Compliant Corporate Agent uses a comprehensive RAG (Retrieval-Augmented Generation) system that incorporates **ALL** the data sources from your provided PDF. This document explains how each source is utilized.

## Complete Data Sources from PDF

### ✅ Fully Implemented Sources

1. **Company Formation & Governance**
   - Document Types: General Incorporation, AoA, MoA, Registers, UBO, Board Resolutions
   - Official Link: https://www.adgm.com/registration-authority/registration-and-incorporation
   - **RAG Usage**: Provides foundational knowledge for company formation compliance

2. **Company Formation - Resolution Templates**
   - Document Type: Resolution for Incorporation (LTD - Multiple Shareholders)
   - Official Link: https://assets.adgm.com/download/assets/adgm-ra-resolution-multiple-incorporate-shareholders-LTD-incorporation-v2.docx/186a12846c3911efa4e6c6223862cd87
   - **RAG Usage**: Template validation for board resolutions

3. **Company Formation & Compliance**
   - Document Types: Incorporation, SPV, LLC, Other Forms & Templates
   - Official Link: https://www.adgm.com/setting-up
   - **RAG Usage**: Comprehensive guidance for various entity types

4. **Policy & Guidance**
   - Document Types: Guidance, Templates, Policy Statements
   - Official Link: https://www.adgm.com/legal-framework/guidance-and-policy-statements
   - **RAG Usage**: Legal framework validation and compliance guidance

5. **ADGM Company Set-up Checklists**
   - Document Type: Checklist – Company Set-up (Various Entities)
   - Official Link: https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/branch-non-financial-services-20231228.pdf
   - **RAG Usage**: Document completeness verification

6. **ADGM Company Set-up - Private Company**
   - Document Type: Checklist – Private Company Limited
   - Official Link: https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/private-company-limited-by-guarantee-non-financial-services-20231228.pdf
   - **RAG Usage**: Specific checklist validation for private companies

7. **Employment & HR (2024)**
   - Document Type: Standard Employment Contract Template (2024 update)
   - Official Link: https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+Template+-+ER+2024+(Feb+2025).docx/ee14b252edbe11efa63b12b3a30e5e3a
   - **RAG Usage**: Latest employment contract compliance validation

8. **Employment & HR (2019)**
   - Document Type: Standard Employment Contract Template (2019 short version)
   - Official Link: https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+-+ER+2019+-+Short+Version+(May+2024).docx/33b57a92ecfe11ef97a536cc36767ef8
   - **RAG Usage**: Legacy employment contract validation

9. **Data Protection**
   - Document Type: Appropriate Policy Document Template
   - Official Link: https://www.adgm.com/documents/office-of-data-protection/templates/adgm-dpr-2021-appropriate-policy-document.pdf
   - **RAG Usage**: Data protection compliance validation

10. **Compliance & Filings**
    - Document Type: Annual Accounts & Filings
    - Official Link: https://www.adgm.com/operating-in-adgm/obligations-of-adgm-registered-entities/annual-filings/annual-accounts
    - **RAG Usage**: Annual compliance requirements

11. **Letters/Permits**
    - Document Type: Application for Official Letters & Permits
    - Official Link: https://www.adgm.com/operating-in-adgm/post-registration-services/letters-and-permits
    - **RAG Usage**: Official correspondence validation

12. **Regulatory Guidance**
    - Document Type: Incorporation Package, Filings, Templates
    - Official Link: https://en.adgm.thomsonreuters.com/rulebook/7-company-incorporation-package
    - **RAG Usage**: Thomson Reuters regulatory guidance integration

13. **Regulatory Template**
    - Document Type: Shareholder Resolution – Amendment of Articles
    - Official Link: https://assets.adgm.com/download/assets/Templates_SHReso_AmendmentArticles-v1-20220107.docx/97120d7c5af911efae4b1e183375c0b2?forcedownload=1
    - **RAG Usage**: Shareholder resolution template validation

## How RAG System Uses These Sources

### 1. **Vector Database Population**
Each data source is processed and stored in ChromaDB with:
- **Content**: Detailed description and usage context
- **Metadata**: Category, document type, official link, compliance level
- **Embeddings**: Semantic search capabilities

### 2. **Contextual Guidance Generation**
For each source, the RAG system provides:
- **Usage Context**: When and how to use each document type
- **Regulatory Requirements**: Specific ADGM compliance requirements
- **Official Links**: Direct links to official ADGM templates

### 3. **Dynamic Retrieval**
When analyzing documents, the system:
- Queries relevant sources based on document type
- Provides contextual compliance guidance
- References specific ADGM regulations
- Suggests official templates when appropriate

### 4. **Compliance Validation**
The RAG system uses all sources to:
- Validate document completeness against official checklists
- Check compliance with ADGM regulations
- Provide specific guidance based on document category
- Reference official templates and requirements

## PDF Note Compliance

As noted in your PDF: *"Some document types (e.g., SHA, NDA, Consultancy Agreements) may only exist as guidance or sample outlines. For such documents, start with the main ADGM guidance/templates page and search for specifics or request them from the ADGM portal."*

The RAG system handles this by:
- Referencing the main ADGM guidance pages for undefined document types
- Providing general compliance guidance for non-templated documents
- Directing users to official ADGM portal for specific requests

## Technical Implementation

### Vector Database Structure
```python
{
    "content": "Detailed ADGM source information",
    "metadata": {
        "category": "Document category",
        "document_type": "Specific document type",
        "source": "official_adgm", 
        "link": "Official ADGM URL",
        "compliance_level": "mandatory"
    }
}
```

### Retrieval Process
1. **Semantic Search**: Query vector database for relevant sources
2. **Context Generation**: Provide usage context and requirements
3. **Compliance Check**: Validate against official ADGM requirements
4. **Reference Generation**: Include official links and regulations

## Verification

To verify RAG system coverage, check:
- `src/config.py` - ADGM_DOCUMENT_SOURCES array (13 sources)
- `src/rag_system.py` - Knowledge base population methods
- Vector database contents after initialization

**✅ Result**: All 13 data sources from your PDF are fully integrated into the RAG system and actively used for document compliance validation.
